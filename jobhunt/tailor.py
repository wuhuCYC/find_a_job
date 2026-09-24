"""针对具体 JD 定制简历：Claude 负责「挑选 + 改写措辞 + 找差距」，guard 负责「不许编」。

需要 ANTHROPIC_API_KEY（或 `ant auth login`）。模型默认 claude-opus-5，可用 JOBHUNT_MODEL 覆盖。
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal

import yaml
from pydantic import BaseModel, Field

from .bank import Bank
from .guard import check_claims, check_skills, compile_vocabulary
from .models import Job
from .resume import PlannedEntry, ResumePlan

MODEL = os.environ.get("JOBHUNT_MODEL", "claude-opus-5")
SHOWABLE = {"expert", "proficient", "working"}


class TailoredBullet(BaseModel):
    bullet_id: str = Field(description="素材库里原 bullet 的 id，必须原样照抄")
    text: str = Field(description="改写后的 bullet（英文，一到两行，数字必须和原文一致）")


class TailoredEntry(BaseModel):
    entry_id: str
    bullets: list[TailoredBullet]


class Gap(BaseModel):
    requirement: str
    severity: Literal["high", "medium", "low"]
    how_to_close: str = Field(description="怎么补（中文）：学什么 / 做什么项目 / 面试怎么讲")


class TailorResult(BaseModel):
    archetype: str
    jd_keywords: list[str] = Field(description="JD 里最重要的 10-20 个技能/领域关键词")
    summary: str = Field(description="1-2 句英文个人定位，只用素材库里的事实")
    entries: list[TailoredEntry]
    skills_priority: list[str] = Field(description="技能栏里优先展示的技能名，只能从素材库 skills 里选")
    gaps: list[Gap]
    why_this_company: str = Field(description="2-3 句英文：为什么适合这家公司/岗位，只用 JD 信息和素材库事实")


SYSTEM = """You are a meticulous resume editor for finance, quant and fintech engineering roles in the United States.
You receive a candidate's experience bank (the ONLY source of truth) and one job description.

Your job: pick and lightly rewrite bullets from the bank so the resume speaks to this job, and report honest gaps.

Hard rules — breaking any of them makes the output unusable:
1. Never invent facts. Every bullet you output must come from one bank bullet (cite its exact bullet_id) and may only
   use information present in that bullet or the facts it references.
2. Keep every number exactly as written in the source (no rounding, no new numbers, no new percentages or counts).
3. Do not add tools, languages or libraries that the source bullet, its facts or the entry's stack do not mention.
   Do not claim professional/employment experience for independent projects.
4. You may reorder bullets, choose which to include, change verbs, and mirror the job's vocabulary when it is
   truthful (e.g. "event study" for a documented placebo-controlled signal test).
5. Choose 10-13 bullets in total, 2-4 per included entry; drop entries that do not help for this job.
6. Write bullets in concise American resume English: strong past-tense verb, what was built/tested, the result.
   One to two lines each. No first person, no buzzword filler, no exaggeration.
7. `gaps` must be candid: list job requirements the bank does not evidence (e.g. C++, fixed-income knowledge,
   N+ years of industry experience, specific cloud tools). `how_to_close` is written in Simplified Chinese for the
   candidate: what to learn or build, and how to address it in an interview.
8. `archetype` must be one of: quant_dev, quant_research, trading_systems, fintech_swe, risk_data,
   investment_analytics, marketplace_econ.
