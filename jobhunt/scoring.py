"""过滤 + 打分。所有规则来自 config/search.yaml 和 config/archetypes.yaml，结果带可读理由。"""
from __future__ import annotations

import re

from .config import CompanyConfig
from .location import classify_locations
from .models import Job, ScoreResult
from .seniority import classify_seniority, min_years_required

_CLASS_OF = re.compile(r"(?:graduating\s+class\s+of|class\s+of|graduating\s+in|graduation\s+(?:date\s+)?(?:in|between))\s+(?:\w+\s+)?(20\d\d)", re.I)


def required_grad_year(text: str) -> int | None:
    """JD 里限定的毕业年份（「Graduating class of 2027」）；只写了一个年份时才算限定。"""
    years = {int(m.group(1)) for m in _CLASS_OF.finditer(text or "")}
    return years.pop() if len(years) == 1 else None
from .text import compile_keyword

LEVEL_VALUE = {"expert": 1.0, "proficient": 0.85, "working": 0.6, "coursework": 0.3, "none": 0.0}
MATCHED_THRESHOLD = 0.5
# 跟「钱」直接相关的公司类别：金融科技后端方向在这些公司里天然成立
FINANCE_CATEGORIES = {
    "asset_manager", "quant_hedge_fund", "hedge_fund", "prop_trading", "broker_dealer", "investment_bank",
    "bank", "lending_credit", "credit_data", "insurance", "fintech", "payments", "crypto", "prediction_market",
}


def _level_value(level: str | None) -> float:
    return LEVEL_VALUE.get(str(level or "none").lower(), 0.0)


