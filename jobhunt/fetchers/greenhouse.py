"""Greenhouse 公开 Job Board API。

GET https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true
返回 {"jobs": [{id, title, location{name}, offices[], departments[], absolute_url, content, updated_at}]}
content 是转义过的 HTML。
"""
from __future__ import annotations

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

API = "https://boards-api.greenhouse.io/v1/boards/{token}/jobs"


def parse(data: dict, company: CompanyConfig) -> list[Job]:
    jobs = []
    for j in data.get("jobs") or []:
        locs: list[str] = []
        name = (j.get("location") or {}).get("name")
        if name:
            locs.append(name)
        for office in j.get("offices") or []:
            loc = office.get("location") or office.get("name")
            if loc and loc not in locs:
                locs.append(loc)
        departments = [d.get("name") for d in j.get("departments") or [] if d.get("name")]
        jobs.append(
            Job(
                company_key=company.key,
                company=company.name,
                source="greenhouse",
                source_id=str(j.get("id")),
                title=(j.get("title") or "").strip(),
                url=j.get("absolute_url") or "",
                apply_url=j.get("absolute_url"),
                locations=locs,
                description=html_to_text(j.get("content")),
                department=", ".join(departments) or None,
                posted_at=j.get("first_published") or j.get("updated_at"),
                remote=any("remote" in loc.lower() for loc in locs) or None,
            )
        )
    return jobs


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    token = company.ats["token"]
    data = http.get_json(API.format(token=token), params={"content": "true"})
    return [j for j in parse(data, company) if prefilter(j.title, j.locations)]
