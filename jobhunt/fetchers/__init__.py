"""各家 ATS 的抓取器。每个模块提供 fetch(company, http, prefilter) -> list[Job]。

prefilter(title, locations) -> bool：列表页就能判断的过滤（职级/职能/地区），
用来避免对明显不相关的职位再去请求详情页（Workday / SmartRecruiters / iCIMS 需要）。
"""
from __future__ import annotations

from typing import Callable

from ..config import CompanyConfig
from ..http import Http
from ..models import Job
from . import ashby, greenhouse, icims, jobvite, lever, smartrecruiters, workday

Prefilter = Callable[[str, list[str]], bool]

FETCHERS = {
    "greenhouse": greenhouse.fetch,
    "lever": lever.fetch,
    "ashby": ashby.fetch,
    "workday": workday.fetch,
    "smartrecruiters": smartrecruiters.fetch,
    "icims": icims.fetch,
    "jobvite": jobvite.fetch,
}


def fetch_company(company: CompanyConfig, http: Http, prefilter: Prefilter | None = None) -> list[Job]:
    fn = FETCHERS.get(company.ats_type)
    if fn is None:
        return []  # manual：只能手动去官网看
    return fn(company, http, prefilter or (lambda title, locs: True))
