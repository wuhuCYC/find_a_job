"""防编造守卫：改写后的简历内容里，数字和技术栈都必须能在原始事实里找到。

这是整个定制流程最重要的一道闸：LLM 可以换措辞、调顺序，但不能多一个数字、多一个技术。
"""
from __future__ import annotations

import re

_THOUSANDS = re.compile(r"(?<=\d),(?=\d{3}\b)")
# 前面紧挨字母的数字不算（CS2、L1/L2、EECS215 这类是名字的一部分）
_NUMBER = re.compile(r"(?<![A-Za-z\d.])\d+(?:\.\d+)?")


def numbers_in(text: str) -> set[float]:
    """抽出文本里的所有数字（去千分位；46.0 和 46 视为同一个数）。"""
    cleaned = _THOUSANDS.sub("", text or "")
    return {float(m.group(0)) for m in _NUMBER.finditer(cleaned)}


def check_numbers(candidate: str, allowed_texts: list[str]) -> list[str]:
    allowed: set[float] = set()
    for t in allowed_texts:
        allowed |= numbers_in(t)
    extra = sorted(numbers_in(candidate) - allowed)
    return [f"数字 {n:g} 在原始事实里找不到" for n in extra]


# 「数字 + 单位」：最容易被编造的是「N years」「N%」「Nx」「N users」这类说法。
# 只看数字的话，"5 years of experience" 里的 5 可能碰巧在别处出现（5,000+ stocks），所以要连单位一起比。
_QUANTITY = re.compile(
    r"(?<![A-Za-z\d.])(\d+(?:\.\d+)?)\s*\+?\s*[-–]?\s*"
    r"(years?|yrs?|months?|weeks?|days?|hours?|minutes?|seconds?|%|percent|percentage points?|x|×|"
    r"users?|customers?|clients?)(?![A-Za-z])",
    re.I,
)
_UNIT_ALIASES = {"yr": "year", "yrs": "year", "percent": "%", "percentage point": "pp", "percentage points": "pp",
                 "×": "x"}


def quantities_in(text: str) -> set[tuple[float, str]]:
    cleaned = _THOUSANDS.sub("", text or "")
    out = set()
    for m in _QUANTITY.finditer(cleaned):
        unit = m.group(2).lower()
        unit = _UNIT_ALIASES.get(unit, unit)
        if unit.endswith("s") and unit not in ("%", "pp", "x"):
            unit = unit[:-1]
        out.add((float(m.group(1)), unit))
    return out


def check_quantities(candidate: str, allowed_texts: list[str]) -> list[str]:
    allowed: set[tuple[float, str]] = set()
    for t in allowed_texts:
        allowed |= quantities_in(t)
    extra = sorted(quantities_in(candidate) - allowed)
    return [f"说法「{v:g} {u}」在原始事实里找不到" for v, u in extra]


def check_claims(candidate: str, allowed_texts: list[str]) -> list[str]:
    """数字守卫 + 数量说法守卫。"""
    return check_numbers(candidate, allowed_texts) + check_quantities(candidate, allowed_texts)


def skills_in(text: str, vocabulary: dict[str, list[re.Pattern]]) -> set[str]:
    return {name for name, pats in vocabulary.items() if any(p.search(text or "") for p in pats)}


def check_skills(candidate: str, allowed_texts: list[str], stack: list[str],
                 vocabulary: dict[str, list[re.Pattern]]) -> list[str]:
    allowed = skills_in(" \n".join(allowed_texts + stack), vocabulary)
    allowed |= {s for s in vocabulary if s.lower() in {x.lower() for x in stack}}
    extra = sorted(skills_in(candidate, vocabulary) - allowed)
    return [f"技术 {s} 不在这段经历的技术栈/事实里" for s in extra]


def compile_vocabulary(raw: dict[str, list[str]]) -> dict[str, list[re.Pattern]]:
    return {name: [re.compile(a, re.I) for a in aliases] for name, aliases in (raw or {}).items()}
