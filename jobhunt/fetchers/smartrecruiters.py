"""SmartRecruiters 公开 Posting API（Experian 用它）。

列表：GET https://api.smartrecruiters.com/v1/companies/{id}/postings?limit=100&offset=N
      返回 {totalFound, content: [{id, name, location{city, region, country, remote, fullLocation},
            releasedDate, department{label}, experienceLevel{label}}]}
详情：GET https://api.smartrecruiters.com/v1/companies/{id}/postings/{postingId}
      返回 {jobAd: {sections: {jobDescription{text}, qualifications{text}, additionalInformation{text}}},
            postingUrl, applyUrl}

companies.yaml：ats: {type: smartrecruiters, company_id: Experian, country: us}
"""
from __future__ import annotations

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

API = "https://api.smartrecruiters.com/v1/companies/{cid}/postings"
PAGE = 100
MAX_POSTINGS = 2000


def location_string(loc: dict) -> str:
    if not loc:
        return ""
    if loc.get("fullLocation"):
        text = loc["fullLocation"]
    else:
        text = ", ".join(x for x in (loc.get("city"), loc.get("region"), (loc.get("country") or "").upper()) if x)
    if loc.get("remote"):
        text = f"Remote - {text}" if text else "Remote"
    return text


def parse_listing(item: dict, company: CompanyConfig) -> Job:
    cid = company.ats["company_id"]
    loc = item.get("location") or {}
    return Job(
        company_key=company.key,
        company=company.name,
        source="smartrecruiters",
        source_id=str(item.get("id")),
        title=(item.get("name") or "").strip(),
        url=f"https://jobs.smartrecruiters.com/{cid}/{item.get('id')}",
        locations=[location_string(loc)] if loc else [],
        department=(item.get("department") or {}).get("label"),
        posted_at=item.get("releasedDate"),
        remote=bool(loc.get("remote")) if loc else None,
    )


def apply_detail(job: Job, detail: dict) -> Job:
    sections = ((detail.get("jobAd") or {}).get("sections")) or {}
    parts = []
    for key in ("jobDescription", "qualifications", "additionalInformation"):
        sec = sections.get(key) or {}
        if sec.get("text"):
            parts.append(f"{sec.get('title') or ''}\n{html_to_text(sec['text'])}".strip())
    job.description = "\n\n".join(parts)
    job.url = detail.get("postingUrl") or job.url
    job.apply_url = detail.get("applyUrl") or job.url
    return job


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    cid = company.ats["company_id"]
    params = {"limit": PAGE}
    if company.ats.get("country"):
        params["country"] = company.ats["country"]
    jobs = []
    offset = 0
    while offset < MAX_POSTINGS:
        data = http.get_json(API.format(cid=cid), params={**params, "offset": offset})
        content = data.get("content") or []
        for item in content:
            job = parse_listing(item, company)
            if prefilter(job.title, job.locations):
                detail = http.get_json(f"{API.format(cid=cid)}/{item.get('id')}")
                jobs.append(apply_detail(job, detail))
        offset += PAGE
        if not content or offset >= (data.get("totalFound") or 0):
            break
    return jobs
