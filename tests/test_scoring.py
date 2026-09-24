from conftest import make_job

QUANT_DEV_JD = """
PIMCO is seeking a Quantitative Developer to build research platforms, backtesting infrastructure and
signal pipelines for systematic strategies. You will work with portfolio managers on time series data.
Requirements: Python (pandas, NumPy), SQL, C++ a plus. Experience with optimization and simulation.
PIMCO participates in E-Verify.
"""

SENIOR_JD = "Lead a team of engineers. 8+ years of experience with Java."
NO_SPONSOR_JD = """Backend engineer for our payments ledger. Python, SQL, AWS.
Applicants must be authorized to work in the United States; we are unable to sponsor visas."""


def test_quant_dev_role_scores_high(scorer):
    r = scorer.score(make_job("Quantitative Developer", QUANT_DEV_JD))
    assert not r.excluded
    assert r.archetype == "quant_dev"
    assert r.regions == ["OC"]
    assert {"Python", "pandas", "NumPy", "SQL"} <= set(r.matched_skills)
    assert "C++" in r.missing_skills
    assert "e_verify" in r.flags
    assert r.score >= 70


def test_senior_role_excluded(scorer):
    r = scorer.score(make_job("Senior Software Engineer", SENIOR_JD))
    assert r.excluded and "职级" in r.exclude_reason


def test_non_tech_role_excluded(scorer):
    r = scorer.score(make_job("Financial Advisor Sales Associate", "Grow client relationships."))
    assert r.excluded


def test_out_of_region_excluded(scorer):
    r = scorer.score(make_job("Software Engineer", "Python", locations=["Chicago, IL"]))
    assert r.excluded and "地区" in r.exclude_reason


def test_remote_us_allowed(scorer):
    r = scorer.score(make_job("Software Engineer", "Python", locations=["Remote - US"]))
    assert not r.excluded and r.regions == ["REMOTE_US"]


def test_visa_blocker_penalized_when_sponsorship_needed(scorer):
    base = scorer.score(make_job("Software Engineer", NO_SPONSOR_JD.split("Applicants")[0]))
    blocked = scorer.score(make_job("Software Engineer", NO_SPONSOR_JD))
    assert "no_sponsorship" in blocked.flags and "visa_blocker" in blocked.flags
    assert blocked.score <= base.score - 30


def test_experience_penalty(scorer):
    easy = scorer.score(make_job("Software Engineer", "Python and SQL."))
    hard = scorer.score(make_job("Software Engineer", "Python and SQL. 5+ years of experience required."))
    assert hard.score < easy.score
    assert any(f.startswith("yoe>=") for f in hard.flags)


def test_company_tier_and_finance_context(scorer):
    fin = scorer.score(make_job("Software Engineer", "Python services.", company_key="pimco"))
    other = scorer.score(make_job("Software Engineer", "Python services.", company_key="acme"))
    assert fin.score > other.score
    assert fin.archetype == "fintech_swe"


def test_prefilter(scorer):
    assert scorer.prefilter("Quantitative Developer", ["Newport Beach, CA"])
    assert scorer.prefilter("Quantitative Developer", [])            # 地点未知先放行
    assert not scorer.prefilter("Quantitative Developer", ["London"])
    assert not scorer.prefilter("Senior Quant Developer", ["Irvine, CA"])
    assert not scorer.prefilter("Summer 2026 Intern", ["Irvine, CA"])
