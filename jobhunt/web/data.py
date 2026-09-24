"""网站数据：把配置、素材库、战略、职位库拼成一个 JSON payload（本地服务和单文件快照共用）。"""
from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone

from .. import config
from ..bank import load_bank
from ..config import CompanyConfig
from ..models import Job
from ..resume import select_base
from ..store import Store

# 地图落点（纬度, 经度）。先匹配更具体的地名，最后才是 "Los Angeles"
CITIES: dict[str, tuple[float, float, str]] = {
    "Century City": (34.056, -118.417, "LA"),
    "Culver City": (34.021, -118.396, "LA"),
    "Santa Monica": (34.019, -118.491, "LA"),
    "Westlake Village": (34.146, -118.806, "LA"),
    "Woodland Hills": (34.168, -118.605, "LA"),
    "Sherman Oaks": (34.151, -118.449, "LA"),
    "Burbank": (34.181, -118.309, "LA"),
    "Pasadena": (34.148, -118.144, "LA"),
    "Torrance": (33.836, -118.341, "LA"),
    "Newport Beach": (33.615, -117.875, "OC"),
    "Costa Mesa": (33.664, -117.912, "OC"),
    "Santa Ana": (33.745, -117.868, "OC"),
    "Irvine": (33.684, -117.826, "OC"),
    "Los Angeles": (34.050, -118.250, "LA"),
}
# 不在 LA/OC 地图上的地区。湾区 / 圣地亚哥先判断（"San Francisco / Santa Monica" 以湾区为准），
# 远程 / 外州最后判断（"Irvine, CA (remote-first)" 仍然落在 Irvine）
OFF_MAP_FIRST = [("San Diego", "SD"), ("Berkeley", "BAY"), ("San Francisco", "BAY"), ("Menlo Park", "BAY"),
                 ("San Mateo", "BAY"), ("Mountain View", "BAY")]
OFF_MAP_LAST = [("Remote", "REMOTE"), ("New York", "REMOTE")]
GROUPS = {
    "buy_side": {"asset_manager", "quant_hedge_fund", "hedge_fund", "prop_trading", "broker_dealer", "investment_bank"},
    "fintech": {"fintech", "payments", "lending_credit", "credit_data", "bank", "insurance", "crypto", "prediction_market"},
    "market": {"marketplace", "game_economy"},
}
GROUP_LABELS = {"buy_side": "买方 / 交易", "fintech": "金融科技 / 信贷 / 银行", "market": "交易市场 / 游戏经济"}
ARCHETYPE_ORDER = ["quant_dev", "investment_analytics", "fintech_swe", "risk_data", "marketplace_econ",
                   "quant_research", "trading_systems"]


def company_place(c: CompanyConfig) -> dict:
    """公司 → 地图位置。返回 {city, region, lat, lon}（不在地图上的 lat/lon 为 None）。"""
    if c.map_city and c.map_city in CITIES:
        lat, lon, region = CITIES[c.map_city]
        return {"city": c.map_city, "region": region, "lat": lat, "lon": lon}
    hq = (c.hq or "").lower()
    for name, region in OFF_MAP_FIRST:
        if name.lower() in hq:
            return {"city": name, "region": region, "lat": None, "lon": None}
    for name, (lat, lon, region) in CITIES.items():
        if name.lower() in hq:
            return {"city": name, "region": region, "lat": lat, "lon": lon}
    for name, region in OFF_MAP_LAST:
        if name.lower() in hq:
            return {"city": name, "region": region, "lat": None, "lon": None}
    return {"city": c.hq, "region": "OTHER", "lat": None, "lon": None}


def company_group(c: CompanyConfig) -> str:
    if c.group in GROUPS:
        return c.group
    return next((g for g, cats in GROUPS.items() if c.category in cats), "fintech")


def _as_date(value):
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(str(value))
    except ValueError:
        return None


