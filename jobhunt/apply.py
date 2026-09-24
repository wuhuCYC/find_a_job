"""半自动投递：打开申请页 → 自动填基本信息、上传定制简历 → 停下来，由你检查并亲手点 Submit。

为什么不全自动点提交：
  - 签证、工作授权、EEO 这类问题答错有法律后果，必须本人确认；
  - 很多 ATS 有 reCAPTCHA，LinkedIn 等平台用户协议明确禁止自动化，封号得不偿失；
  - 金融公司 HR 能看到同一个人投了多少岗，海投反而减分 —— 质量 > 数量。

依赖：pip install playwright，然后 `playwright install chromium`（或用本机 Chrome：JOBHUNT_BROWSER_CHANNEL=chrome）。
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from .config import DATA_DIR

# (标签正则, 值的 key) —— 按顺序匹配，先命中先用
FIELD_RULES: list[tuple[str, str]] = [
    (r"\b(legal\s+)?first\s*name\b|\bgiven\s+name\b|\bpreferred\s+first\s+name\b", "first_name"),
    (r"\b(legal\s+)?last\s*name\b|\bfamily\s+name\b|\bsurname\b", "last_name"),
    (r"^\s*(full\s+|legal\s+|your\s+)?name\s*\*?\s*$|\bfull\s+(legal\s+)?name\b", "full_name"),
    (r"e-?mail", "email"),
    (r"\bphone\b|\bmobile\b|\bcell\b", "phone"),
    (r"linkedin", "linkedin_url"),
    (r"github", "github_url"),
    (r"\bwebsite\b|\bportfolio\b|\bpersonal\s+(site|url)\b|\bother\s+url\b", "website"),
    (r"current\s+(company|employer)|^\s*org(anization)?\s*$", "current_company"),
    (r"\b(current\s+)?location\b|\bcity\b", "location"),
    (r"\bschool\b|\buniversity\b|\bcollege\b", "school"),
    (r"\bdegree\b", "degree"),
    (r"graduation|grad(uation)?\s+date", "graduation"),
    (r"how\s+did\s+you\s+(hear|find)", "how_did_you_hear"),
]
TEXT_TYPES = {"", "text", "email", "tel", "url", "search"}

COLLECT_JS = """
() => {
  const els = Array.from(document.querySelectorAll('input, textarea, select'));
  return els.map((el, i) => {
    el.setAttribute('data-jobhunt-idx', String(i));
    let label = '';
    if (el.id) {
      const l = document.querySelector('label[for="' + CSS.escape(el.id) + '"]');
      if (l) label = l.innerText;
    }
    if (!label) { const l = el.closest('label'); if (l) label = l.innerText; }
    if (!label) label = el.getAttribute('aria-label') || '';
    if (!label) {
      const ids = (el.getAttribute('aria-labelledby') || '').split(/\\s+/).filter(Boolean);
      label = ids.map(id => (document.getElementById(id) || {}).innerText || '').join(' ');
    }
    if (!label) label = el.getAttribute('placeholder') || '';
    if (!label) label = el.getAttribute('name') || '';
    return {
      idx: i, tag: el.tagName.toLowerCase(), type: (el.getAttribute('type') || '').toLowerCase(),
      label: (label || '').trim().replace(/\\s+/g, ' ').slice(0, 200),
      name: el.getAttribute('name') || '', id: el.id || '',
      required: !!(el.required || el.getAttribute('aria-required') === 'true'),
      value: el.value || '',
      visible: !!(el.offsetWidth || el.offsetHeight || el.getClientRects().length),
    };
  });
}
"""


def profile_values(profile: dict) -> dict[str, str]:
    person = profile.get("person") or {}
    grad = profile.get("graduation") or {}
    answers = profile.get("application_answers") or {}
    name = person.get("name") or ""
    first = person.get("first_name") or (name.split()[0] if name else "")
    last = person.get("last_name") or (name.split()[-1] if len(name.split()) > 1 else "")
    li, gh = person.get("linkedin") or "", person.get("github") or ""
    values = {
        "first_name": first,
        "last_name": last,
        "full_name": name,
        "email": person.get("email") or "",
        "phone": person.get("phone") or "",
        "linkedin_url": li if li.startswith("http") or not li else f"https://www.linkedin.com/in/{li}",
        "github_url": gh if gh.startswith("http") or not gh else f"https://github.com/{gh}",
        "website": person.get("website") or "",
        "current_company": answers.get("current_company") or "",
        "location": person.get("location") or "",
        "school": grad.get("school") or "",
        "degree": grad.get("degree") or "",
        "graduation": str(grad.get("date") or ""),
        "how_did_you_hear": answers.get("how_did_you_hear") or "",
    }
    return {k: v for k, v in values.items() if v and "TODO" not in str(v)}


def match_field(label: str, name: str = "", field_id: str = "") -> str | None:
    text = " ".join(x for x in (label, name.replace("_", " "), field_id.replace("_", " ")) if x)
    for pattern, key in FIELD_RULES:
        if re.search(pattern, label, re.I) or (not label and re.search(pattern, text, re.I)):
            return key
    # label 没命中时再看 name/id（Lever 的 name="urls[LinkedIn]" 这种）
    for pattern, key in FIELD_RULES:
        if re.search(pattern, text, re.I):
            return key
    return None


def is_resume_input(field: dict) -> bool:
    text = f"{field['label']} {field['name']} {field['id']}".lower()
    return field["type"] == "file" and ("resume" in text or re.search(r"\bcv\b", text) is not None) \
        and "cover" not in text


def plan_fill(fields: list[dict], values: dict[str, str]) -> tuple[list[tuple[int, str, str]], list[dict]]:
    """决定哪些字段填什么；返回 (要填的 [(idx, key, value)], 需要你手动处理的字段)。"""
    to_fill, manual = [], []
    used_keys: set[str] = set()
    for f in fields:
        if not f["visible"] or f["type"] in {"hidden", "submit", "button", "image", "reset"}:
            continue
        if f["type"] == "file":
            if not is_resume_input(f):
                manual.append(f)
            continue
        if f["tag"] == "select" or f["type"] in {"checkbox", "radio"}:
            if f["required"] or f["label"]:
                manual.append(f)
            continue
        if f["type"] not in TEXT_TYPES and f["tag"] != "textarea":
            continue
        key = match_field(f["label"], f["name"], f["id"])
        if key and key in values and not f["value"] and (key not in used_keys or key in {"email", "phone"}):
            to_fill.append((f["idx"], key, values[key]))
            used_keys.add(key)
        elif f["required"] and not f["value"]:
            manual.append(f)
    return to_fill, manual


def prefill_page(page, profile: dict, resume_pdf: Path | None) -> dict:
    """在已打开的页面上预填。绝不点击提交按钮。"""
    fields = page.evaluate(COLLECT_JS)
    to_fill, manual = plan_fill(fields, profile_values(profile))
    filled = []
    for idx, key, value in to_fill:
        try:
            page.fill(f'[data-jobhunt-idx="{idx}"]', value)
            filled.append(key)
        except Exception as exc:  # noqa: BLE001 —— 单个字段失败不影响其他字段
            manual.append({"label": f"{key}（自动填失败：{exc.__class__.__name__}）", "required": True})
    uploaded = False
    if resume_pdf:
        for f in fields:
            if f["visible"] and is_resume_input(f):
                page.set_input_files(f'[data-jobhunt-idx="{f["idx"]}"]', str(resume_pdf))
                uploaded = True
                break
    return {"filled": filled, "uploaded": uploaded, "manual": manual}


def apply_url_for(url: str, apply_url: str | None) -> str:
    target = apply_url or url
    if "jobs.lever.co" in target and not target.rstrip("/").endswith("/apply"):
        target = target.rstrip("/") + "/apply"
    if "jobs.ashbyhq.com" in target and not target.rstrip("/").endswith("/application"):
        target = target.rstrip("/") + "/application"
    return target


def open_and_prefill(url: str, profile: dict, resume_pdf: Path | None) -> dict:
    from playwright.sync_api import sync_playwright

    channel = os.environ.get("JOBHUNT_BROWSER_CHANNEL")          # 例如 chrome（用本机 Chrome）
    executable = os.environ.get("JOBHUNT_BROWSER_PATH")          # 或指定浏览器可执行文件
    user_dir = DATA_DIR / "browser-profile"                       # 保留登录状态（Workday 账号等）
    user_dir.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        kwargs = {"headless": False}
        if channel:
            kwargs["channel"] = channel
        if executable:
            kwargs["executable_path"] = executable
        ctx = p.chromium.launch_persistent_context(str(user_dir), **kwargs)
        page = ctx.pages[0] if ctx.pages else ctx.new_page()
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(2500)  # 等前端框架渲染出表单
        result = prefill_page(page, profile, resume_pdf)
        print_checklist(result, profile)
        print("\n浏览器保持打开。检查无误后【你自己】点 Submit；完成后关闭浏览器窗口回到这里。")
        page.wait_for_event("close", timeout=0)
        ctx.close()
    return result


def print_checklist(result: dict, profile: dict) -> None:
    print(f"\n✅ 已自动填写：{', '.join(result['filled']) or '（没有识别到标准字段）'}")
    print(f"{'✅' if result['uploaded'] else '⚠'} 简历上传：{'已上传' if result['uploaded'] else '没找到简历上传框，请手动上传'}")
    manual = [m for m in result["manual"] if m.get("label")]
    if manual:
        print("\n需要你手动处理的字段：")
        for m in manual[:40]:
            print(f"  - {'[必填] ' if m.get('required') else ''}{m['label']}")
    answers = profile.get("application_answers") or {}
    auth = profile.get("work_authorization") or {}
    print("\n常见问题的参考答案（来自 private/profile.yaml，务必如实）：")
    print(f"  - Legally authorized to work in the US?  {auth.get('authorized_to_work_answer', 'TODO：在 profile 里填')}")
    print(f"  - Require sponsorship now or in future?   {auth.get('sponsorship_answer', 'TODO：在 profile 里填')}")
    for key in ("willing_to_relocate", "earliest_start_date", "salary_expectation", "eeo"):
        if answers.get(key):
            print(f"  - {key}: {answers[key]}")
