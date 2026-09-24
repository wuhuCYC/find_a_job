"""Lever 公开 Postings API。

GET https://api.lever.co/v0/postings/{site}?mode=json
返回职位数组：{id, text, categories{location, allLocations, team, department, commitment},
descriptionPlain, lists[{text, content}], additionalPlain, hostedUrl, applyUrl, workplaceType,
createdAt(ms), salaryRange{min,max,currency,interval}}
"""
from __future__ import annotations

from datetime import datetime, timezone

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

API = "https://api.lever.co/v0/postings/{site}"


def _salary(p: dict) -> str | None:
    sr = p.get("salaryRange") or {}
    if sr.get("min") or sr.get("max"):
        cur = sr.get("currency") or "USD"
        interval = (sr.get("interval") or "").replace("-", " ")

        def fmt(v):
            return f"{v:,.0f}" if isinstance(v, (int, float)) else "?"

        return f"{cur} {fmt(sr.get('min'))}–{fmt(sr.get('max'))} {interval}".strip()
    return p.get("salaryDescriptionPlain") or None


def parse(data: list, company: CompanyConfig) -> list[Job]:
    jobs = []
    for p in data or []:
        cats = p.get("categories") or {}
        locs = list(cats.get("allLocations") or [])
        if cats.get("location") and cats["location"] not in locs:
            locs.insert(0, cats["location"])
        parts = [p.get("descriptionPlain") or html_to_text(p.get("description"))]
        for block in p.get("lists") or []:
            parts.append(f"{block.get('text', '')}\n{html_to_text(block.get('content'))}")
        parts.append(p.get("additionalPlain") or html_to_text(p.get("additional")))
        created = p.get("createdAt")
        posted = (
            datetime.fromtimestamp(created / 1000, tz=timezone.utc).date().isoformat()
            if isinstance(created, (int, float))
            else None
        )
        workplace = (p.get("workplaceType") or "").lower()
        jobs.append(
            Job(
                company_key=company.key,
                company=company.name,
                source="lever",
                source_id=str(p.get("id")),
                title=(p.get("text") or "").strip(),
                url=p.get("hostedUrl") or "",
                apply_url=p.get("applyUrl"),
                locations=locs,
                description="\n\n".join(x for x in parts if x).strip(),
                department=cats.get("team") or cats.get("department"),
                posted_at=posted,
                remote=True if workplace == "remote" else (False if workplace in ("onsite", "on-site") else None),
                salary=_salary(p),
            )
        )
    return jobs


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    site = company.ats["site"]
    data = http.get_json(API.format(site=site), params={"mode": "json"})
    return [j for j in parse(data, company) if prefilter(j.title, j.locations)]
