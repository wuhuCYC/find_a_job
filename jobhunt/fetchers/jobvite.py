"""Jobvite 招聘页（loanDepot 用它）—— 实验性，解析 HTML 列表。

列表页：https://jobs.jobvite.com/{company}/jobs
每行：<td class="jv-job-list-name"><a href="/{company}/job/{id}">Title</a></td>
      <td class="jv-job-list-location">City, State</td>

companies.yaml：ats: {type: jobvite, company: loandepot}
"""
from __future__ import annotations

import html
import re

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

_ROW = re.compile(
    r'<a[^>]+href="(?P<href>/[^"/]+/job/(?P<id>[A-Za-z0-9]+))"[^>]*>(?P<title>.*?)</a>'
    r'(?P<rest>.*?)(?=<a[^>]+href="/[^"/]+/job/|$)',
    re.S | re.I,
)
_LOC = re.compile(r'class="[^"]*jv-job-list-location[^"]*"[^>]*>(.*?)</td>', re.S | re.I)


class ParseError(RuntimeError):
    pass


def parse_list(page_html: str) -> list[dict]:
    out = []
    for m in _ROW.finditer(page_html):
        if any(o["id"] == m.group("id") for o in out):
            continue
        loc_m = _LOC.search(m.group("rest"))
        out.append({
            "id": m.group("id"),
            "title": html.unescape(html_to_text(m.group("title"))).strip(),
            "url": "https://jobs.jobvite.com" + m.group("href"),
            "location": html_to_text(loc_m.group(1)).replace("\n", " ").strip() if loc_m else "",
        })
    return out


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    slug = company.ats["company"]
    listings = parse_list(http.get_text(f"https://jobs.jobvite.com/{slug}/jobs"))
    if not listings:
        raise ParseError(f"Jobvite 页面没解析出职位，请手动打开 https://jobs.jobvite.com/{slug}/jobs 查看")
    jobs = []
    for item in listings:
        locs = [item["location"]] if item["location"] else []
        if not prefilter(item["title"], locs):
            continue
        detail = http.get_text(item["url"])
        jobs.append(
            Job(
                company_key=company.key,
                company=company.name,
                source="jobvite",
                source_id=item["id"],
                title=item["title"],
                url=item["url"],
                apply_url=item["url"] + "/apply",
                locations=locs,
                description=html_to_text(detail)[:20000],
            )
        )
    return jobs
