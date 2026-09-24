"""抓取器解析测试。样例 JSON 按各家公开 API 文档的字段结构手写（沙箱里连不上真实接口）。"""
from jobhunt.config import CompanyConfig
from jobhunt.fetchers import ashby, greenhouse, icims, jobvite, lever, smartrecruiters, workday

ALLOW_ALL = lambda title, locs: True  # noqa: E731


def test_greenhouse_parse():
    c = CompanyConfig(key="zest", name="Zest AI", ats={"type": "greenhouse", "token": "zestai"})
    data = {"jobs": [{
        "id": 4001, "title": " Software Engineer ", "updated_at": "2026-09-01T00:00:00Z",
        "location": {"name": "Burbank, CA"},
        "offices": [{"name": "Burbank", "location": "Burbank, California, United States"}, {"name": "Remote"}],
        "departments": [{"name": "Engineering"}],
        "absolute_url": "https://job-boards.greenhouse.io/zestai/jobs/4001",
        "content": "&lt;p&gt;Build &lt;b&gt;credit&lt;/b&gt; models in Python&lt;/p&gt;",
    }]}
    jobs = greenhouse.parse(data, c)
    assert len(jobs) == 1
    j = jobs[0]
    assert j.title == "Software Engineer" and j.source_id == "4001"
    assert j.locations == ["Burbank, CA", "Burbank, California, United States", "Remote"]
    assert "credit models in Python" in j.description
    assert j.uid == "greenhouse:zest:4001"


def test_lever_parse():
    c = CompanyConfig(key="tala", name="Tala", ats={"type": "lever", "site": "tala"})
    data = [{
        "id": "abc-123", "text": "Data Platform Engineer I",
        "categories": {"location": "Santa Monica, CA", "allLocations": ["Santa Monica, CA", "Remote - US"], "team": "Data"},
        "descriptionPlain": "Build pipelines.", "lists": [{"text": "Requirements", "content": "<li>Python</li><li>SQL</li>"}],
        "additionalPlain": "We sponsor visas.", "hostedUrl": "https://jobs.lever.co/tala/abc-123",
        "applyUrl": "https://jobs.lever.co/tala/abc-123/apply", "workplaceType": "hybrid", "createdAt": 1756684800000,
        "salaryRange": {"currency": "USD", "interval": "per-year-salary", "min": 120000, "max": 150000},
    }]
    j = lever.parse(data, c)[0]
    assert j.locations == ["Santa Monica, CA", "Remote - US"]
    assert "Requirements" in j.description and "- Python" in j.description and "We sponsor visas." in j.description
    assert j.salary.startswith("USD 120,000–150,000")
    assert j.posted_at == "2025-09-01"
    assert j.remote is None


def test_ashby_parse_skips_unlisted():
    c = CompanyConfig(key="acorns", name="Acorns", ats={"type": "ashby", "org": "Acorns"})
    data = {"jobs": [
        {"id": "1", "title": "Software Engineer I, Recent Graduate", "location": "Irvine, CA",
         "secondaryLocations": [{"location": "Remote - US"}], "isRemote": True, "isListed": True,
         "descriptionPlain": "Java and Python.", "jobUrl": "https://jobs.ashbyhq.com/Acorns/1",
         "applyUrl": "https://jobs.ashbyhq.com/Acorns/1/application",
         "compensation": {"compensationTierSummary": "$130K – $150K"}},
        {"id": "2", "title": "Hidden", "isListed": False},
    ]}
    jobs = ashby.parse(data, c)
    assert [j.source_id for j in jobs] == ["1"]
    assert jobs[0].locations == ["Irvine, CA", "Remote - US"] and jobs[0].salary == "$130K – $150K"


class FakeHttp:
    """按 URL 返回预设数据，并记录请求。"""

    def __init__(self, posts=None, gets=None, texts=None):
        self.posts, self.gets, self.texts = posts or {}, gets or {}, texts or {}
        self.calls = []

    def post_json(self, url, payload):
        self.calls.append(("POST", url, payload.get("offset")))
        return self.posts[(url, payload.get("offset"))]

    def get_json(self, url, params=None):
        self.calls.append(("GET", url, params))
        return self.gets[url]

    def get_text(self, url, params=None):
        self.calls.append(("TEXT", url, params))
        return self.texts[url] if url in self.texts else self.texts[(url, (params or {}).get("pr"))]