def personal_timeline(profile: dict) -> dict | None:
    """根据 private/profile.yaml 的日期算 OPT 关键节点（规则见 docs/VISA_NOTES.md；不是法律意见）。"""
    auth = profile.get("work_authorization") or {}
    end = _as_date(auth.get("program_end_date"))
    if not end:
        return None
    filed = _as_date(auth.get("opt_filed_date"))
    ead = _as_date(auth.get("ead_start_date"))
    deadline = end + timedelta(days=60)
    events = [
        {"date": end.isoformat(), "kind": "past", "note": "项目结束（I-20 上的日期）"},
        {"date": (end - timedelta(days=90)).isoformat(), "kind": "info", "note": "OPT 最早可以提交的日子（项目结束前 90 天）"},
    ]
    if filed:
        events.append({"date": filed.isoformat(), "kind": "done", "note": "已提交 I-765（OPT）"})
    if filed:
        events.append({"date": deadline.isoformat(), "kind": "info",
                       "note": "60 天宽限期的最后一天（OPT 已提交）；申请的 EAD 开始日最晚只能是这天"})
    else:
        events.append({"date": deadline.isoformat(), "kind": "deadline",
                       "note": "OPT 提交截止 + 60 天宽限期结束；EAD 开始日最晚只能选到这天（还没记录提交日期）"})
    if ead:
        events.append({"date": ead.isoformat(), "kind": "ead", "note": "EAD 开始：可以合法工作，90 天失业计时从这天算"})
        events.append({"date": (ead + timedelta(days=90)).isoformat(), "kind": "deadline",
                       "note": "如果一直没工作，90 天失业上限用完的日子（找到工作 10 天内要报告）"})
        events.append({"date": (ead + timedelta(days=365) - timedelta(days=90)).isoformat(), "kind": "info",
                       "note": "最早可以申请 STEM OPT 延期（OPT 到期前 90 天；需要 E-Verify 雇主）"})
    else:
        latest = deadline + timedelta(days=90)
        events.append({"date": latest.isoformat(), "kind": "info",
                       "note": f"参考：如果 EAD 从 {deadline.isoformat()} 开始，90 天失业上限用到这天；"
                               "批准得更晚的话 EAD 从批准日开始，这个日子也往后推（拿到卡后在 profile 填 ead_start_date）"})
    lottery_year = end.year if end.month < 3 else end.year + 1
    events.append({"date": f"{lottery_year}-03-10", "kind": "info",
                   "note": "H-1B 抽签注册（大约 3 月），需要雇主在这之前愿意为你注册"})
    events.sort(key=lambda e: e["date"])
    return {"program_end": end.isoformat(), "opt_deadline": deadline.isoformat(),
            "ead_start": ead.isoformat() if ead else None, "filed": filed.isoformat() if filed else None,
            "events": events}


def _bank_payload(bank) -> dict:
    return {
        "summaries": bank.summaries,
        "skills": [s.model_dump() for s in bank.skills],
        "entries": [
            {
                "id": e.id, "kind": e.kind, "title": e.title, "role": e.role, "start": str(e.start or ""),
                "end": str(e.end or ""), "stack": e.stack,
                "bullets": [{"id": b.id, "label": b.label or b.id, "text": b.text, "weights": b.weights} for b in e.bullets],
            }
            for e in bank.entries
        ],
    }


def _plans(bank, archetypes: list[str]) -> dict:
    plans = {}
    for a in archetypes:
        plan = select_base(bank, a)
        plans[a] = [{"entry_id": pe.entry.id, "bullet_ids": pe.bullet_ids} for pe in plan.entries]
    return plans


def _job_row(row, detail: dict, include_description: bool) -> dict:
    out = {
        "uid": row["uid"], "company": row["company"], "company_key": row["company_key"], "title": row["title"],
        "url": row["url"], "locations": json.loads(row["locations"] or "[]"), "salary": row["salary"],
        "posted_at": row["posted_at"], "first_seen": row["first_seen"], "status": row["status"],
        "score": row["score"], "archetype": detail.get("archetype"), "regions": detail.get("regions", []),
        "seniority": detail.get("seniority"), "flags": detail.get("flags", []),
        "matched_skills": detail.get("matched_skills", []), "missing_skills": detail.get("missing_skills", []),
        "reasons": detail.get("reasons", []), "components": detail.get("components", {}),
    }
    if include_description:
        out["description"] = row["description"] or ""
    return out


def example_jobs() -> list[Job]:
    """快照里没有真实职位时，用来演示打分效果的示例（界面上会明确标成示例）。"""
    return [
        Job("pimco", "PIMCO", "example", "ex1", "Quantitative Developer", "https://www.pimco.com/us/en/about-us/careers",
            ["Newport Beach, CA"], description=(
                "Example posting. Build backtesting and signal research platforms in Python (pandas, NumPy) and SQL "
                "for systematic strategies; C++ a plus. 3+ years of experience. PIMCO participates in E-Verify.")),
        Job("capital_group", "Capital Group", "example", "ex2", "New Grad - Software Development Engineer I",
            "https://www.capitalgroup.com/about-us/careers.html", ["Irvine, CA"], description=(
                "Example posting. Java, Python, AWS and REST APIs for investment platforms used by portfolio managers.")),
        Job("acorns", "Acorns", "example", "ex3", "Software Engineer I, Recent Graduate", "https://jobs.ashbyhq.com/Acorns",
            ["Irvine, CA", "Remote - US"], description=(
                "Example posting. Backend services for investing and banking features. Python, PostgreSQL, AWS, APIs.")),
        Job("experian", "Experian", "example", "ex4", "Software Engineer - Xcelerator Program", "https://jobs.experian.com",
            ["Costa Mesa, CA, US"], description=(
                "Example posting. Java microservices and SQL on credit data. Candidates must be authorized to work in "
                "the US without sponsorship.")),
        Job("zest_ai", "Zest AI", "example", "ex5", "Machine Learning Engineer", "https://job-boards.greenhouse.io/zestai",
            ["Burbank, CA"], description=(
                "Example posting. Credit underwriting models with Python, XGBoost, feature engineering and model "
                "validation; SQL; lending experience a plus.")),
    ]


