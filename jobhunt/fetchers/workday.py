"""Workday 公开职位接口（CXS）。PIMCO / Capital Group / Pacific Life 都用它。

列表：POST https://{host}/wday/cxs/{tenant}/{site}/jobs
      body {"appliedFacets": {}, "limit": 20, "offset": N, "searchText": "..."}
      返回 {"total": N, "jobPostings": [{title, externalPath, locationsText, postedOn, bulletFields}]}
      （很多租户只在 offset=0 那页返回 total）
详情：GET  https://{host}/wday/cxs/{tenant}/{site}{externalPath}
      返回 {"jobPostingInfo": {title, jobDescription(HTML), location, additionalLocations,
            externalUrl, jobReqId, startDate, timeType, remoteType}}

companies.yaml 配置：
  ats: {type: workday, host: pimco.wd1.myworkdayjobs.com, tenant: pimco, site: pimco-careers}
  search_terms: [software, quant, data]   # 可选：大公司职位多时只搜这些词
"""
from __future__ import annotations

from ..config import CompanyConfig
from ..http import Http
from ..location import is_unresolved
from ..models import Job
from ..text import html_to_text

PAGE = 20
MAX_POSTINGS = 1000


def list_postings(http: Http, host: str, tenant: str, site: str, search_text: str = "") -> list[dict]:
    url = f"https://{host}/wday/cxs/{tenant}/{site}/jobs"
    postings: list[dict] = []
    total = None
    offset = 0
    while offset < MAX_POSTINGS:
        data = http.post_json(url, {"appliedFacets": {}, "limit": PAGE, "offset": offset, "searchText": search_text})
        page = data.get("jobPostings") or []
        if total is None:
            total = data.get("total") or 0
        postings.extend(page)
        offset += PAGE
        if not page or offset >= total:
            break
    return postings


def parse_detail(detail: dict, posting: dict, company: CompanyConfig, host: str, site: str) -> Job:
    info = detail.get("jobPostingInfo") or {}
    locs = [info["location"]] if info.get("location") else []
    for extra in info.get("additionalLocations") or []:
        if extra and extra not in locs:
            locs.append(extra)
    if not locs and posting.get("locationsText"):
        locs = [posting["locationsText"]]
    path = posting.get("externalPath") or ""
    url = info.get("externalUrl") or f"https://{host}/en-US/{site}{path}"
    remote_type = (info.get("remoteType") or "").lower()
    return Job(
        company_key=company.key,
        company=company.name,
        source="workday",
        source_id=str(info.get("jobReqId") or (posting.get("bulletFields") or [path])[0]),
        title=(info.get("title") or posting.get("title") or "").strip(),
        url=url,
        apply_url=url.rstrip("/") + "/apply" if url else None,
        locations=locs,
        description=html_to_text(info.get("jobDescription")),
        posted_at=info.get("startDate") or posting.get("postedOn"),
        remote=True if "remote" in remote_type else None,
    )


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    host, tenant, site = company.ats["host"], company.ats["tenant"], company.ats["site"]
    terms = company.search_terms or [""]
    seen: dict[str, dict] = {}
    for term in terms:
        for p in list_postings(http, host, tenant, site, term):
            seen.setdefault(p.get("externalPath") or p.get("title"), p)

    jobs = []
    for path, posting in seen.items():
        loc_text = posting.get("locationsText") or ""
        locs = [] if is_unresolved([loc_text]) else [loc_text]
        # 列表页先粗筛（「2 Locations」这种要看详情才知道，先放行）
        if not prefilter(posting.get("title") or "", locs):
            continue
        detail = http.get_json(f"https://{host}/wday/cxs/{tenant}/{site}{posting.get('externalPath')}")
        job = parse_detail(detail, posting, company, host, site)
        if prefilter(job.title, job.locations):
            jobs.append(job)
    return jobs
