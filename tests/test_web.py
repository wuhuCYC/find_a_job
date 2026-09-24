import json
import os
import threading
import urllib.error
import urllib.request
from urllib.parse import quote

import pytest
import yaml

from conftest import make_job
from jobhunt import config
from jobhunt import store as store_mod
from jobhunt.config import CompanyConfig
from jobhunt.web.data import build_payload, company_place, personal_timeline
from jobhunt.web.export import export_site, inline_page
from jobhunt.web.server import make_server, safe_output_path


# ---------------------------------------------------------------- 数据
@pytest.mark.parametrize("hq,map_city,expected", [
    ("Los Angeles + Irvine campus", None, ("Irvine", "OC")),
    ("Irvine, CA (remote-first)", None, ("Irvine", "OC")),
    ("San Francisco (Aladdin) / Santa Monica", None, ("San Francisco", "BAY")),
    ("Los Angeles, CA (Century City)", None, ("Century City", "LA")),
    ("Tampa, FL (LA office)", "Los Angeles", ("Los Angeles", "LA")),
    ("Remote-first", None, ("Remote", "REMOTE")),
    ("San Diego + Mountain View", None, ("San Diego", "SD")),
])
def test_company_place(hq, map_city, expected):
    place = company_place(CompanyConfig(key="x", name="X", hq=hq, map_city=map_city))
    assert (place["city"], place["region"]) == expected
    assert (place["lat"] is None) == (expected[1] not in ("LA", "OC"))


def test_personal_timeline_opt_math():
    t = personal_timeline({"work_authorization": {"program_end_date": "2026-06-12"}})
    assert t["opt_deadline"] == "2026-08-11"          # 项目结束后 60 天
    dates = [e["date"] for e in t["events"]]
    assert dates == sorted(dates)
    assert "2026-03-14" in dates                        # 最早可提交：结束前 90 天
    assert "2027-03-10" in dates                        # 下一次 H-1B 注册

    t2 = personal_timeline({"work_authorization": {"program_end_date": "2026-06-12", "opt_filed_date": "2026-07-01",
                                                   "ead_start_date": "2026-08-01"}})
    assert t2["filed"] == "2026-07-01" and t2["ead_start"] == "2026-08-01"
    assert any(e["date"] == "2026-10-30" and e["kind"] == "deadline" for e in t2["events"])   # EAD + 90 天
    assert personal_timeline({"work_authorization": {"program_end_date": "TODO"}}) is None
    assert personal_timeline({}) is None


