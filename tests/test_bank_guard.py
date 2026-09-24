from jobhunt.bank import validate_bank
from jobhunt.guard import check_numbers, check_skills, compile_vocabulary, numbers_in


def test_real_bank_is_consistent(bank, search):
    """素材库里每条 bullet 的数字和技术栈都必须有事实支撑 —— 改素材库后这个测试必须过。"""
    assert validate_bank(bank, search["skill_vocabulary"]) == []


def test_every_archetype_has_summary_and_bullets(bank):
    archetypes = {"quant_dev", "quant_research", "trading_systems", "fintech_swe", "risk_data",
                  "investment_analytics", "marketplace_econ"}
    assert archetypes <= set(bank.summaries)
    for a in archetypes:
        assert sum(1 for e in bank.entries for b in e.bullets if b.weights.get(a, 0) >= 2) >= 4, a


def test_numbers_in_normalizes():
    assert numbers_in("13,671 events, 46.0% vs 46%, CS2, L1/L2, T+1") == {13671.0, 46.0, 1.0}


def test_check_numbers_flags_invented_numbers():
    evidence = ["hit rate 46.0% vs 33.3% on 13,671 events"]
    assert check_numbers("46% vs. 33.3% across 13671 events", evidence) == []
    assert check_numbers("46% hit rate, 2x the baseline", evidence) == ["数字 2 在原始事实里找不到"]


def test_check_skills_flags_new_tech(search):
    vocab = compile_vocabulary(search["skill_vocabulary"])
    assert check_skills("Built it in Python with pandas", ["Python pipeline"], ["pandas"], vocab) == []
    problems = check_skills("Built it in Python and Kafka on AWS", ["Python pipeline"], ["pandas"], vocab)
    assert any("Kafka" in p for p in problems) and any("AWS" in p for p in problems)


def test_validate_bank_catches_problems(bank, search):
    broken = bank.model_copy(deep=True)
    b = broken.entries[0].bullets[0]
    b.text = b.text + " Improved Sharpe by 42%."
    b.facts = b.facts + ["missing_fact"]
    problems = validate_bank(broken, search["skill_vocabulary"])
    assert any("42" in p for p in problems)
    assert any("missing_fact" in p for p in problems)
