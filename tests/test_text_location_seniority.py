import pytest

from jobhunt.location import classify_location, classify_locations, is_unresolved
from jobhunt.seniority import classify_seniority, min_years_required
from jobhunt.text import compile_keyword, html_to_text


def test_html_to_text_handles_escaped_greenhouse_content():
    raw = "&lt;p&gt;We build &lt;strong&gt;trading&lt;/strong&gt; systems.&lt;/p&gt;&lt;ul&gt;&lt;li&gt;Python&lt;/li&gt;&lt;li&gt;C++&lt;/li&gt;&lt;/ul&gt;"
    text = html_to_text(raw)
    assert "We build trading systems." in text
    assert "- Python" in text and "- C++" in text
    assert "<" not in text


def test_html_to_text_drops_scripts_and_empty():
    assert html_to_text("") == ""
    assert "alert" not in html_to_text("<p>Hi</p><script>alert(1)</script>")


def test_keyword_word_boundaries():
    assert compile_keyword("quant").search("Quant Developer")
    assert not compile_keyword("quant").search("quantity surveyor")
    assert compile_keyword("c++").search("strong C++ skills")
    assert compile_keyword("re:\\balgo\\b").search("Algo Trading")


@pytest.mark.parametrize("loc,expected", [
    ("Newport Beach, CA", {"OC"}),
    ("Irvine, California, United States", {"OC"}),
    ("US-CA-Irvine", {"OC"}),
    ("Orange, CA", {"OC"}),
    ("Los Angeles, CA", {"LA"}),
    ("Santa Monica", {"LA"}),
    ("Westlake Village, CA", {"LA"}),
    ("LA or NYC", {"LA"}),
    ("San Diego, CA", {"SD"}),
    ("San Francisco, CA", {"BAY"}),
    ("Remote - US", {"REMOTE_US"}),
    ("Remote", {"REMOTE_US"}),
    ("Remote - Canada", {"OTHER"}),
    ("Remote - Texas", {"OTHER"}),
    ("Glendale, AZ", {"OTHER"}),
    ("Long Beach, NY", {"OTHER"}),
    ("New York, NY", {"OTHER"}),
    ("London, United Kingdom", {"OTHER"}),
    ("Sacramento, CA", {"CA_OTHER"}),
])
def test_classify_location(loc, expected):
    assert classify_location(loc) == expected


def test_classify_locations_merges_and_drops_other():
    assert classify_locations(["New York, NY", "Irvine, CA"]) == ["OC"]
    assert classify_locations([], remote=True) == ["REMOTE_US"]
    assert classify_locations(["Chicago, IL"]) == ["OTHER"]


def test_unresolved_locations():
    assert is_unresolved(["2 Locations"])
    assert is_unresolved(["Multiple Locations"])
    assert not is_unresolved(["Irvine, CA"])


@pytest.mark.parametrize("title,expected", [
    ("Software Engineer I, Recent Graduate", "entry"),
    ("New Grad - Software Development Engineer I", "entry"),
    ("CAMPUS: Technology Rotational Experience (TREx) Associate (2026)", "entry"),
    ("Quantitative Developer", "unknown"),
    ("Software Engineer II", "mid"),
    ("Senior Software Engineer", "senior"),
    ("Sr. Quant Analyst", "senior"),
    ("Staff Engineer, Payments", "senior"),
    ("Engineering Manager", "senior"),
    ("Associate Director, Risk", "senior"),
    ("Summer 2026 Intern - Technology Analyst", "intern"),
    ("Leadership Development Program Analyst", "entry"),
])
def test_classify_seniority(title, expected):
    assert classify_seniority(title) == expected


def test_min_years_required():
    assert min_years_required("Requires 3+ years of experience with Python; 5+ years of experience preferred") == 3
    assert min_years_required("at least 2 years in fintech") == 2
    assert min_years_required("0-2 years of relevant experience") is None or min_years_required("0-2 years of relevant experience") <= 2
    assert min_years_required("No experience requirement mentioned") is None
