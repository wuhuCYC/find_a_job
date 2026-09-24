import os

import pytest

from jobhunt.apply import apply_url_for, match_field, plan_fill, prefill_page, profile_values

PROFILE = {
    "person": {"name": "Test Person", "email": "t@example.com", "phone": "+1 949 555 0100",
               "location": "Irvine, CA", "linkedin": "test-person", "github": "tester"},
    "graduation": {"school": "University of California, Irvine", "degree": "MS EECS", "date": "TODO"},
    "application_answers": {"current_company": "UC Irvine", "how_did_you_hear": "Company website"},
}


def test_profile_values_skips_placeholders():
    v = profile_values(PROFILE)
    assert v["first_name"] == "Test" and v["last_name"] == "Person"
    assert v["linkedin_url"] == "https://www.linkedin.com/in/test-person"
    assert "graduation" not in v


@pytest.mark.parametrize("label,name,expected", [
    ("First Name *", "", "first_name"),
    ("Legal Last Name", "", "last_name"),
    ("Full name", "name", "full_name"),
    ("Email", "", "email"),
    ("Phone", "", "phone"),
    ("LinkedIn Profile", "", "linkedin_url"),
    ("", "urls[GitHub]", "github_url"),
    ("Current company", "org", "current_company"),
    ("How did you hear about us?", "", "how_did_you_hear"),
    ("Company Name", "", None),
    ("Why do you want to work here?", "", None),
])
def test_match_field(label, name, expected):
    assert match_field(label, name) == expected


def test_plan_fill_routes_manual_fields():
    fields = [
        {"idx": 0, "tag": "input", "type": "text", "label": "First Name", "name": "", "id": "", "required": True, "value": "", "visible": True},
        {"idx": 1, "tag": "input", "type": "text", "label": "Last Name", "name": "", "id": "", "required": True, "value": "Already", "visible": True},
        {"idx": 2, "tag": "select", "type": "", "label": "Will you require sponsorship?", "name": "", "id": "", "required": True, "value": "", "visible": True},
        {"idx": 3, "tag": "textarea", "type": "", "label": "Why this company?", "name": "", "id": "", "required": True, "value": "", "visible": True},
        {"idx": 4, "tag": "input", "type": "hidden", "label": "token", "name": "", "id": "", "required": False, "value": "", "visible": False},
        {"idx": 5, "tag": "input", "type": "file", "label": "Cover Letter", "name": "cover_letter", "id": "", "required": False, "value": "", "visible": True},
    ]
    to_fill, manual = plan_fill(fields, profile_values(PROFILE))
    assert to_fill == [(0, "first_name", "Test")]
    assert {m["idx"] for m in manual} == {2, 3, 5}


def test_apply_url_for():
    assert apply_url_for("https://jobs.lever.co/tala/abc", None) == "https://jobs.lever.co/tala/abc/apply"
    assert apply_url_for("https://jobs.ashbyhq.com/Acorns/1", None) == "https://jobs.ashbyhq.com/Acorns/1/application"
    assert apply_url_for("https://x.com/job", "https://x.com/apply") == "https://x.com/apply"


FORM = """
<form onsubmit="window.submitted = true; return false;">
  <label for="fn">First Name *</label><input id="fn" required>
  <label for="ln">Last Name *</label><input id="ln" required>
  <label>Email <input type="email" name="email"></label>
  <input name="urls[LinkedIn]" placeholder="LinkedIn URL">
  <label for="cv">Resume/CV</label><input type="file" id="cv" name="resume">
  <label for="q1">Are you legally authorized to work in the US?</label>
  <select id="q1" required><option></option><option>Yes</option><option>No</option></select>
  <button type="submit" id="submit">Submit</button>
</form>
"""


def _browser_path():
    return os.environ.get("JOBHUNT_BROWSER_PATH") or ("/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)


def test_prefill_page_fills_uploads_and_never_submits(tmp_path):
    sync_api = pytest.importorskip("playwright.sync_api")
    resume = tmp_path / "resume.pdf"
    resume.write_bytes(b"%PDF-1.4 test")
    with sync_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(executable_path=_browser_path()) if _browser_path() else p.chromium.launch()
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"浏览器不可用：{exc}")
        page = browser.new_page()
        page.set_content(FORM)
        result = prefill_page(page, PROFILE, resume)
        assert page.input_value("#fn") == "Test" and page.input_value("#ln") == "Person"
        assert page.input_value("input[name=email]") == "t@example.com"
        assert page.input_value("input[name='urls[LinkedIn]']") == "https://www.linkedin.com/in/test-person"
        assert result["uploaded"] and page.eval_on_selector("#cv", "el => el.files.length") == 1
        assert any("authorized" in m["label"] for m in result["manual"])
        assert page.evaluate("window.submitted === true") is False
        browser.close()