def _example_rows() -> list[dict]:
    from ..actions import make_scorer

    scorer = make_scorer()
    rows = []
    for job in example_jobs():
        r = scorer.score(job)
        rows.append({
            "uid": job.uid, "company": job.company, "company_key": job.company_key, "title": job.title,
            "url": job.url, "locations": job.locations, "salary": None, "posted_at": None, "first_seen": None,
            "status": "new", "score": r.score, "archetype": r.archetype, "regions": r.regions,
            "seniority": r.seniority, "flags": r.flags, "matched_skills": r.matched_skills,
            "missing_skills": r.missing_skills, "reasons": r.reasons, "components": r.components,
            "description": job.description, "example": True,
        })
    return sorted(rows, key=lambda x: -x["score"])


def build_payload(mode: str = "live", include_jobs: bool = True, include_descriptions: bool = False,
                  examples_if_empty: bool = False) -> dict:
    """mode: live（本地服务，可以操作）/ snapshot（单文件快照，只读）。"""
    bank = load_bank()
    archetypes_cfg = config.load_archetypes()
    archetypes = [a for a in ARCHETYPE_ORDER if a in archetypes_cfg] + [a for a in archetypes_cfg if a not in ARCHETYPE_ORDER]
    # YAML 会把 2026-09-24 解析成 date，统一转成字符串，前端直接用
    strategy = json.loads(json.dumps(config.load_yaml(config.ROOT / "docs" / "strategy.yaml") or {}, default=str))

    jobs, excluded, status_counts, per_company = [], 0, {}, {}
    db_path = config.DATA_DIR / "jobs.db"
    if include_jobs and db_path.exists():
        store = Store(db_path)
        try:
            for row in store.ranked(min_score=0, include_excluded=True):
                detail = json.loads(row["detail"])
                if detail.get("excluded"):
                    excluded += 1
                    continue
                jobs.append(_job_row(row, detail, include_descriptions))
            status_counts = store.status_counts()
        finally:
            store.close()
    for j in jobs:
        stats = per_company.setdefault(j["company_key"], {"open": 0, "best": 0.0})
        stats["open"] += 1
        stats["best"] = max(stats["best"], j["score"])
    examples = False
    if not jobs and examples_if_empty:
        jobs, examples = _example_rows(), True

    companies = []
    for c in config.load_companies():
        place = company_place(c)
        stats = per_company.get(c.key, {"open": 0, "best": None})
        companies.append({
            "key": c.key, "name": c.name, "tier": c.tier, "category": c.category, "group": company_group(c),
            "hq": c.hq, **place, "verified": c.verified, "ats": c.ats_type, "careers_url": c.careers_url,
            "notes": c.notes, "open_jobs": stats["open"], "best_score": stats["best"],
        })

    resumes = {}
    for a in archetypes:
        pdf = config.OUTPUT_DIR / "base" / f"resume_{a}.pdf"
        if mode == "live" and pdf.exists():
            resumes[a] = f"base/resume_{a}.pdf"

    return {
        "mode": mode,
        "personal": personal_timeline(config.load_profile()),
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "strategy": strategy,
        "archetypes": {a: {"label": archetypes_cfg[a].get("label"), "label_zh": archetypes_cfg[a].get("label_zh")}
                       for a in archetypes},
        "archetype_order": archetypes,
        "groups": GROUP_LABELS,
        "companies": companies,
        "bank": _bank_payload(bank),
        "plans": _plans(bank, archetypes),
        "resumes": resumes,
        "jobs": jobs,
        "jobs_excluded": excluded,
        "examples": examples,
        "status_counts": status_counts,
        "statuses": ["new", "shortlisted", "tailored", "prefilled", "applied", "oa", "interview", "offer",
                     "rejected", "skipped"],
    }
