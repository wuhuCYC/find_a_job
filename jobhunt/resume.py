"""简历组装：从素材库挑 bullet → 生成 RenderCV 的 YAML 结构 → 渲染 PDF（自动压到一页）。

两种来源：
  - select_base()：不调用 LLM，按岗位方向的权重挑（每个方向一份「基础简历」）
  - tailor.py：LLM 针对具体 JD 挑选 + 改写（再经过 guard 校验），产出同样的 ResumePlan
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from .bank import Bank, Education, Entry

# 各方向在技能栏里优先展示的分组和技能（只展示 working 及以上）
GROUP_ORDER = {
    "quant_dev": ["Languages", "Data & ML", "Backend", "Infra & Tools"],
    "quant_research": ["Languages", "Data & ML", "Backend", "Infra & Tools"],
    "trading_systems": ["Languages", "Backend", "Infra & Tools", "Data & ML"],
    "fintech_swe": ["Languages", "Backend", "Frontend", "Infra & Tools", "Data & ML"],
    "risk_data": ["Languages", "Data & ML", "Backend", "Infra & Tools"],
    "investment_analytics": ["Languages", "Data & ML", "Backend", "Infra & Tools"],
    "marketplace_econ": ["Languages", "Data & ML", "Backend", "Frontend", "Infra & Tools"],
}
SHOW_LEVELS = {"expert", "proficient", "working"}
_DATE = re.compile(r"^\d{4}(-\d{2})?$")


@dataclass
class PlannedEntry:
    entry: Entry
    bullet_ids: list[str]
    texts: list[str]
    weights: list[int] = field(default_factory=list)


@dataclass
class ResumePlan:
    archetype: str
    summary: str | None
    entries: list[PlannedEntry]
    skill_priority: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def drop_weakest_bullet(self) -> bool:
        """一页放不下时，删掉权重最低的一条（每段经历至少留 1 条；都只剩 1 条就删最弱的整段）。"""
        candidates = [
            (pe.weights[i] if i < len(pe.weights) else 0, -i, n, i)
            for n, pe in enumerate(self.entries) if len(pe.texts) > 1
            for i in range(len(pe.texts))
        ]
        if candidates:
            _, _, n, i = min(candidates)
            pe = self.entries[n]
            for lst in (pe.texts, pe.bullet_ids, pe.weights):
                if i < len(lst):
                    del lst[i]
            return True
        if len(self.entries) > 1:
            weakest = min(range(len(self.entries)), key=lambda k: max(self.entries[k].weights or [0]))
            del self.entries[weakest]
            return True
        return False


def select_base(bank: Bank, archetype: str, max_bullets: int = 13, per_entry: int = 4, min_weight: int = 1,
                min_total: int = 9) -> ResumePlan:
    """按方向权重挑 bullet（确定性，不用 LLM）。

    该方向相关的 bullet 太少时（例如 marketplace_econ），用其他经历里最强的 1-2 条补足，
    避免一份简历只剩两段经历。
    """
    scored = []
    for e in bank.entries:
        bullets = [(b, b.weights.get(archetype, 0)) for b in e.bullets]
        bullets = [(b, w) for b, w in bullets if w >= min_weight]
        if not bullets:
            continue
        bullets.sort(key=lambda x: -x[1])  # 稳定排序：同权重保留素材库里的顺序
        top = bullets[:per_entry]
        entry_score = sum(w for _, w in top[:3]) + (100 if e.kind == "experience" else 0)
        scored.append((entry_score, e, top))
    scored.sort(key=lambda x: -x[0])

    have = sum(min(len(top), per_entry) for _, _, top in scored)
    if have < min_total:
        included = {e.id for _, e, _ in scored}
        for e in bank.entries:
            if e.id in included or have >= min_total:
                continue
            # 补位的 bullet 权重记为 0：一页放不下时最先被删
            fill = sorted(e.bullets, key=lambda b: -max(b.weights.values() or [0]))[:2]
            if fill:
                scored.append((0, e, [(b, 0) for b in fill]))
                have += len(fill)

    # 全局按权重分配名额，保证每段经历至少 2 条（如果它有 2 条）
    picked: dict[str, list] = {e.id: top[: min(2, len(top))] for _, e, top in scored}
    budget = max_bullets - sum(len(v) for v in picked.values())
    extras = sorted(
        ((w, e.id, b) for _, e, top in scored for b, w in top[2:]),
        key=lambda x: -x[0],
    )
    for w, eid, b in extras:
        if budget <= 0:
            break
        picked[eid].append((b, w))
        budget -= 1

    entries = []
    for _, e, _top in scored:
        chosen = picked[e.id]
        # 段内按素材库的叙事顺序排（「Stress-tested that edge」必须紧跟在事件研究那条后面）
        order = {b.id: k for k, b in enumerate(e.bullets)}
        chosen.sort(key=lambda x: order[x[0].id])
        entries.append(PlannedEntry(entry=e, bullet_ids=[b.id for b, _ in chosen],
                                    texts=[b.text for b, _ in chosen], weights=[w for _, w in chosen]))
    return ResumePlan(archetype=archetype, summary=bank.summaries.get(archetype), entries=entries)


# ----------------------------------------------------------------- RenderCV
def _clean_date(value) -> str | None:
    if value is None:
        return None
    s = str(value).strip()
    if s.lower() == "present":
        return "present"
    return s if _DATE.match(s) else None


def _is_placeholder(value) -> bool:
    return value is None or str(value).strip() == "" or "TODO" in str(value)


def _skills_section(bank: Bank, archetype: str, priority: list[str]) -> list[dict]:
    order = GROUP_ORDER.get(archetype, GROUP_ORDER["fintech_swe"])
    groups: dict[str, list[str]] = {}
    for s in bank.skills:
        if s.level in SHOW_LEVELS and s.group in order:
            groups.setdefault(s.group, []).append(s.name)
    rank = {name.lower(): i for i, name in enumerate(priority)}
    out = []
    for g in order:
        names = groups.get(g) or []
        names.sort(key=lambda n: rank.get(n.lower(), 1000))  # 稳定排序：没指定优先级的保持原顺序
        if names:
            out.append({"label": g, "details": ", ".join(names)})
    langs = [f"{x['name']} ({x['level']})" for x in bank.spoken_languages if not _is_placeholder(x.get("level"))]
    if langs:
        out.append({"label": "Spoken Languages", "details": ", ".join(langs)})
    return out


def _education_entry(ed: Education) -> dict:
    item = {"institution": ed.institution, "area": ed.area, "degree": ed.degree}
    if not _is_placeholder(ed.location):
        item["location"] = ed.location
    start, end = _clean_date(ed.start), _clean_date(ed.end)
    if start:
        item["start_date"] = start
    if end:
        item["end_date"] = end
    highlights = []
    if not _is_placeholder(ed.gpa):
        highlights.append(f"GPA: {ed.gpa}")
    courses = [c for c in ed.coursework if not _is_placeholder(c)]
    if courses:
        highlights.append("Coursework: " + ", ".join(courses))
    if highlights:
        item["highlights"] = highlights
    return item


def to_rendercv(plan: ResumePlan, bank: Bank, profile: dict, include_summary: bool = True) -> dict:
    person = profile.get("person") or {}
    cv: dict = {"name": person.get("name") or "Your Name"}
    for key in ("location", "email", "phone", "website"):
        if not _is_placeholder(person.get(key)):
            cv[key] = person[key]
    socials = []
    for network, key in (("LinkedIn", "linkedin"), ("GitHub", "github")):
        if not _is_placeholder(person.get(key)):
            socials.append({"network": network, "username": person[key]})
    if socials:
        cv["social_networks"] = socials

    sections: dict = {}
    if include_summary and plan.summary:
        sections["summary"] = [plan.summary.strip()]
    edu = [_education_entry(ed) for ed in bank.education if not _is_placeholder(ed.institution)]
    if edu:
        sections["education"] = edu

    experience, projects = [], []
    for pe in plan.entries:
        e = pe.entry
        start, end = _clean_date(e.start), _clean_date(e.end)
        dates = {k: v for k, v in (("start_date", start), ("end_date", end)) if v}
        if e.kind == "experience":
            item = {"company": e.org or e.title, "position": e.role or e.title, **dates, "highlights": pe.texts}
            if e.location:
                item["location"] = e.location
            experience.append(item)
        else:
            name = f"[{e.title}]({e.url})" if e.url else e.title
            role = e.role.strip() if not _is_placeholder(e.role) else ""
            summary = " · ".join(x for x in (f"*{role}*" if role else "", ", ".join(e.stack[:7])) if x)
            item = {"name": name, **dates, "summary": summary, "highlights": pe.texts}
            projects.append(item)
    if experience:
        sections["experience"] = experience
    if projects:
        sections["projects"] = projects
    sections["skills"] = _skills_section(bank, plan.archetype, plan.skill_priority)

    # 四边页边距必须相同：RenderCV 2.3 的模板在 Typst 0.15 下遇到不等边距会报
    # "cannot multiply dictionary with integer"
    design = {
        "theme": "engineeringresumes",
        "page": {
            "size": "us-letter",
            "top_margin": "1.4cm",
            "bottom_margin": "1.4cm",
            "left_margin": "1.4cm",
            "right_margin": "1.4cm",
            "show_page_numbering": False,
            "show_last_updated_date": False,
        },
        "text": {"font_size": "10pt", "leading": "0.55em"},
        "section_titles": {"vertical_space_above": "0.4cm", "vertical_space_below": "0.2cm"},
        "entries": {"vertical_space_between_entries": "0.3cm"},
        "highlights": {"vertical_space_between_highlights": "0.12cm", "top_margin": "0.15cm"},
    }
    design.update(profile.get("resume_design") or {})
    return {"cv": {**cv, "sections": sections}, "design": design}


# ------------------------------------------------------------------ 渲染
def rendercv_command() -> list[str] | None:
    exe = shutil.which("rendercv")
    if exe:
        return [exe]
    candidate = Path(sys.executable).parent / "rendercv"
    return [str(candidate)] if candidate.exists() else None


def pdf_page_count(pdf: Path) -> int | None:
    try:
        from pypdf import PdfReader
    except ImportError:
        return None
    return len(PdfReader(str(pdf)).pages)


def render_yaml(yaml_path: Path, pdf_path: Path) -> None:
    cmd = rendercv_command()
    if not cmd:
        raise RuntimeError('没找到 rendercv，请先 pip install "rendercv[full]"')
    work = yaml_path.parent / "rendercv_output"
    result = subprocess.run(
        [*cmd, "render", str(yaml_path), "--pdf-path", str(pdf_path), "-o", str(work),
         "--dont-generate-markdown", "--dont-generate-html", "--dont-generate-png"],
        capture_output=True, text=True,
    )
    if result.returncode != 0 or not pdf_path.exists():
        raise RuntimeError(f"RenderCV 渲染失败：\n{result.stdout[-2000:]}\n{result.stderr[-2000:]}")


def write_and_render(plan: ResumePlan, bank: Bank, profile: dict, out_dir: Path, basename: str,
                     render_pdf: bool = True, fit_one_page: bool = True, include_summary: bool = True) -> dict:
    """写 YAML（给你手动微调用）并渲染 PDF；超过一页就逐条删最弱的 bullet 重排。"""
    out_dir.mkdir(parents=True, exist_ok=True)
    yaml_path = out_dir / f"{basename}.yaml"
    pdf_path = out_dir / f"{basename}.pdf"
    dropped = 0
    while True:
        data = to_rendercv(plan, bank, profile, include_summary=include_summary)
        yaml_path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=110), encoding="utf-8")
        if not render_pdf:
            return {"yaml": yaml_path, "pdf": None, "pages": None, "dropped": 0}
        render_yaml(yaml_path, pdf_path)
        pages = pdf_page_count(pdf_path)
        if not fit_one_page or pages is None or pages <= 1 or dropped >= 10:
            return {"yaml": yaml_path, "pdf": pdf_path, "pages": pages, "dropped": dropped}
        if include_summary and dropped == 0 and plan.summary:
            include_summary = False  # 先去掉 summary 省一行
        elif not plan.drop_weakest_bullet():
            return {"yaml": yaml_path, "pdf": pdf_path, "pages": pages, "dropped": dropped}
        dropped += 1
