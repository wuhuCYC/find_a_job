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
    assert select_base(bank, "fintech_swe").entries[0].entry.id == "portfolio_alert_saas"
    assert select_base(bank, "quant_research").entries[0].entry.id == "cs2_market_platform"


def test_to_rendercv_structure(bank):
    data = to_rendercv(select_base(bank, "quant_dev"), bank, TEST_PROFILE)
    cv = data["cv"]
    assert cv["name"] == "Test Person"
    assert "phone" not in cv                       # 占位值不输出
    assert cv["sections"]["education"][0]["institution"] == "University of California, Irvine"
    assert "start_date" not in cv["sections"]["education"][0]   # TODO 日期被跳过
    assert cv["sections"]["projects"] and cv["sections"]["skills"]
    skills_text = " ".join(s["details"] for s in cv["sections"]["skills"])
    assert "C++" not in skills_text and "AWS" not in skills_text   # coursework/none 等级不展示
    page = data["design"]["page"]
    assert len({page[k] for k in ("top_margin", "bottom_margin", "left_margin", "right_margin")}) == 1


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
