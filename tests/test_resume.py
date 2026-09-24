import pytest

from conftest import TEST_PROFILE
from jobhunt.resume import pdf_page_count, rendercv_command, select_base, to_rendercv, write_and_render

ARCHETYPES = ["quant_dev", "quant_research", "trading_systems", "fintech_swe", "risk_data",
              "investment_analytics", "marketplace_econ"]


@pytest.mark.parametrize("archetype", ARCHETYPES)
def test_select_base(bank, archetype):
    plan = select_base(bank, archetype)
    total = sum(len(pe.texts) for pe in plan.entries)
    assert 8 <= total <= 13
    for pe in plan.entries:
        assert 1 <= len(pe.texts) <= 4
        # 段内保持素材库的叙事顺序
        order = [b.id for b in pe.entry.bullets]
        assert pe.bullet_ids == sorted(pe.bullet_ids, key=order.index)


def test_different_archetypes_lead_with_different_projects(bank):
    def first_project(archetype):
        return next(pe.entry.id for pe in select_base(bank, archetype).entries if pe.entry.kind != "experience")
    assert first_project("fintech_swe") == "portfolio_alert_saas"
    assert first_project("quant_research") == "cs2_market_platform"
    # 有真实雇主的经历排在最前
    assert select_base(bank, "fintech_swe").entries[0].entry.kind == "experience"


def test_to_rendercv_structure(bank):
    data = to_rendercv(select_base(bank, "quant_dev"), bank, TEST_PROFILE)
    cv = data["cv"]
    assert cv["name"] == "Test Person"
    assert "phone" not in cv                       # 占位值不输出
    assert cv["sections"]["education"][0]["institution"] == "University of California, Irvine"
    assert all("TODO" not in str(v) for ed in cv["sections"]["education"] for v in ed.values())   # TODO 字段被跳过
    assert cv["sections"]["projects"] and cv["sections"]["skills"]
    skills_text = " ".join(s["details"] for s in cv["sections"]["skills"])
    assert "C++" not in skills_text and "AWS" not in skills_text   # coursework/none 等级不展示
    page = data["design"]["page"]
    assert len({page[k] for k in ("top_margin", "bottom_margin", "left_margin", "right_margin")}) == 1


def test_unconfirmed_end_date_is_not_rendered_as_present(bank):
    """只有开始日期时 RenderCV 会写「– present」：结束日期没确认就整段不写日期。"""
    entry = bank.entries[0].model_copy(update={"kind": "experience", "start": "2023-10", "end": "TODO"})
    other = bank.model_copy(update={"entries": [entry]})
    plan = select_base(other, next(iter(entry.bullets[0].weights)))
    exp = to_rendercv(plan, other, TEST_PROFILE)["cv"]["sections"]["experience"][0]
    assert "start_date" not in exp and "end_date" not in exp
    confirmed = entry.model_copy(update={"end": "present"})
    plan = select_base(other.model_copy(update={"entries": [confirmed]}), next(iter(entry.bullets[0].weights)))
    exp = to_rendercv(plan, other, TEST_PROFILE)["cv"]["sections"]["experience"][0]
    assert exp["end_date"] == "present"


def test_drop_weakest_bullet(bank):
    plan = select_base(bank, "quant_dev")
    before = sum(len(pe.texts) for pe in plan.entries)
    assert plan.drop_weakest_bullet()
    assert sum(len(pe.texts) for pe in plan.entries) == before - 1


@pytest.mark.skipif(rendercv_command() is None, reason="没装 rendercv")
def test_render_one_page_pdf(bank, tmp_path):
    try:
        files = write_and_render(select_base(bank, "quant_dev"), bank, TEST_PROFILE, tmp_path, "resume")
    except RuntimeError as exc:
        if "download" in str(exc) or "Proxy" in str(exc):
            pytest.skip("离线环境无法下载 Typst 包")
        raise
    assert files["pdf"].exists()
    if pdf_page_count(files["pdf"]) is not None:
        assert files["pages"] == 1