def test_workday_paginates_prefilters_and_fetches_detail():
    host, tenant, site = "pimco.wd1.myworkdayjobs.com", "pimco", "pimco-careers"
    c = CompanyConfig(key="pimco", name="PIMCO", ats={"type": "workday", "host": host, "tenant": tenant, "site": site})
    base = f"https://{host}/wday/cxs/{tenant}/{site}"
    page0 = {"total": 21, "jobPostings": [
        {"title": f"Role {i}", "externalPath": f"/job/Newport-Beach/Role_{i}", "locationsText": "Newport Beach, CA"}
        for i in range(19)] + [{"title": "Quantitative Developer", "externalPath": "/job/x/QD_R1", "locationsText": "2 Locations"}]}
    page1 = {"total": 0, "jobPostings": [{"title": "Senior Manager", "externalPath": "/job/y/SM_R2", "locationsText": "Newport Beach, CA"}]}
    detail = {"jobPostingInfo": {"title": "Quantitative Developer", "jobReqId": "R1", "location": "Newport Beach, CA",
                                 "additionalLocations": ["New York, NY"], "jobDescription": "<p>Backtest infra in Python</p>",
                                 "externalUrl": f"https://{host}/pimco-careers/job/x/QD_R1", "startDate": "2026-09-10"}}
    http = FakeHttp(posts={(f"{base}/jobs", 0): page0, (f"{base}/jobs", 20): page1}, gets={f"{base}/job/x/QD_R1": detail})

    def prefilter(title, locs):
        return title.startswith("Quantitative")

    jobs = workday.fetch(c, http, prefilter)
    assert [j.title for j in jobs] == ["Quantitative Developer"]
    j = jobs[0]
    assert j.source_id == "R1" and j.locations == ["Newport Beach, CA", "New York, NY"]
    assert "Backtest infra in Python" in j.description
    assert j.apply_url.endswith("/apply")
    # 两页列表 + 只对通过粗筛的职位请求一次详情
    assert [c[0] for c in http.calls] == ["POST", "POST", "GET"]


def test_smartrecruiters_fetch():
    c = CompanyConfig(key="experian", name="Experian", ats={"type": "smartrecruiters", "company_id": "Experian", "country": "us"})
    api = "https://api.smartrecruiters.com/v1/companies/Experian/postings"
    listing = {"totalFound": 2, "content": [
        {"id": "744", "name": "Software Engineer - Xcelerator", "location": {"city": "Costa Mesa", "region": "CA", "country": "us"},
         "releasedDate": "2026-09-01", "department": {"label": "Technology"}},
        {"id": "745", "name": "Sales Executive", "location": {"city": "Costa Mesa", "region": "CA", "country": "us"}},
    ]}
    detail = {"jobAd": {"sections": {"jobDescription": {"title": "Job Description", "text": "<p>Java microservices</p>"},
                                      "qualifications": {"title": "Qualifications", "text": "<ul><li>SQL</li></ul>"}}},
              "postingUrl": "https://jobs.smartrecruiters.com/Experian/744", "applyUrl": "https://jobs.smartrecruiters.com/Experian/744?apply"}
    http = FakeHttp(gets={api: listing, f"{api}/744": detail})
    jobs = smartrecruiters.fetch(c, http, lambda t, l: "Sales" not in t)
    assert len(jobs) == 1
    assert jobs[0].locations == ["Costa Mesa, CA, US"]
    assert "Java microservices" in jobs[0].description and "- SQL" in jobs[0].description
    assert jobs[0].apply_url.endswith("?apply")


ICIMS_PAGE = """
<div class="row"><div class="col-xs-12 title">
  <a href="https://careers-tcw.icims.com/jobs/2120/summer-2026-internship-program/job?in_iframe=1" class="iCIMS_Anchor" title="2120 - Summer 2026 Internship Program">
    <span class="sr-only field-label">Title</span><h3>Summer 2026 Internship Program</h3></a></div>
  <div class="col-xs-6 header left"><span class="sr-only field-label">Location</span>
    <span>US-CA-Los Angeles</span></div></div>
<div class="row"><div class="col-xs-12 title">
  <a href="https://careers-tcw.icims.com/jobs/2133/software-engineer/job?in_iframe=1" class="iCIMS_Anchor" title="2133 - Software Engineer">
    <h3>Software Engineer</h3></a></div>
  <div class="col-xs-6 header left"><span class="sr-only field-label">Location</span><span>US-NY-New York</span></div></div>
"""


def test_icims_parse_search_page():
    rows = icims.parse_search_page(ICIMS_PAGE, "careers-tcw.icims.com")
    assert [r["id"] for r in rows] == ["2120", "2133"]
    assert rows[0]["title"] == "Summer 2026 Internship Program"
    assert rows[0]["location"] == "US-CA-Los Angeles" and rows[1]["location"] == "US-NY-New York"
    assert rows[1]["url"] == "https://careers-tcw.icims.com/jobs/2133/software-engineer/job"


JOBVITE_PAGE = """
<table class="jv-job-list"><tr>
  <td class="jv-job-list-name"><a href="/loandepot/job/oAbc123">Software Engineer I</a></td>
  <td class="jv-job-list-location">Irvine, California</td></tr>
<tr><td class="jv-job-list-name"><a href="/loandepot/job/oXyz789">Loan Officer</a></td>
  <td class="jv-job-list-location">Plano, Texas</td></tr></table>
"""


def test_jobvite_parse_list():
    rows = jobvite.parse_list(JOBVITE_PAGE)
    assert [(r["id"], r["title"], r["location"]) for r in rows] == [
        ("oAbc123", "Software Engineer I", "Irvine, California"),
        ("oXyz789", "Loan Officer", "Plano, Texas"),
    ]
    assert rows[0]["url"] == "https://jobs.jobvite.com/loandepot/job/oAbc123"