class Scorer:
    def __init__(
        self,
        archetypes: dict[str, dict],
        search: dict,
        profile: dict,
        skills: list[dict],
        companies: list[CompanyConfig] | None = None,
    ):
        self.search = search
        self.regions_pref: dict[str, float] = search.get("regions") or {}
        sen = search.get("seniority") or {}
        self.exclude_senior = sen.get("exclude_senior", True)
        prefs = profile.get("preferences") or {}
        # 毕业年份（从 program_end_date 取）：JD 限定「Class of 2027」而你是 2026 届时扣分
        end = str((profile.get("work_authorization") or {}).get("program_end_date") or "")
        self.grad_year = int(end[:4]) if end[:4].isdigit() else None
        self.include_internships = prefs.get("include_internships", sen.get("include_internships", False))
        self.seniority_scores = sen.get("scores") or {"entry": 10, "intern": 8, "unknown": 6, "mid": 4}
        self.weights = search.get("weights") or {"archetype": 40, "skills": 25, "location": 15, "seniority": 10, "company": 10}
        self.tier_scores = {int(k): v for k, v in (search.get("company_tier_scores") or {1: 10, 2: 6, 3: 3}).items()}
        self.exp_penalties = sorted(search.get("experience_penalty") or [], key=lambda x: -x["min_years"])
        self.visa_penalty = search.get("visa_blocker_penalty", 35)
        self.e_verify_bonus = search.get("e_verify_bonus", 2)
        auth = profile.get("work_authorization") or {}
        self.needs_sponsorship = bool(auth.get("requires_sponsorship_now") or auth.get("requires_sponsorship_future"))

        self.function_pats = [compile_keyword(k) for k in search.get("function_title_keywords") or []]
        self.exclude_pats = [compile_keyword(k) for k in search.get("exclude_title_keywords") or []]
        self.visa_pats = {
            flag: [compile_keyword(k) for k in kws] for flag, kws in (search.get("visa_phrases") or {}).items()
        }
        self.skill_pats = {
            name: [re.compile(a, re.I) for a in aliases] for name, aliases in (search.get("skill_vocabulary") or {}).items()
        }
        self.user_skills = {s["name"].lower(): _level_value(s.get("level")) for s in skills}

        self.archetypes = {}
        for key, spec in archetypes.items():
            self.archetypes[key] = {
                "title": {k: compile_keyword(k) for k in spec.get("title_keywords") or []},
                "desc": {k: compile_keyword(k) for k in spec.get("desc_keywords") or []},
            }
        priority = prefs.get("archetype_priority") or list(archetypes)
        self.archetype_pref = {a: max(0.6, 1.0 - 0.07 * i) for i, a in enumerate(priority)}
        self.companies = {c.key: c for c in companies or []}

    # ------------------------------------------------------------------ 过滤
    def title_ok(self, title: str) -> tuple[bool, str | None]:
        if any(p.search(title) for p in self.exclude_pats):
            return False, "非技术岗（职位名命中排除词）"
        if self.function_pats and not any(p.search(title) for p in self.function_pats):
            return False, "职能不相关（职位名没有技术/量化/金融关键词）"
        sen = classify_seniority(title)
        if sen == "senior" and self.exclude_senior:
            return False, "职级太高（Senior/Staff/Lead/Manager…）"
        if sen == "intern" and not self.include_internships:
            return False, "实习岗（profile 里没开 include_internships）"
        return True, None

    def location_ok(self, locations: list[str], remote: bool | None = None) -> tuple[bool, list[str]]:
        if not locations and remote is None:
            return True, []  # 没有地点信息：先放行，打分时标记
        regions = classify_locations(locations, remote)
        return any(r in self.regions_pref for r in regions), regions

    def prefilter(self, title: str, locations: list[str]) -> bool:
        """给抓取器用的列表页粗筛：不相关的就不去请求详情页了。"""
        ok, _ = self.title_ok(title)
        if not ok:
            return False
        loc_ok, _ = self.location_ok(locations)
        return loc_ok

    # ------------------------------------------------------------------ 打分
    def _archetype_scores(self, job: Job) -> tuple[dict[str, float], dict[str, list[str]]]:
        text = f"{job.title}\n{job.description}"
        company = self.companies.get(job.company_key)
        finance = bool(company and company.category in FINANCE_CATEGORIES)
        scores, hits = {}, {}
        for key, pats in self.archetypes.items():
            title_hits = [k for k, p in pats["title"].items() if p.search(job.title)]
            desc_hits = [k for k, p in pats["desc"].items() if p.search(text)]
            n_desc = len(desc_hits)
            if finance and key == "fintech_swe":
                n_desc += 2  # 在金融公司做工程本身就是「和钱打交道」
            raw = 0.6 * (1 if title_hits else 0) + 0.4 * min(n_desc, 8) / 8
            scores[key] = round(raw, 3)
            hits[key] = title_hits + desc_hits
        return scores, hits

    def _skills(self, job: Job) -> tuple[list[str], list[str]]:
        text = f"{job.title}\n{job.description}"
        required = [name for name, pats in self.skill_pats.items() if any(p.search(text) for p in pats)]
        matched = [s for s in required if self.user_skills.get(s.lower(), 0.0) >= MATCHED_THRESHOLD]
        missing = [s for s in required if self.user_skills.get(s.lower(), 0.0) < MATCHED_THRESHOLD]
        return matched, missing

    def _visa_flags(self, text: str) -> list[str]:
        return [flag for flag, pats in self.visa_pats.items() if any(p.search(text) for p in pats)]

    def score(self, job: Job) -> ScoreResult:
        reasons: list[str] = []
        flags: list[str] = []
        seniority = classify_seniority(job.title)

        ok, why = self.title_ok(job.title)
        loc_ok, regions = self.location_ok(job.locations, job.remote)
        excluded, exclude_reason = False, None
        if not ok:
            excluded, exclude_reason = True, why
        elif not loc_ok:
            excluded, exclude_reason = True, f"地区不在目标范围（{', '.join(job.locations) or '未知'}）"

        w = self.weights
        # 1) 方向
        arch_scores, arch_hits = self._archetype_scores(job)
        weighted = {k: v * self.archetype_pref.get(k, 0.6) for k, v in arch_scores.items()}
        best = max(weighted, key=weighted.get) if weighted else None
        arch_points = w["archetype"] * (weighted.get(best, 0.0) if best else 0.0)
        if best and arch_scores[best] > 0:
            reasons.append(f"方向 {best}：命中 {', '.join(arch_hits[best][:8]) or '（公司类别加成）'}")
        else:
            best = None
            reasons.append("方向：没有明显匹配的岗位方向")

        # 2) 技能
        matched, missing = self._skills(job)
        required = matched + missing
        if required:
            avg = sum(self.user_skills.get(s.lower(), 0.0) for s in required) / len(required)
            skill_points = w["skills"] * avg
            reasons.append(f"技能：会 {', '.join(matched) or '无'}；缺 {', '.join(missing) or '无'}")
        else:
            skill_points = w["skills"] * 0.5
            reasons.append("技能：JD 没列出可识别的技术栈")

        # 3) 地区
        if regions:
            pref = max((self.regions_pref.get(r, 0.0) for r in regions), default=0.0)
            reasons.append(f"地区：{'/'.join(regions)}（{'; '.join(job.locations)[:80]}）")
        else:
            pref = 0.3
            flags.append("location_unknown")
            reasons.append("地区：JD 没写地点，需要人工确认")
        loc_points = w["location"] * pref

        # 4) 职级 + 年限
        sen_points = w["seniority"] * self.seniority_scores.get(seniority, 6) / 10
        reasons.append(f"职级：{seniority}")
        penalty = 0.0
        years = min_years_required(job.description)
        if years is not None:
            for rule in self.exp_penalties:
                if years >= rule["min_years"]:
                    penalty += rule["penalty"]
                    flags.append(f"yoe>={years}")
                    reasons.append(f"经验要求：{years}+ 年（-{rule['penalty']}）")
                    break

        req_year = required_grad_year(job.description)
        if self.grad_year and req_year and req_year != self.grad_year:
            penalty += 25
            flags.append(f"class_of_{req_year}")
            reasons.append(f"⚠ 只招 {req_year} 届毕业生，你是 {self.grad_year} 届（-25）")

        # 5) 公司
        company = self.companies.get(job.company_key)
        tier = company.tier if company else 3
        comp_points = self.tier_scores.get(tier, 3)

        # 6) 签证
        visa_flags = self._visa_flags(f"{job.title}\n{job.description}")
        flags.extend(visa_flags)
        blockers = [f for f in visa_flags if f in ("no_sponsorship", "citizenship_required", "clearance")]
        if blockers:
            reasons.append(f"⚠ 签证：JD 出现 {', '.join(blockers)} 相关措辞，请读原文确认")
            if self.needs_sponsorship:
                penalty += self.visa_penalty
                flags.append("visa_blocker")
        else:
            reasons.append("签证：JD 没发现不担保措辞（不代表一定担保）")
        bonus = self.e_verify_bonus if "e_verify" in visa_flags else 0.0

        total = arch_points + skill_points + loc_points + sen_points + comp_points + bonus - penalty
        total = max(0.0, min(100.0, total))
        return ScoreResult(
            score=round(total, 1),
            archetype=best,
            archetype_scores=arch_scores,
            regions=regions,
            seniority=seniority,
            matched_skills=matched,
            missing_skills=missing,
            flags=sorted(set(flags)),
            reasons=reasons,
            excluded=excluded,
            exclude_reason=exclude_reason,
            components={
                "archetype": round(arch_points, 1),
                "skills": round(skill_points, 1),
                "location": round(loc_points, 1),
                "seniority": round(sen_points, 1),
                "company": round(float(comp_points), 1),
                "bonus": round(bonus, 1),
                "penalty": round(-penalty, 1),
            },
        )
