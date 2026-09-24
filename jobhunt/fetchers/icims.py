"""iCIMS 招聘门户（TCW / PennyMac / East West Bank 用它）—— 实验性。

iCIMS 没有公开 JSON 接口，这里解析搜索结果页 HTML：
  https://{portal}/jobs/search?ss=1&in_iframe=1&pr={page}
每条职位是一个 href 形如 /jobs/{id}/{slug}/job 的链接，后面跟着 Location 字段。
页面结构一变就可能解析不到，此时 fetch 会抛错提示你手动去官网看。

companies.yaml：ats: {type: icims, portal: careers-tcw.icims.com}
"""
from __future__ import annotations

import html
import re

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from ..text import html_to_text

MAX_PAGES = 15
_ANCHOR = re.compile(
    r'<a[^>]+href="(?P<href>(?:https?://[^"]+)?/jobs/(?P<id>\d+)/[^"/]+/job[^"]*)"[^>]*>(?P<inner>.*?)</a>',
    re.S | re.I,
)
_TITLE_ATTR = re.compile(r'title="(?:\d+\s*-\s*)?([^"]+)"', re.I)
_LOCATION = re.compile(r"Location[s]?\s*</span>\s*(?:<[^>]+>\s*)*([^<]{2,120})<", re.I)


class ParseError(RuntimeError):
    pass


def parse_search_page(page_html: str, portal: str) -> list[dict]:
    """返回 [{id, title, url, location}]。"""
    results: list[dict] = []
    matches = list(_ANCHOR.finditer(page_html))
    for i, m in enumerate(matches):
        job_id = m.group("id")
        if any(r["id"] == job_id for r in results):
            continue
        tag = page_html[m.start(): m.start() + 500]
        title_m = _TITLE_ATTR.search(tag.split(">", 1)[0])
        title = title_m.group(1) if title_m else html_to_text(m.group("inner"))
        title = re.sub(r"^\s*title\s*", "", html.unescape(title), flags=re.I).strip()
        # 这条职位到下一条职位之间的 HTML 里找 Location
        end = matches[i + 1].start() if i + 1 < len(matches) else len(page_html)
        loc_m = _LOCATION.search(page_html[m.end(): end])
        href = m.group("href")
        url = href if href.startswith("http") else f"https://{portal}{href}"
        results.append({
            "id": job_id,
            "title": title,
            "url": url.split("?")[0],
            "location": html.unescape(loc_m.group(1)).strip() if loc_m else "",
        })
    return results


def fetch(company: CompanyConfig, http: Http, prefilter) -> list[Job]:
    portal = company.ats["portal"]
    listings: list[dict] = []
    for page in range(MAX_PAGES):
        page_html = http.get_text(f"https://{portal}/jobs/search", params={"ss": 1, "in_iframe": 1, "pr": page})
        found = parse_search_page(page_html, portal)
        new = [f for f in found if all(f["id"] != x["id"] for x in listings)]
        if not new:
            break
        listings.extend(new)
    if not listings:
        raise ParseError(f"iCIMS 页面没解析出职位，可能改版了。请手动打开 https://{portal}/jobs/search 查看")

    jobs = []
    for item in listings:
        locs = [item["location"]] if item["location"] else []
        if not prefilter(item["title"], locs):
            continue
        detail_html = http.get_text(item["url"], params={"in_iframe": 1})
        jobs.append(
            Job(
                company_key=company.key,
                company=company.name,
                source="icims",
                source_id=item["id"],
                title=item["title"],
                url=item["url"],
                apply_url=item["url"],
                locations=locs,
                description=html_to_text(detail_html)[:20000],
            )
        )
    return jobs
