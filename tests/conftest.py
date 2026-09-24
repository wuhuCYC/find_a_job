from __future__ import annotations

import pytest

from jobhunt import config
from jobhunt.bank import load_bank
from jobhunt.config import CompanyConfig
from jobhunt.models import Job
from jobhunt.scoring import Scorer

TEST_PROFILE = {
    "work_authorization": {"requires_sponsorship_now": False, "requires_sponsorship_future": True},
    "preferences": {
        "archetype_priority": ["quant_dev", "trading_systems", "fintech_swe", "investment_analytics",
                               "quant_research", "risk_data", "marketplace_econ"],
        "include_internships": False,
    },
    "person": {"name": "Test Person", "email": "test@example.com", "location": "Irvine, CA", "github": "tester"},
}


@pytest.fixture(scope="session")
def bank():
    return load_bank(config.PROFILE_DIR / "experience_bank.yaml")


@pytest.fixture(scope="session")
def search():
    return config.load_search()


@pytest.fixture
def companies():
    return [
        CompanyConfig(key="pimco", name="PIMCO", tier=1, category="asset_manager"),
        CompanyConfig(key="acme", name="Acme Retail", tier=3, category="other"),
    ]


@pytest.fixture
def scorer(bank, search, companies):
    return Scorer(config.load_archetypes(), search, TEST_PROFILE, [s.model_dump() for s in bank.skills], companies)


def make_job(title, description="", locations=("Newport Beach, CA",), company_key="pimco", remote=None, **kw):
    return Job(company_key=company_key, company=company_key.upper(), source="test", source_id=title[:20],
               title=title, url="https://example.com/job", locations=list(locations), description=description,
               remote=remote, **kw)
