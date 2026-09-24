"""Ashby 公开 Job Board API。

GET https://api.ashbyhq.com/posting-api/job-board/{org}?includeCompensation=true
返回 {"jobs": [{id, title, location, secondaryLocations[{location}], isRemote, workplaceType,
isListed, department, team, descriptionPlain, descriptionHtml, jobUrl, applyUrl, publishedAt,
compensation{compensationTierSummary}}]}
"""
from __future__ import annotations

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

API = "https://api.ashbyhq.com/posting-api/job-board/{org}"


def parse(data: dict, company: CompanyConfig) -> list[Job]:
    jobs = []
    for j in data.get("jobs") or []:
        if j.get("isListed") is False:
            continue
        locs = [j["location"]] if j.get("location") else []
        for sec in j.get("secondaryLocations") or []:
            loc = sec.get("location") if isinstance(sec, dict) else sec
            if loc and loc not in locs:
                locs.append(loc)
        comp = j.get("compensation") or {}
        salary = comp.get("compensationTierSummary") or comp.get("scrapeableCompensationSalarySummary")
        workplace = (j.get("workplaceType") or "").lower()
        remote = j.get("isRemote")
        if remote is None and workplace:
            remote = workplace == "remote"
        jobs.append(
            Job(
                company_key=company.key,
                company=company.name,
                source="ashby",
                source_id=str(j.get("id")),
                title=(j.get("title") or "").strip(),
                url=j.get("jobUrl") or "",
                apply_url=j.get("applyUrl") or j.get("jobUrl"),
                locations=locs,
                description=j.get("descriptionPlain") or html_to_text(j.get("descriptionHtml")),
                department=j.get("department") or j.get("team"),
                posted_at=j.get("publishedAt"),
                remote=remote,
                salary=salary,
            )
        )
    return jobs


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    org = company.ats["org"]
    data = http.get_json(API.format(org=org), params={"includeCompensation": "true"})
    return [j for j in parse(data, company) if prefilter(j.title, j.locations)]
