from types import SimpleNamespace

import pytest

from conftest import make_job
from jobhunt.tailor import (Gap, TailorResult, TailoredBullet, TailoredEntry, apply_guard, call_claude,
                            keyword_coverage, report_markdown)


def _result(**overrides):
    base = dict(
        archetype="quant_dev",
        jd_keywords=["backtesting", "Python", "C++"],
        summary="MS EECS candidate at UC Irvine who builds backtesting and signal research tools in Python.",
        entries=[
            TailoredEntry(entry_id="equity_signal_platform", bullets=[
                # 合法改写：数字一致
                TailoredBullet(bullet_id="eq.backtester", text=(
                    "Built an event-driven backtester with next-open execution, limit-up/down handling, position caps "
                    "(10 names, ≤20% each), asymmetric commissions and tiered slippage, reporting Sharpe and drawdown.")),
                # 编造数字：Sharpe 2.1
                TailoredBullet(bullet_id="eq.optuna", text="Tuned parameters with Optuna, reaching a Sharpe ratio of 2.1."),
                # 编造技术：Kafka
                TailoredBullet(bullet_id="eq.realtime_monitor", text="Streamed quotes through Kafka every 6 seconds."),
                TailoredBullet(bullet_id="does.not.exist", text="Fake."),
            ]),
            TailoredEntry(entry_id="nope", bullets=[TailoredBullet(bullet_id="x", text="y")]),
        ],
        skills_priority=["Python", "C++", "pandas", "Kubernetes"],
        gaps=[Gap(requirement="C++", severity="high", how_to_close="补一个 C++ 订单簿项目")],
        why_this_company="PIMCO's systematic research needs production-grade tooling.",
    )
    base.update(overrides)
    return TailorResult(**base)


def test_guard_keeps_valid_rewrites_and_reverts_invented(bank, search):
    outcome = apply_guard(_result(), bank, search["skill_vocabulary"])
    (pe,) = outcome.plan.entries
    assert pe.bullet_ids == ["eq.backtester", "eq.optuna", "eq.realtime_monitor"]
    assert pe.texts[0].startswith("Built an event-driven backtester")          # 合法改写保留
    src = {b.id: b.text for b in pe.entry.bullets}
    assert pe.texts[1] == src["eq.optuna"]                                      # 编造数字 → 退回原文
    assert pe.texts[2] == src["eq.realtime_monitor"]                            # 编造技术 → 退回原文
    joined = " ".join(outcome.warnings)
    assert "2.1" in joined and "Kafka" in joined and "does.not.exist" in joined and "nope" in joined
    # C++ 是 coursework、Kubernetes 没有 → 不能进技能栏
    assert outcome.plan.skill_priority == ["Python", "pandas"]


def test_guard_rejects_summary_with_invented_numbers(bank, search):
    outcome = apply_guard(_result(summary="Engineer with 5 years of trading experience."), bank, search["skill_vocabulary"])
    assert outcome.plan.summary == bank.summaries["quant_dev"]


def test_keyword_coverage(bank, search):
    outcome = apply_guard(_result(), bank, search["skill_vocabulary"])
    cov = keyword_coverage(["backtester", "C++", "Python"], outcome.plan, bank)
    assert cov == {"backtester": True, "C++": False, "Python": True}


class FakeMessages:
    def __init__(self, response):
        self.response = response
        self.kwargs = None

    def parse(self, **kwargs):
        self.kwargs = kwargs
        return self.response


def _client(response):
    messages = FakeMessages(response)
    return SimpleNamespace(beta=SimpleNamespace(messages=messages)), messages


def test_call_claude_wiring(bank):
    client, messages = _client(SimpleNamespace(stop_reason="end_turn", parsed_output=_result()))
    result = call_claude(bank, make_job("Quantitative Developer", "Python backtesting"), client=client)
    assert result.archetype == "quant_dev"
    kw = messages.kwargs
    assert kw["model"] == "claude-opus-5" and kw["output_format"] is TailorResult
    assert kw["fallbacks"] == "default" and kw["betas"] == ["server-side-fallback-2026-07-01"]
    assert kw["system"][1]["cache_control"] == {"type": "ephemeral"}
    assert "EXPERIENCE BANK" in kw["system"][1]["text"] and "source:" not in kw["system"][1]["text"]
    assert "Quantitative Developer" in kw["messages"][0]["content"]


def test_call_claude_refusal(bank):
    client, _ = _client(SimpleNamespace(stop_reason="refusal", parsed_output=None, stop_details=None))
    with pytest.raises(RuntimeError):
        call_claude(bank, make_job("Quant", "x"), client=client)


def test_report_markdown(bank, search):
    outcome = apply_guard(_result(), bank, search["skill_vocabulary"])
    outcome.coverage = {"Python": True, "C++": False}
    md = report_markdown(make_job("Quantitative Developer"), outcome, {"pdf": "x.pdf", "pages": 1, "dropped": 0})
    assert "❌ C++" in md and "补一个 C++ 订单簿项目" in md and "守卫拦截记录" in md
