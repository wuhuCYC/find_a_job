"""命令行和网站共用的动作：生成基础简历、定制简历、找某个职位的简历文件。"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

from . import config
from .bank import load_bank
from .models import Job
from .store import Store


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:60]


def render_base(archetypes: list[str] | None = None, render_pdf: bool = True) -> list[dict]:
    from .resume import select_base, write_and_render

    bank, profile = load_bank(), config.load_profile()
    out = config.OUTPUT_DIR / "base"
    results = []
    for a in archetypes or list(config.load_archetypes()):
        files = write_and_render(select_base(bank, a), bank, profile, out, f"resume_{a}", render_pdf=render_pdf)
        results.append({"archetype": a, **files})
    return results


def tailor_job(job: Job, store: Store | None = None, render_pdf: bool = True) -> dict:
    """调用 Claude 定制简历 → 渲染 PDF → 写差距报告；非手动职位同时把状态改成 tailored。"""
    from .resume import write_and_render
    from .tailor import report_markdown, tailor

    bank, profile, search = load_bank(), config.load_profile(), config.load_search()
    outcome = tailor(job, bank, search.get("skill_vocabulary") or {})
    out = config.OUTPUT_DIR / "tailored" / f"{date.today().isoformat()}_{slug(job.company)}_{slug(job.title)}"
    files = write_and_render(outcome.plan, bank, profile, out, "resume", render_pdf=render_pdf)
    report = out / "report.md"
    report.write_text(report_markdown(job, outcome, files), encoding="utf-8")
    if store is not None and job.source != "manual":
        store.set_status(job.uid, "tailored", resume_path=str(files["pdf"] or files["yaml"]))
    return {**files, "report": report, "warnings": outcome.warnings, "out_dir": out}


def resume_for(store: Store, uid: str) -> Path | None:
    """这个职位最近一次定制出的 PDF（没有就返回 None）。"""
    row = store.conn.execute("SELECT resume_path FROM applications WHERE uid=?", (uid,)).fetchone()
    if row and row["resume_path"] and row["resume_path"].endswith(".pdf"):
        path = Path(row["resume_path"])
        return path if path.exists() else None
    return None


def make_scorer(companies=None):
    from .scoring import Scorer

    bank = load_bank()
    return Scorer(
        config.load_archetypes(),
        config.load_search(),
        config.load_profile(),
        [s.model_dump() for s in bank.skills],
        companies if companies is not None else config.load_companies(),
    )


def fetch_all(keys: list[str] | None = None, tier: int | None = None, log=print) -> int:
    """抓取职位（一家失败不影响其他家），返回新增职位数。"""
    from .fetchers import fetch_company
    from .http import Http

    all_companies = config.load_companies()
    companies = [c for c in all_companies if (not keys or c.key in keys) and (tier is None or c.tier <= tier)]
    scorer = make_scorer(all_companies)
    store, http = Store(), Http()
    total_new = 0
    try:
        for c in companies:
            if not c.enabled or c.ats_type == "manual":
                continue
            try:
                jobs = fetch_company(c, http, prefilter=scorer.prefilter)
            except Exception as exc:  # noqa: BLE001 —— 一家失败不影响其他家
                store.log_fetch(c.key, False, error=str(exc)[:500])
                log(f"  ✗ {c.name}: {str(exc)[:150]}")
                continue
            new, gone = store.upsert_jobs(c.key, jobs)
            store.log_fetch(c.key, True, n_jobs=len(jobs))
            total_new += new
            log(f"  ✓ {c.name}: {len(jobs)} 个相关职位（新增 {new}，下架 {gone}）")
    finally:
        store.close()
    return total_new


def score_all() -> tuple[int, int]:
    """给所有在招职位重新打分，返回 (总数, 进入候选数)。"""
    store, scorer = Store(), make_scorer()
    try:
        jobs = store.active_jobs()
        kept = 0
        for job in jobs:
            result = scorer.score(job)
            store.save_score(job.uid, result)
            kept += 0 if result.excluded else 1
        return len(jobs), kept
    finally:
        store.close()
