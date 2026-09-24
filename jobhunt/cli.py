"""命令行入口：python -m jobhunt <命令>

  check                 检查 companies.yaml 里每家公司的招聘接口配置是否有效
  fetch [-c KEY ...]    抓取职位（默认所有 enabled 的公司）
  score                 给所有在招职位打分
  list [选项]           看排名（可导出 Markdown / CSV）
  show UID              看一个职位的打分理由和 JD
  base [-a 方向|all]    生成各方向的基础简历（不调用 LLM）
  tailor UID            针对某个职位定制简历 + 差距报告（调用 Claude）
  tailor --jd-file F    针对你手动粘贴的 JD 定制
  apply UID             打开申请页、预填、上传简历（你自己点提交）
  status UID 状态       更新投递状态：shortlisted/applied/oa/interview/offer/rejected/skipped
  validate              校验经历素材库（数字/技术栈都有事实支撑）
  web                   打开本地可视化网站（--export 导出单文件快照）
  run                   一条龙：fetch → score → 导出 output/jobs.md
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

from . import config
from .bank import load_bank, validate_bank
from .http import Http
from .models import Job
from .store import STATUSES, Store


def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


# ------------------------------------------------------------------ 抓取
def cmd_check(args) -> int:
    from .fetchers import fetch_company

    http = Http(delay=0.3)
    bad = 0
    for c in config.load_companies():
        if not c.enabled:
            continue
        if c.ats_type == "manual":
            print(f"  ·  {c.key:<22} 手动：{c.careers_url or '（没填官网链接）'}")
            continue
        try:
            fetch_company(c, http, prefilter=lambda t, l: False)  # 只验证列表接口，不抓详情
            print(f"  ✓  {c.key:<22} {c.ats_type:<15} 接口正常")
        except Exception as exc:  # noqa: BLE001
            bad += 1
            print(f"  ✗  {c.key:<22} {c.ats_type:<15} {str(exc)[:120]}")
    print(f"\n{bad} 家公司配置有问题（改 config/companies.yaml 里的 ats 字段，或改成 type: manual）")
    return 1 if bad else 0


def cmd_fetch(args) -> int:
    from .actions import fetch_all

    total_new = fetch_all(keys=args.company, tier=args.tier)
    print(f"\n本次新增 {total_new} 个职位。下一步：python -m jobhunt score")
    return 0


def cmd_score(args) -> int:
    from .actions import score_all

    total, kept = score_all()
    print(f"已打分 {total} 个职位，其中 {kept} 个进入候选。下一步：python -m jobhunt list")
    return 0


# ------------------------------------------------------------------ 查看
def _filtered_rows(args):
    rows = Store().ranked(min_score=args.min, include_excluded=args.all, status=args.status, only_new=args.new)
    out = []
    for r in rows:
        detail = json.loads(r["detail"])
        if args.region and not set(args.region.split(",")) & set(detail["regions"]):
            continue
        if args.archetype and detail["archetype"] != args.archetype:
            continue
        if args.hide_visa and "visa_blocker" in detail["flags"]:
            continue
        out.append((r, detail))
    return out[: args.limit]


def cmd_list(args) -> int:
    rows = _filtered_rows(args)
    if not rows:
        print("没有符合条件的职位。先跑 fetch + score，或放宽 --min。")
        return 0
    for r, d in rows:
        flags = " ".join(f"[{f}]" for f in d["flags"] if f in ("visa_blocker", "no_sponsorship", "e_verify") or f.startswith("yoe"))
        print(f"{r['score']:5.1f}  {r['company'][:18]:<18}  {r['title'][:52]:<52}  {'/'.join(d['regions'])[:10]:<10}"
              f"  {(d['archetype'] or '-')[:16]:<16} {r['status']:<10} {flags}")
        print(f"       uid={r['uid']}")
    if args.md:
        export_markdown(rows, Path(args.md))
        print(f"\n已导出 {args.md}")
    if args.csv:
        export_csv(rows, Path(args.csv))
        print(f"已导出 {args.csv}")
    return 0


def export_markdown(rows, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# 职位排名（{date.today().isoformat()}）", "",
             "| 分数 | 公司 | 职位 | 地区 | 方向 | 状态 | 标记 | uid |", "|---|---|---|---|---|---|---|---|"]
    for r, d in rows:
        title = f"[{r['title']}]({r['url']})" if r["url"] else r["title"]
        lines.append(f"| {r['score']:.1f} | {r['company']} | {title} | {'/'.join(d['regions'])} | "
                     f"{d['archetype'] or '-'} | {r['status']} | {' '.join(d['flags'])} | `{r['uid']}` |")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_csv(rows, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["score", "company", "title", "regions", "archetype", "status", "flags", "url", "uid"])
        for r, d in rows:
            w.writerow([r["score"], r["company"], r["title"], "/".join(d["regions"]), d["archetype"],
                        r["status"], " ".join(d["flags"]), r["url"], r["uid"]])


def _resolve_job(store: Store, uid: str) -> Job:
    full = store.find_uid(uid)
    job = store.get_job(full) if full else None
    if not job:
        sys.exit(f"找不到职位 {uid}（用 list 看完整 uid）")
    return job


def cmd_show(args) -> int:
    store = Store()
    job = _resolve_job(store, args.uid)
    detail = store.get_score(job.uid) or {}
    print(f"{job.company} — {job.title}\n{job.url}\n地点：{'; '.join(job.locations)}  薪资：{job.salary or '未写'}")
    print(f"\n分数 {detail.get('score')}  方向 {detail.get('archetype')}  标记 {detail.get('flags')}")
    for reason in detail.get("reasons", []):
        print(f"  - {reason}")
    if detail.get("excluded"):
        print(f"  ✗ 被过滤：{detail.get('exclude_reason')}")
    if args.jd:
        print("\n" + job.description)
    return 0


# ------------------------------------------------------------------ 简历
def cmd_base(args) -> int:
    from .actions import render_base

    archetypes = None if args.archetype == "all" else [args.archetype]
    for r in render_base(archetypes, render_pdf=not args.no_pdf):
        print(f"  ✓ {r['archetype']:<22} {r['pdf'] or r['yaml']}  页数={r['pages']} 删减={r['dropped']}")
    if config.profile_path().name == "profile.example.yaml":
        print("\n⚠ 还在用 profile.example.yaml 的占位信息。复制到 private/profile.yaml 填真实信息后再生成。")
    return 0


def cmd_tailor(args) -> int:
    from .actions import tailor_job

    store = Store()
    if args.jd_file:
        text = Path(args.jd_file).read_text(encoding="utf-8")
        job = Job(company_key="manual", company=args.company or "Company", source="manual",
                  source_id=_slug(args.title or "role"), title=args.title or "Role", url=args.url or "",
                  locations=[args.location] if args.location else [], description=text)
    else:
        job = _resolve_job(store, args.uid)
    print(f"正在为 {job.company} — {job.title} 定制（调用 Claude）…")
    result = tailor_job(job, store=store, render_pdf=not args.no_pdf)
    print(f"\n简历：{result['pdf'] or result['yaml']}\n报告：{result['report']}")
    for w in result["warnings"]:
        print(f"  ⚠ {w}")
    return 0


def cmd_apply(args) -> int:
    from .apply import apply_url_for, open_and_prefill

    store = Store()
    job = _resolve_job(store, args.uid)
    from .actions import resume_for

    resume = Path(args.resume) if args.resume else resume_for(store, job.uid)
    if resume is None or not resume.exists():
        print("⚠ 没有这个职位的定制简历（先跑 tailor），这次不上传简历。")
        resume = None
    open_and_prefill(apply_url_for(job.url, job.apply_url), config.load_profile(), resume)
    answer = input("\n你已经在浏览器里点了提交吗？[y/N] ").strip().lower()
    store.set_status(job.uid, "applied" if answer == "y" else "prefilled")
    print("状态已更新。")
    return 0


def cmd_status(args) -> int:
    store = Store()
    job = _resolve_job(store, args.uid)
    store.set_status(job.uid, args.status, notes=args.note)
    print(f"{job.company} — {job.title} → {args.status}")
    return 0


def cmd_validate(args) -> int:
    bank = load_bank()
    problems = validate_bank(bank, config.load_search().get("skill_vocabulary"))
    if problems:
        print("素材库有问题：")
        for p in problems:
            print(f"  ✗ {p}")
        return 1
    n = sum(len(e.bullets) for e in bank.entries)
    print(f"✓ 素材库通过校验：{len(bank.entries)} 段经历、{n} 条 bullet，数字和技术栈都有事实支撑。")
    todo = sum(1 for line in config.bank_path().read_text(encoding="utf-8").splitlines() if "TODO" in line)
    if todo:
        print(f"  还有 {todo} 处 TODO 等你补充（grep -n TODO {config.bank_path()}）")
    return 0


def cmd_web(args) -> int:
    from .web.export import export_site
    from .web.server import serve

    if args.export:
        path = export_site(Path(args.export), standalone=not args.artifact, include_jobs=not args.no_jobs)
        print(f"已导出单文件网站：{path}")
        return 0
    serve(port=args.port, open_browser=not args.no_browser, allowed_hosts=set(args.allow_host or []),
          server_mode=args.server)
    return 0


def cmd_run(args) -> int:
    cmd_fetch(argparse.Namespace(company=None, tier=args.tier))
    cmd_score(args)
    ns = argparse.Namespace(min=args.min, all=False, status=None, new=False, region=None, archetype=None,
                            hide_visa=False, limit=200, md=str(config.OUTPUT_DIR / "jobs.md"), csv=None)
    return cmd_list(ns)


# ------------------------------------------------------------------ main
def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="jobhunt", description="LA / Irvine 金融相关求职流水线")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="检查招聘接口配置").set_defaults(func=cmd_check)

    f = sub.add_parser("fetch", help="抓取职位")
    f.add_argument("-c", "--company", nargs="*", help="只抓这些公司（companies.yaml 的 key）")
    f.add_argument("--tier", type=int, help="只抓 tier <= N 的公司")
    f.set_defaults(func=cmd_fetch)

    sub.add_parser("score", help="打分").set_defaults(func=cmd_score)

    ls = sub.add_parser("list", help="看排名")
    ls.add_argument("--min", type=float, default=40)
    ls.add_argument("--all", action="store_true", help="包括被过滤掉的")
    ls.add_argument("--status", choices=STATUSES)
    ls.add_argument("--new", action="store_true", help="只看还没处理过的")
    ls.add_argument("--region", help="例如 OC,LA")
    ls.add_argument("--archetype")
    ls.add_argument("--hide-visa", action="store_true", help="隐藏 JD 明确不担保的")
    ls.add_argument("--limit", type=int, default=50)
    ls.add_argument("--md", help="导出 Markdown 路径")
    ls.add_argument("--csv", help="导出 CSV 路径")
    ls.set_defaults(func=cmd_list)

    sh = sub.add_parser("show", help="看职位详情和打分理由")
    sh.add_argument("uid")
    sh.add_argument("--jd", action="store_true", help="同时打印 JD 全文")
    sh.set_defaults(func=cmd_show)

    b = sub.add_parser("base", help="生成各方向基础简历")
    b.add_argument("-a", "--archetype", default="all")
    b.add_argument("--no-pdf", action="store_true")
    b.set_defaults(func=cmd_base)

    t = sub.add_parser("tailor", help="针对职位定制简历")
    t.add_argument("uid", nargs="?")
    t.add_argument("--jd-file", help="手动粘贴的 JD 文本文件")
    t.add_argument("--company")
    t.add_argument("--title")
    t.add_argument("--location")
    t.add_argument("--url")
    t.add_argument("--no-pdf", action="store_true")
    t.set_defaults(func=cmd_tailor)

    a = sub.add_parser("apply", help="打开申请页并预填（你自己点提交）")
    a.add_argument("uid")
    a.add_argument("--resume", help="指定简历 PDF")
    a.set_defaults(func=cmd_apply)

    s = sub.add_parser("status", help="更新投递状态")
    s.add_argument("uid")
    s.add_argument("status", choices=STATUSES)
    s.add_argument("--note")
    s.set_defaults(func=cmd_status)

    sub.add_parser("validate", help="校验经历素材库").set_defaults(func=cmd_validate)

    w = sub.add_parser("web", help="打开本地可视化网站（或导出单文件快照）")
    w.add_argument("--port", type=int, default=8765)
    w.add_argument("--no-browser", action="store_true", help="不自动打开浏览器")
    w.add_argument("--export", help="导出单文件 HTML 快照到这个路径（不启动服务）")
    w.add_argument("--artifact", action="store_true", help="导出不带 <html>/<head> 外壳的版本（发布成 Claude Artifact 用）")
    w.add_argument("--no-jobs", action="store_true", help="导出时不包含职位数据")
    w.add_argument("--server", action="store_true", help="服务器模式：不开浏览器、关闭预填申请（配合 nginx 反代，见 deploy/）")
    w.add_argument("--allow-host", action="append", help="允许的域名（nginx 反代时填你的域名，可重复）")
    w.set_defaults(func=cmd_web)

    r = sub.add_parser("run", help="一条龙：fetch → score → 导出 output/jobs.md")
    r.add_argument("--tier", type=int)
    r.add_argument("--min", type=float, default=40)
    r.set_defaults(func=cmd_run)
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.cmd == "tailor" and not (args.uid or args.jd_file):
        sys.exit("tailor 需要 UID 或 --jd-file")
    return args.func(args) or 0


if __name__ == "__main__":
    raise SystemExit(main())