def test_build_payload_snapshot(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    p = build_payload(mode="snapshot", include_jobs=True, examples_if_empty=True)
    assert p["mode"] == "snapshot" and p["examples"] is True
    assert len(p["companies"]) == len(config.load_companies())
    assert all(j.get("example") for j in p["jobs"]) and p["jobs"] == sorted(p["jobs"], key=lambda j: -j["score"])
    bullets = {b["id"] for e in p["bank"]["entries"] for b in e["bullets"]}
    for a in p["archetype_order"]:
        assert all(bid in bullets for plan in p["plans"][a] for bid in plan["bullet_ids"])
    json.dumps(p)   # 必须能序列化（YAML 里的日期已转成字符串）
    assert p["resumes"] == {}   # 快照里不链接本地 PDF


def test_strategy_yaml_shapes():
    """strategy.yaml 里的流式映射如果值里有英文逗号（如 $103,265）会被拆坏，这里兜底。"""
    d = yaml.safe_load(open(config.ROOT / "docs" / "strategy.yaml", encoding="utf-8"))
    def keys(items, expected):
        for it in items:
            assert set(it) == expected, it
    keys(d["visa"]["items"], {"title", "status", "meaning"})
    keys(d["visa"]["events"], {"date", "note"})
    keys(d["quant_vs_fintech"]["rows"], {"label", "quant", "fintech"})
    keys(d["books"], {"title", "why"})
    for reqs in d["requirements"].values():
        keys(reqs, {"item", "have"})
        assert all(r["have"] in ("yes", "partial", "no") for r in reqs)   # yes/no 必须加引号，否则变成布尔
    for row in d["hiring"]["rows"]:
        keys(row.get("spans", []), {"start", "end", "kind", "note"})
        keys(row.get("marks", []), {"date", "note"})
    archetypes = set(config.load_archetypes())
    assert {x["key"] for x in d["directions"]} == archetypes
    assert set(d["requirements"]) == archetypes


# ---------------------------------------------------------------- 导出
def test_inline_page_escapes_script_close():
    page = inline_page({"mode": "snapshot", "evil": "</script><script>alert(1)</script>"})
    assert page.count("</script>") == 2           # 只剩数据块和程序块自己的闭合标签
    assert '<link rel="stylesheet" href="app.css">' not in page and '<script src="app.js">' not in page
    assert '<script id="snapshot" type="application/json">' in page


def test_export_site_modes(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    art = export_site(tmp_path / "a.html", standalone=False).read_text(encoding="utf-8")
    std = export_site(tmp_path / "s.html", standalone=True).read_text(encoding="utf-8")
    assert "<html" not in art and art.lstrip().startswith("<title>")
    assert std.startswith("<!doctype html>")


# ---------------------------------------------------------------- 本地服务
@pytest.fixture
def server(monkeypatch, tmp_path):
    monkeypatch.setattr(config, "DATA_DIR", tmp_path)
    monkeypatch.setattr(store_mod, "DATA_DIR", tmp_path)
    s = store_mod.Store(tmp_path / "jobs.db")
    job = make_job("Quantitative Developer", "backtesting in Python")
    s.upsert_jobs("pimco", [job])
    from jobhunt.actions import make_scorer
    s.save_score(job.uid, make_scorer().score(job))
    s.close()
    srv = make_server(port=0, allowed_hosts={"jobs.example.com"}, server_mode=True)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{srv.server_address[1]}", job
    srv.shutdown()
    srv.server_close()


def _req(url, body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, headers=headers or {}, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()


def test_server_read_and_write(server):
    base, job = server
    status, body = _req(base + "/api/data")
    data = json.loads(body)
    assert status == 200 and data["mode"] == "live" and data["can_apply"] is False
    assert [j["uid"] for j in data["jobs"]] == [job.uid] and "description" not in data["jobs"][0]

    status, body = _req(base + "/api/job?uid=" + quote(job.uid))
    assert status == 200 and "backtesting" in json.loads(body)["description"]

    ok_headers = {"Content-Type": "application/json", "X-Jobhunt": "1"}
    assert _req(base + "/api/status", {"uid": job.uid, "status": "applied"}, {"Content-Type": "application/json"})[0] == 403
    assert _req(base + "/api/status", {"uid": job.uid, "status": "ghosted"}, ok_headers)[0] == 400
    assert _req(base + "/api/status", {"uid": job.uid, "status": "applied"}, ok_headers)[0] == 200
    data = json.loads(_req(base + "/api/data")[1])
    assert data["jobs"][0]["status"] == "applied"

    # 服务器模式不能开浏览器预填
    assert _req(base + "/api/apply", {"uid": job.uid}, ok_headers)[0] == 400


def test_server_host_check(server):
    base, _ = server
    assert _req(base + "/api/data", headers={"Host": "evil.example.net"})[0] == 403
    assert _req(base + "/api/data", headers={"Host": "jobs.example.com"})[0] == 200


def test_safe_output_path(tmp_path, monkeypatch):
    monkeypatch.setattr(config, "OUTPUT_DIR", tmp_path)
    (tmp_path / "base").mkdir()
    (tmp_path / "base" / "r.pdf").write_bytes(b"%PDF")
    (tmp_path / "base" / "x.py").write_text("print(1)")
    assert safe_output_path("base/r.pdf") == (tmp_path / "base" / "r.pdf").resolve()
    assert safe_output_path("base/x.py") is None
    assert safe_output_path("../../etc/passwd") is None
    assert safe_output_path("%2e%2e/%2e%2e/etc/hosts") is None


# ---------------------------------------------------------------- 浏览器冒烟测试
def test_exported_site_renders_without_errors(tmp_path, monkeypatch):
    sync_api = pytest.importorskip("playwright.sync_api")
    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    site = export_site(tmp_path / "site.html", standalone=True)
    exe = os.environ.get("JOBHUNT_BROWSER_PATH") or ("/opt/pw-browsers/chromium" if os.path.exists("/opt/pw-browsers/chromium") else None)
    errors = []
    with sync_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        except Exception as exc:  # noqa: BLE001
            pytest.skip(f"浏览器不可用：{exc}")
        page = browser.new_page(viewport={"width": 1200, "height": 900})
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.goto(site.as_uri())
        page.wait_for_selector("#view-overview .fit-row")
        for view in ["jobs", "companies", "resumes", "skills", "visa", "overview"]:
            page.click(f"#tab-{view}")
            assert page.is_visible(f"#view-{view}")
            assert sum(page.is_visible(f"#view-{v}") for v in ["overview", "jobs", "companies", "resumes", "skills", "visa"]) == 1
        page.click("#tab-jobs")
        page.click("#job-results tbody tr")
        assert page.is_visible("#drawer")
        page.keyboard.press("Escape")
        assert not page.is_visible("#drawer")
        assert page.locator("#view-companies svg circle").count() > 20
        assert "null" not in page.inner_text("#view-companies")
        browser.close()
    assert errors == []