"""


@dataclass
class TailorOutcome:
    plan: ResumePlan
    result: TailorResult
    warnings: list[str] = field(default_factory=list)
    coverage: dict[str, bool] = field(default_factory=dict)


def bank_as_prompt(bank: Bank) -> str:
    """素材库转成给模型看的 YAML（去掉 source 字段，省 token）。"""
    data = bank.model_dump(exclude={"entries": {"__all__": {"facts": {"__all__": {"source"}}}}})
    return "# EXPERIENCE BANK (source of truth)\n" + yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=120)


def job_as_prompt(job: Job) -> str:
    return (
        f"# JOB\nCompany: {job.company}\nTitle: {job.title}\nLocation: {'; '.join(job.locations)}\n"
        f"URL: {job.url}\n\n## Description\n{job.description[:30000]}"
    )


def call_claude(bank: Bank, job: Job, client=None) -> TailorResult:
    import anthropic

    client = client or anthropic.Anthropic()
    response = client.beta.messages.parse(
        model=MODEL,
        max_tokens=16000,
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=[
            {"type": "text", "text": SYSTEM},
            # 素材库对每个 JD 都一样 → 缓存，批量定制时省钱
            {"type": "text", "text": bank_as_prompt(bank), "cache_control": {"type": "ephemeral"}},
        ],
        messages=[{"role": "user", "content": job_as_prompt(job)}],
        output_format=TailorResult,
    )
    if response.stop_reason == "refusal":
        raise RuntimeError(f"模型拒绝了这个请求：{getattr(response, 'stop_details', None)}")
    if response.parsed_output is None:
        raise RuntimeError(f"模型没有返回结构化结果（stop_reason={response.stop_reason}）")
    return response.parsed_output


def apply_guard(result: TailorResult, bank: Bank, vocabulary_raw: dict) -> TailorOutcome:
    """逐条校验改写结果；不合格的 bullet 退回素材库原文，并记录原因。"""
    vocab = compile_vocabulary(vocabulary_raw)
    warnings: list[str] = []
    entries: list[PlannedEntry] = []
    used: set[str] = set()
    for te in result.entries:
        entry = bank.entry(te.entry_id)
        if entry is None:
            warnings.append(f"模型引用了不存在的经历 {te.entry_id}，已忽略")
            continue
        ids, texts, weights = [], [], []
        for tb in te.bullets:
            src = entry.bullet(tb.bullet_id)
            if src is None or tb.bullet_id in used:
                warnings.append(f"{te.entry_id}: bullet {tb.bullet_id} 不存在或重复，已忽略")
                continue
            evidence = entry.evidence_for(src)
            problems = check_claims(tb.text, evidence) + check_skills(tb.text, evidence, entry.stack, vocab)
            if problems:
                warnings.append(f"{tb.bullet_id}: 改写被拒（{'；'.join(problems)}），已退回原文")
                text = src.text
            else:
                text = tb.text.strip()
            used.add(tb.bullet_id)
            ids.append(tb.bullet_id)
            texts.append(text)
            weights.append(max(src.weights.values() or [1]))
        if texts:
            entries.append(PlannedEntry(entry=entry, bullet_ids=ids, texts=texts, weights=weights))

    archetype = result.archetype if result.archetype in bank.summaries else "fintech_swe"
    summary = result.summary.strip()
    user_skill_names = [s.name for s in bank.skills if s.level in SHOWABLE]
    summary_problems = check_claims(summary, bank.all_fact_texts() + list(bank.summaries.values()))
    summary_problems += check_skills(summary, bank.all_fact_texts(), user_skill_names, vocab)
    if summary_problems:
        warnings.append(f"summary 改写被拒（{'；'.join(summary_problems)}），改用素材库里的 {archetype} 版本")
        summary = bank.summaries.get(archetype, "")

    lower = {n.lower(): n for n in user_skill_names}
    priority = [lower[s.lower()] for s in result.skills_priority if s.lower() in lower]
    dropped = [s for s in result.skills_priority if s.lower() not in lower]
    if dropped:
        warnings.append(f"技能栏去掉了你没有（或等级太低）的技能：{', '.join(dropped)}")

    plan = ResumePlan(archetype=archetype, summary=summary, entries=entries, skill_priority=priority, notes=warnings)
    return TailorOutcome(plan=plan, result=result, warnings=warnings)


def keyword_coverage(keywords: list[str], plan: ResumePlan, bank: Bank) -> dict[str, bool]:
    """JD 关键词有没有在最终简历里出现（给你判断还缺什么）。"""
    text = " ".join([plan.summary or ""] + [t for pe in plan.entries for t in pe.texts]
                    + [s.name for s in bank.skills if s.level in SHOWABLE]).lower()
    return {kw: kw.lower() in text for kw in keywords}


def tailor(job: Job, bank: Bank, vocabulary_raw: dict, client=None) -> TailorOutcome:
    result = call_claude(bank, job, client=client)
    outcome = apply_guard(result, bank, vocabulary_raw)
    outcome.coverage = keyword_coverage(result.jd_keywords, outcome.plan, bank)
    return outcome


def report_markdown(job: Job, outcome: TailorOutcome, files: dict) -> str:
    r = outcome.result
    lines = [
        f"# {job.company} — {job.title}",
        "",
        f"- 链接：{job.url}",
        f"- 地点：{'; '.join(job.locations)}",
        f"- 判定方向：{outcome.plan.archetype}",
        f"- 简历：{files.get('pdf') or files.get('yaml')}（页数 {files.get('pages')}，为压一页删了 {files.get('dropped', 0)} 条）",
        "",
        "## JD 关键词覆盖",
        "",
    ]
    for kw, hit in outcome.coverage.items():
        lines.append(f"- {'✅' if hit else '❌'} {kw}")
    lines += ["", "## 差距 & 怎么补", ""]
    for g in r.gaps:
        lines.append(f"- **[{g.severity}] {g.requirement}** — {g.how_to_close}")
    lines += ["", "## Why this company（可用于申请表 / cover letter，自己再改改）", "", r.why_this_company, ""]
    if outcome.warnings:
        lines += ["## ⚠ 守卫拦截记录", ""] + [f"- {w}" for w in outcome.warnings] + [""]
    lines += ["## 投递前自查", "",
              "- [ ] 每一条 bullet 我都能讲清楚细节和取舍",
              "- [ ] 联系方式、毕业时间、签证问题的回答都是真实的",
              "- [ ] 读过 JD 原文里关于 sponsorship / 学历 / 年限的要求", ""]
    return "\n".join(lines)
