"""职级判断（只看职位名）。"""
from __future__ import annotations

import re

_SENIOR = re.compile(
    r"\b(senior|sr\.?|staff|principal|lead|manager|mgr|director|head of|vp|vice president|chief|"
    r"distinguished|fellow|partner|managing director|executive|architect|supervisor)\b"
    r"|\b(iii|iv|v)\b|\b(engineer|developer|analyst|scientist)\s+(3|4|5)\b",
    re.I,
)
_INTERN = re.compile(r"\b(intern|internship|co-?op|summer (analyst|associate))\b", re.I)
_ENTRY = re.compile(
    r"\b(new grad(uate)?|graduate|entry[- ]level|junior|jr\.?|early career|university|campus|"
    r"rotation(al)?|associate|recent grad(uate)?|class of 20\d\d|20(26|27))\b"
    r"|\b(development|rotation(al)?|leadership|early talent|graduate|analyst|associate|technology)\s+program\b"
    r"|\b(engineer|developer|analyst|scientist)\s+(i|1)\b",
    re.I,
)
_MID = re.compile(r"\b(ii|2)\b", re.I)


def classify_seniority(title: str) -> str:
    """返回 senior / intern / entry / mid / unknown。"""
    t = title or ""
    if _INTERN.search(t):
        return "intern"
    if _SENIOR.search(t):
        # "Associate Director" 之类仍然是 senior；"Senior Associate" 也是 senior
        return "senior"
    if _ENTRY.search(t):
        return "entry"
    if _MID.search(t):
        return "mid"
    return "unknown"


_YEARS = re.compile(
    r"(\d{1,2})\s*\+?\s*(?:(?:-|–|to)\s*\d{1,2}\s*)?\+?\s*(?:years?|yrs?)\b[^.\n]{0,60}?\b(experience|exp\.)",
    re.I,
)
_MINIMUM_YEARS = re.compile(r"(?:minimum|at least)\s+(?:of\s+)?(\d{1,2})\s+(?:years?|yrs?)", re.I)


def min_years_required(text: str) -> int | None:
    """从 JD 里抽「N+ years of experience」的最小年限；抽不到返回 None。

    取所有匹配里最小的那个（JD 常写「3+ years Python, 5+ years preferred」）。
    """
    values = [int(m.group(1)) for m in _YEARS.finditer(text or "")]
    values += [int(m.group(1)) for m in _MINIMUM_YEARS.finditer(text or "")]
    values = [v for v in values if 0 < v <= 20]
    return min(values) if values else None
