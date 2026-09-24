"""核心数据结构。"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Job:
    """一条职位（所有 ATS 抓回来的数据都统一成这个形状）。"""

    company_key: str            # companies.yaml 里的 key
    company: str                # 展示用公司名
    source: str                 # greenhouse / lever / ashby / workday / smartrecruiters / icims / jobvite
    source_id: str              # ATS 内部职位 id
    title: str
    url: str                    # 职位详情页
    locations: list[str] = field(default_factory=list)   # 原始地点字符串
    apply_url: str | None = None
    description: str = ""       # 纯文本 JD
    department: str | None = None
    posted_at: str | None = None
    remote: bool | None = None
    salary: str | None = None

    @property
    def uid(self) -> str:
        return f"{self.source}:{self.company_key}:{self.source_id}"


@dataclass
class ScoreResult:
    """打分结果：分数 + 可解释的理由。"""

    score: float
    archetype: str | None
    archetype_scores: dict[str, float]
    regions: list[str]
    seniority: str
    matched_skills: list[str]
    missing_skills: list[str]
    flags: list[str]
    reasons: list[str]
    excluded: bool = False
    exclude_reason: str | None = None
