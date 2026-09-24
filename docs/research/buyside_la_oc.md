# LA / Orange County buy-side, trading, and capital-markets employers (as of 2026-09-24)

**Scope.** Asset managers, hedge funds, prop/HFT firms, broker-dealers, and investment banks with offices in Los Angeles County or Orange County. Each firm is judged against this candidate: UCI MS EECS; Python, Java, and React; a self-built equity signal and backtest system; likely needs visa sponsorship.

**Method and limits.** Evidence comes from WebSearch result titles, snippets, and URLs, including ATS identifiers taken from posting URLs and H-1B counts from h1bdata, h1bgrader, and myvisajobs snippets. **The shared session limit of 200 web searches ran out partway through this task.** Only these firms were checked with searches: PIMCO, Capital Group, Pacific Life, Research Affiliates, DoubleLine, and TCW. Crabel, Los Angeles Capital Management, Franklin Templeton's ATS, and the office lists for the HFT and market-making firms were checked through search results that parallel agents had already fetched in this session. **Every other entry comes from background knowledge and is marked `UNVERIFIED`.** Treat those as leads to check, not facts.

**Visa context that changes the ranking.** Source: the parallel visa agent's search results.
- FY2027 was the first H-1B cap year run as a wage-weighted lottery (final rule effective 2026-02-27). Higher offered wage levels now get better odds, which favors well-paid quant and engineering roles at PIMCO, Capital Group, and Crabel.
- The $100K H-1B proclamation fee exempts F-1 change-of-status cases. A court also vacated it in June 2026; an appeal is pending.
- **DHS proposed a $103,265 fee on every cap-subject H-1B petition on 2026-08-25.** It would apply to F-1 change-of-status cases and to the US advanced-degree cap as well. Comments close around 2026-09-24, and the rule is not final. If it is finalized, expect smaller firms to stop sponsoring new graduates. Large firms (PIMCO, Capital Group, Pacific Life) are the likeliest to keep paying. Cap-exempt employers (universities and their affiliated nonprofits) would not pay it.
- An OPT-fee proposal cleared White House review on 2026-09-11 and has not yet been published.

All H-1B counts below are historical LCA filings. They show willingness to sponsor in the past, not a guarantee under the 2026-27 rules.

```yaml
# ---------- VERIFIED BY SEARCH (this session) ----------
- name: "PIMCO (Pacific Investment Management Company)"
  city: "Newport Beach"
  region: OC
  category: asset_manager
  roles:
    - "2026 Summer Intern - Technology Analyst, Software Engineering (Newport Beach; $52.88/hr)"
    - "2026 Summer Intern - PhD Quant Research Analyst, Client Solutions & Analytics"
    - "Quantitative Developer (Newport Beach; posted base $130K-$195K)"
    - "Quantitative Research Analyst / Quantitative Researcher-Developer, PM Analytics, Portfolio Engineering & Implementation (Newport Beach; $165K-$215K; 'integrate systematic signals and models into the investment process')"
    - "Quantitative Research Analyst - Client Solutions & Analytics (Newport Beach)"
    - "Quantitative Developer - SMA Muni"
    - "Software Engineer, Short Term Technology (Java 17/21, microservices, AWS; trading & cash-management systems; 5+ yrs)"
    - "Senior Developer, Investment Accounting ($168K-$240K)"
  roles_in_region: "Yes. Newport Beach HQ is the main tech/quant hub. Some PIMCO roles are also posted in New York (Built In NYC lists PIMCO jobs)."
  new_grad: "Yes, mainly through the Technology Analyst (SWE) summer internship and the PhD quant internship, both pipelines to full-time analyst hires. No separate full-time new-grad tech posting for 2026-27 was seen (unverified). Most quant developer/research postings ask for an MS plus about 3 yrs of Python/C++ and relational DBs."
  ats: Workday
  ats_id: "pimco.wd1.myworkdayjobs.com, site 'pimco-careers' (seen as /wday/cxs/pimco/pimco-careers)"
  careers_url: "https://www.pimco.com/us/en/about-us/careers"
  h1b: "strong. h1bdata shows 103 LCA records for Pacific Investment Management Company (PIMCO), median $168K (33% above $200K). Ellis/h1bgrader put the median H-1B salary around $155K; top titles are Financial Analysts and Software Developers, Applications."
  fit: "Best OC fit. The quant developer and researcher-developer roles take systematic signals into production and build backtest, market-data, and compute infrastructure, which mirrors the candidate's signal system and walk-forward backtester. The Python/Java stack matches. Gaps: the fixed-income focus and the 3-yr experience asks on many roles, so also target Technology Analyst and junior quant dev openings."
  sources:
    - "https://pimco.wd1.myworkdayjobs.com/wday/cxs/pimco/pimco-careers"
    - "https://www.pimco.com/us/en/about-us/careers"
    - "https://builtin.com/job/2026-summer-intern-technology-analyst-software-engineering/7009931"
    - "https://builtin.com/job/2026-summer-internship-phd-quant-research-analyst-client-solutions-analytics/7009940"
    - "https://www.builtinla.com/job/quantitative-developer/6205246"
    - "https://www.builtinla.com/job/quantitative-research-analyst/6758286"
    - "https://builtin.com/job/quantitative-developer-sma-muni/7303326"
    - "https://www.dice.com/job-detail/af755a67-68ee-44fa-af55-9e08b5f8b86b"
    - "https://h1bdata.info/index.php?em=pacific+investment+management+company+(pimco)&city=newport+beach"
    - "https://h1bgrader.com/h1b-sponsors/pacific-investment-management-company-pimco-vk487v3g0w"
    - "https://www.ellis.com/visa-sponsors/pacific-investment-management-company-llc/salaries"

- name: "Capital Group (American Funds)"
  city: "Los Angeles (HQ, downtown) + Irvine (technology campus)"
  region: "LA + OC"
  category: asset_manager
  roles:
    - "CAMPUS: Technology Rotational Experience (TREx) Associate (2026) - Irvine (rotations in solutions/software engineering, architecture, infosec, etc.)"
    - "CAMPUS: Software Development Engineer Associate"
    - "New Grad - Software Development Engineer I"
    - "CAMPUS: Information Technology Summer Associate (2026) - Irvine"
    - "CAMPUS: Data Engineer (2024) - Irvine"
    - "Quant Engineer - downtown LA or Irvine (SoCal base $148,045-$236,872; R/Python/MATLAB; turn quant models into production software)"
    - "Machine Learning Engineer - Irvine ($148,045-$236,872)"
    - "Solutions Engineer II - Irvine; Data Product Manager - Irvine"
  roles_in_region: "Yes. Irvine is the main technology campus; the Quant Engineer role is based in LA or Irvine."
  new_grad: "Strong. Formal CAMPUS programs (TREx rotational, SDE Associate, New Grad SDE I, Data Engineer, IT Summer Associate), mostly in Irvine."
  ats: Workday
  ats_id: "capgroup.wd1.myworkdayjobs.com, site 'capitalgroupcareers'"
  careers_url: "https://www.capitalgroup.com/about-us/careers.html (students: https://www.capitalgroup.com/about-us/careers/students.html)"
  h1b: "strong (historical). h1bdata shows 50 LCA records for 'Capital Group Companies Global' in 2021 (median $145K; Solutions Engineer III/IV, Data Science Analyst) and a Software Developer Engineer II median of $192K. 'Capital Research and Management Company' also files (investment analyst). Recent-year counts not confirmed, and whether CAMPUS roles sponsor is UNVERIFIED; ask the recruiter."
  fit: "Top target by volume: the largest new-grad tech intake in OC, plus a Quant Engineer role that matches the candidate's model-to-production trading work. The investing side is mostly long-only and fundamental, so most tech roles are platform and data work rather than alpha. The firm also contributes 15% of eligible pay to retirement."
  sources:
    - "https://capgroup.wd1.myworkdayjobs.com/capitalgroupcareers"
    - "https://capgroup.wd1.myworkdayjobs.com/en-US/capitalgroupcareers/job/Irvine/CAMPUS--Data-Engineer--2024-_JR1815"
    - "https://capgroup.wd1.myworkdayjobs.com/capitalgroupcareers/job/Irvine/Solutions-Engineer-II_JR5025"
    - "https://www.themuse.com/jobs/capitalgroup/campus-technology-rotational-experience-trex-associate-2026"
    - "https://www.wayup.com/i-Investment-Management-j-New-Grad-Software-Development-Engineer-I-Capital-Group-212791420529711/"
    - "https://www.linkedin.com/jobs/view/campus-software-development-engineer-associate-at-capital-group-4051427718"
    - "https://builtin.com/job/campus-information-technology-summer-associate-2026/7008591"
    - "https://openquant.co/job/quant-engineer-capital-group/1918"
    - "https://www.theladders.com/job/quant-engineer-thecapitalgroupcompaniesinc-irvine-ca_81237895"
    - "https://h1bdata.info/index.php?em=capital+group+companies+global"
    - "https://h1bgrader.com/h1b-sponsors/capital-research-and-management-company-n60e4vqmkz"

- name: "Pacific Life (Pacific Life Investments)"
  city: "Newport Beach"
  region: OC
  category: other
  roles:
    - "Quantitative Analyst - Pacific Life Investments (Newport Beach; hybrid; $111K-$135K; portfolio optimization/monitoring models)"
    - "Investment risk quant (cash-flow and market-risk models for public/illiquid assets; on-site Newport Beach)"
    - "Summer 2026 Software Engineering Internship Program (Newport Beach, req R15496)"
    - "Investment Analyst Intern (Summer 2026, Newport Beach)"
    - "Summer 2027 Actuarial Intern (Newport Beach, req R17460)"
  roles_in_region: "Yes. The investments division and much of technology are in Newport Beach; other functions are in Omaha NE and Charlotte NC."
  new_grad: "Yes. Summer internships in software engineering, data engineering, investment analysis, and actuarial. Summer-2027 postings are expected Sept-Oct 2026 (the actuarial one is already up)."
  ats: Workday
  ats_id: "pacificlife.wd1.myworkdayjobs.com, site 'PacificLifeCareers'"
  careers_url: "https://www.pacificlife.com/home/Careers.html (early career: https://www.pacificlife.com/home/Careers/early-career.html)"
  h1b: "strong. h1bdata shows 90 records for Pacific Life Insurance Company (median about $126.9K). myvisajobs: 13 H-1B I-129 petitions approved and 0 denied in FY2025; not H-1B dependent."
  fit: "Solid, sponsorship-friendly OC option. The Quantitative Analyst role (pandas/optimization models for a large bond portfolio) is a reachable entry point. It is insurance general-account investing rather than trading, and pay is lower than PIMCO."
  sources:
    - "https://pacificlife.wd1.myworkdayjobs.com/PacificLifeCareers"
    - "https://pacificlife.wd1.myworkdayjobs.com/PacificLifeCareers/job/Newport-Beach-CA-700/Summer-2026-Software-Engineering-Internship-Program_R15496"
    - "https://pacificlife.wd1.myworkdayjobs.com/PacificLifeCareers/job/Newport-Beach-CA-700/Summer-2027-Actuarial-Intern--Newport-Beach-_R17460"
    - "https://builtin.com/job/quantitative-analyst/4694748"
    - "https://builtin.com/job/investment-analyst-intern/3473366"
    - "https://www.pacificlife.com/home/Careers/early-career.html"
    - "https://h1bdata.info/index.php?em=pacific+life+insurance+company"
    - "https://www.myvisajobs.com/employer/pacific-life-insurance/"

- name: "Research Affiliates"
  city: "Newport Beach"
  region: OC
  category: asset_manager
  roles:
    - "Software Engineer - Investment Systems team (listed on careers page; posting date not confirmed)"
    - "Researcher (quant research on risk/return drivers, develop new signals into strategies; $95K-$125K + bonus)"
    - "Analyst (LinkedIn posting, Newport Beach)"
  roles_in_region: "Yes. Newport Beach is the firm's US office."
  new_grad: "Moderate. The Researcher role is early-career (coding plus data-set work plus signal research). No formal program seen. Current openings not confirmed."
  ats: "unknown (roles hosted on researchaffiliates.com; applications to humancapital@rallc.com)"
  ats_id: "unknown"
  careers_url: "https://www.researchaffiliates.com/about-us/careers"
  h1b: "some. h1bdata shows 14 LCA records for Research Affiliates LLC (median $127.5K)."
  fit: "Excellent content fit: factor/smart-beta signal research is what the candidate's 21-signal walk-forward system does. Caveat: TMX Group bought RAFI Indices LLC from Research Affiliates for US$490M (announced June 2026, completion announced by TMX), and the firm's LinkedIn now says 'Research Affiliates & RAFI are now part of VettaFi'. Check which entity is hiring and whether it sponsors."
  sources:
    - "https://www.researchaffiliates.com/about-us/careers"
    - "https://www.researchaffiliates.com/about-us/careers/researcher"
    - "https://www.linkedin.com/jobs/view/analyst-at-research-affiliates-4246705576"
    - "https://h1bdata.info/index.php?em=research+affiliates+llc"
    - "https://www.tmx.com/en/newsroom/press-releases?id=1358"
    - "https://www.tmx.com/en/newsroom/press-releases?id=1374"
    - "https://www.vettafi.com/insights/indexing-article-tmx-vettafi-completes-acquisition-of-rafi-indices-from-research-affiliates"
    - "https://www.linkedin.com/company/research-affiliates"

- name: "TCW Group"
  city: "Los Angeles (515 S. Flower St, downtown)"
  region: LA
  category: asset_manager
  roles:
    - "Salesforce Software Engineer / Salesforce Developer - Engineering Solutions, Corporate Services (LA)"
    - "Senior Developer Analyst (title seen in LA LCA filings)"
    - "Summer 2026 Internship Program (LA/NY/Boston; 9 weeks from 2026-06-15; grads Dec 2026-Jun 2027; GPA 3.0+)"
  roles_in_region: "Yes. Engineering is at the LA HQ; the firm has about 20 US openings overall."
  new_grad: "Yes. A structured internship leads to offers for the full-time analyst program the following year (early-career programs page)."
  ats: iCIMS
  ats_id: "careers-tcw.icims.com (e.g., /jobs/2120/summer-2026-internship-program); internal portal careers-int-tcw.icims.com"
  careers_url: "https://www.tcw.com/careers (openings: https://www.tcw.com/careers/opportunities; early career: https://www.tcw.com/careers/early-career-programs)"
  h1b: "some. h1bdata shows 26 records for TCW LLC (median $125K); Senior Developer Analyst in LA x2 at median $156.5K; 5 LCAs in FY2024, all certified."
  fit: "Good LA engineering option on investment platforms, with some Salesforce/enterprise work. If the MS ends between Dec 2026 and Jun 2027, apply to the next internship cycle; otherwise target developer-analyst roles."
  sources:
    - "https://careers-tcw.icims.com/jobs/2120/summer-2026-internship-program/job"
    - "https://careers-int-tcw.icims.com/jobs/intro"
    - "https://www.tcw.com/careers/opportunities"
    - "https://www.tcw.com/careers/early-career-programs"
    - "https://www.builtinla.com/company/tcw-group"
    - "https://h1bdata.info/index.php?em=tcw+llc"
    - "https://h1bdata.info/index.php?city=los+angeles&em=tcw+llc&job=senior+developer+analyst"
    - "https://h1bgrader.com/h1b-sponsors/tcw-llc-ew2xyz6nk3"

- name: "DoubleLine"
  city: "Los Angeles (office; HQ now Tampa, FL)"
  region: LA
  category: asset_manager
  roles:
    - "Director, Data Technology (Los Angeles)"
    - "Analyst - Corporate Credit; Analyst - EM credit; Analyst - CMBS/CRE (LA postings)"
  roles_in_region: "Partly. LA postings still appear in 2025-26, but Wikipedia now lists Tampa as HQ, Gundlach is moving there, and a Tampa office was leased. Expect growth in Tampa."
  new_grad: "Limited. Analyst roles only; no tech new-grad program seen. About 259 employees."
  ats: "unknown (apply via doubleline.com)"
  ats_id: "unknown"
  careers_url: "https://doubleline.com (careers section; exact URL unverified)"
  h1b: "some (small). h1bdata shows 4 records for DoubleLine Group LP: Quantitative Risk Analyst x3 (median $117K) and Analyst, Government Securities x1."
  fit: "Lower priority: small, fundamental fixed-income shop that is shifting to Tampa. Past quant-risk-analyst sponsorship is a plus."
  sources:
    - "https://en.wikipedia.org/wiki/DoubleLine_Capital"
    - "https://www.thewealthadvisor.com/article/gundlach-and-doubleline-capital-moving-tampa"
    - "https://www.builtinla.com/company/doubleline-group-lp/jobs"
    - "https://www.glassdoor.com/Jobs/DoubleLine-Jobs-E1395029.htm"
    - "https://h1bdata.info/index.php?em=DOUBLELINE+GROUP+LP"

- name: "Crabel Capital Management"
  city: "Los Angeles (HQ)"
  region: LA
  category: quant_hedge_fund
  roles:
    - "UNVERIFIED which are open now: Software Engineer (C++/Python), Quantitative Researcher, Quantitative Developer, trading/operations roles. No live posting with a salary range was surfaced in search."
  roles_in_region: "Likely yes (the firm is LA-based and Built In LA lists Crabel jobs), but check each posting because the firm also has other offices (UNVERIFIED)."
  new_grad: "UNVERIFIED. No new-grad program surfaced in search."
  ats: "UNVERIFIED (careers page crabel.com/careers; ATS vendor not seen in URLs)"
  ats_id: "unknown"
  careers_url: "https://crabel.com/careers/"
  h1b: "some. LCA pages exist on h1bdata.info and h1bgrader for Crabel Capital Management LLC, and h1bsalary.online shows an LCA titled 'High Frequency Trading Specialist'. Counts not seen."
  fit: "The only systematic futures/FX trading firm confirmed headquartered in LA, and the closest match to the candidate's automated-signal, backtest, and live-monitor work. Expect a high bar (C++, statistics, trading-firm interviews) and small hiring numbers."
  sources:
    - "https://crabel.com/careers/"
    - "https://www.builtinla.com/company/crabel-capital-management-llc/jobs"
    - "https://h1bdata.info/index.php?em=CRABEL+CAPITAL+MANAGEMENT+LLC&job="
    - "https://h1bgrader.com/h1b-sponsors/crabel-capital-management-llc-1k9nnl4x2m/salaries"
    - "https://h1bsalary.online/index.php?searchtext=CRABEL+CAPITAL+MANAGEMENT+LLC&job_title=HIGH+FREQUENCY+TRADING+SPECIALIST"
    - "https://en.wikipedia.org/wiki/Toby_Crabel"

- name: "Los Angeles Capital Management (LACM)"
  city: "Los Angeles"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: quantitative research analyst, software/data engineering (quant equity manager with a model-driven stock-selection process)"
  roles_in_region: "UNVERIFIED (single LA office as far as known)"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: firm website careers page"
  h1b: "some (small). myvisajobs: 4 LCAs in the first three quarters of FY2025 and 1 H-1B I-129 approved in FY2025."
  fit: "Strong content fit (systematic equity factor models) and has sponsored recently, but it is small. Worth a direct application and a follow-up search."
  sources:
    - "https://www.myvisajobs.com/employer/los-angeles-capital-management/"

# ---------- NOT VERIFIED BY SEARCH (search budget exhausted) - background knowledge; verify before use ----------
- name: "Western Asset Management (Franklin Templeton)"
  city: "Pasadena"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: historically Pasadena hosted many Java/.NET/Python developers, quant analysts, and risk/analytics roles"
  roles_in_region: "UNVERIFIED. Franklin's own engineering roles are posted largely in San Mateo and elsewhere."
  new_grad: "UNVERIFIED"
  ats: Workday
  ats_id: "franklintempleton.wd5.myworkdayjobs.com, site 'Primary-External-1' (verified via a Franklin posting URL; that Western Asset roles go through it is UNVERIFIED)"
  careers_url: "https://careers.franklintempleton.com/us/en"
  h1b: "unknown (UNVERIFIED: Western Asset historically filed LCAs for developers and quant analysts)"
  fit: "UNVERIFIED current state. Since the former co-CIO was charged in late 2024 there have been heavy outflows and restructuring, so tech hiring in Pasadena may be thin. Check recent postings before investing time."
  sources:
    - "https://franklintempleton.wd5.myworkdayjobs.com/en-US/Primary-External-1/job/Senior-Software-Engineer_864529"
    - "https://careers.franklintempleton.com/us/en"

- name: "Oaktree Capital Management"
  city: "Los Angeles (333 S. Grand Ave, downtown)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: enterprise technology, data engineering and analytics at the LA HQ; investment analyst roles"
  roles_in_region: "UNVERIFIED (LA is HQ; large NY/London presence)"
  new_grad: "UNVERIFIED: believed to run a summer analyst / analyst program, mainly investment-side"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.oaktreecapital.com (careers section)"
  h1b: "unknown"
  fit: "Credit/alternatives giant (majority-owned by Brookfield). Tech roles are likely platform/enterprise rather than quant. A moderate fit, but a big LA employer worth checking."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Ares Management"
  city: "Los Angeles (Century City HQ)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: technology, data and AI engineering, and investment analyst roles; many roles are posted in New York"
  roles_in_region: "UNVERIFIED (HQ in LA, but much hiring in NY)"
  new_grad: "UNVERIFIED: analyst and summer analyst programs exist, mostly investment-side"
  ats: "UNVERIFIED: believed to be Workday"
  ats_id: "UNVERIFIED (possibly aresmgmt.wd1.myworkdayjobs.com)"
  careers_url: "UNVERIFIED: https://www.aresmgmt.com (careers section)"
  h1b: "unknown"
  fit: "Large, growing alternatives manager with a real data/tech build-out. Verify whether engineering roles sit in LA."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Payden & Rygel"
  city: "Los Angeles (downtown)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: fixed-income analyst, risk/quant analyst, small IT team"
  roles_in_region: "UNVERIFIED (LA HQ)"
  new_grad: "UNVERIFIED: hires analysts out of school"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.payden.com (careers section)"
  h1b: "unknown"
  fit: "Independent LA bond manager. Moderate fit via risk/analytics roles; few pure engineering openings."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Wilshire Advisors"
  city: "Santa Monica"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: quantitative/performance analytics, analytics-platform engineering, OCIO/consulting analyst"
  roles_in_region: "UNVERIFIED (Santa Monica HQ)"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.wilshire.com (careers section)"
  h1b: "unknown"
  fit: "Analytics and index heritage (the Wilshire 5000) makes it a plausible quant-analytics landing spot. Privately owned since 2021 (UNVERIFIED)."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Guggenheim Investments"
  city: "Santa Monica"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: portfolio analytics, quant/risk analyst, some technology roles"
  roles_in_region: "UNVERIFIED (Santa Monica is a major investment office; much tech is in NY/Chicago)"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.guggenheimpartners.com (careers section)"
  h1b: "unknown"
  fit: "Moderate. Fixed-income analytics roles could use the candidate's Python/data skills."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Beach Point Capital Management"
  city: "Santa Monica"
  region: LA
  category: hedge_fund
  roles:
    - "UNVERIFIED: small credit fund; occasional analyst/operations roles"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED (unlikely to have a program)"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Low. Small discretionary credit shop with few tech roles."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Kayne Anderson Capital Advisors (and Kayne Anderson Rudnick)"
  city: "Los Angeles (Century City)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: investment analyst, data/IT roles"
  roles_in_region: "UNVERIFIED (Kayne Anderson also has Houston and other offices)"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Low-moderate: mostly fundamental/alternatives investing."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Hotchkis & Wiley"
  city: "Los Angeles (downtown)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: small firm; occasional quant/research-analyst or IT roles"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Low: small value-equity boutique."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Dimensional Fund Advisors"
  city: "Santa Monica office (HQ Austin, TX)"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: research and portfolio roles may sit in Santa Monica; engineering is mainly Austin and Charlotte"
  roles_in_region: "UNVERIFIED. Tech roles are probably NOT in LA."
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.dimensional.com (careers section)"
  h1b: "unknown"
  fit: "Systematic, evidence-based investing is a good content match, but tech jobs are likely out of region; check for Santa Monica research roles."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Houlihan Lokey"
  city: "Los Angeles (Century City HQ)"
  region: LA
  category: investment_bank
  roles:
    - "UNVERIFIED: Corporate Finance financial analyst, Financial & Valuation Advisory (FVA) analyst, summer analyst; some IT/data roles"
  roles_in_region: "UNVERIFIED (LA HQ with a large analyst class)"
  new_grad: "UNVERIFIED: runs analyst and summer-analyst programs"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://hl.com (careers section)"
  h1b: "unknown (UNVERIFIED: believed to file analyst LCAs)"
  fit: "Money-adjacent but banking/valuation (Excel and modeling) rather than engineering. Only if the candidate wants an analyst track."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Wedbush Securities"
  city: "Los Angeles (downtown HQ)"
  region: LA
  category: broker_dealer
  roles:
    - "UNVERIFIED: in-house developers for brokerage/clearing/trading platforms, equity research associate"
  roles_in_region: "UNVERIFIED (LA HQ)"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED: https://www.wedbush.com (careers section)"
  h1b: "unknown"
  fit: "Possible trading-technology entry point in LA (order routing, clearing). Verify current tech postings."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "B. Riley Financial / B. Riley Securities"
  city: "Los Angeles"
  region: LA
  category: investment_bank
  roles:
    - "UNVERIFIED"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Low. UNVERIFIED but widely reported financial distress in 2024-25 (large losses, delayed filings, asset sales) makes it a risky sponsor."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Roth Capital Partners"
  city: "Newport Beach"
  region: OC
  category: investment_bank
  roles:
    - "UNVERIFIED: IB/equity research analyst; small tech team"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Low for engineering; banking-analyst track only."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "Causeway Capital Management"
  city: "Los Angeles"
  region: LA
  category: asset_manager
  roles:
    - "UNVERIFIED: runs quantitative equity strategies with an in-house quant research team; quant research analyst and software roles appear from time to time"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: "unknown"
  ats_id: "unknown"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  fit: "Potentially strong content fit (quant equity) if a role is open. Added as a discovered lead; verify."
  sources:
    - "none retrieved - shared search budget exhausted"

- name: "BlackRock (Santa Monica office, ex-Tennenbaum/TCP)"
  city: "Santa Monica (engineering mainly SF/NY/Atlanta)"
  region: LA
  category: asset_manager
  roles:
    - "Santa Monica: UNVERIFIED, likely private-credit investment roles only"
    - "California tech is in San Francisco (verified via parallel search): Associate Full Stack Engineer ($133K-$162K), Analyst Quant Research ($112K-$133K), Quantitative/Systematic Research Associate ($133K-$162K)"
  roles_in_region: "No for tech. The LA presence is UNVERIFIED and investment-only; SF is the California fallback."
  new_grad: "Yes at firm level (graduate programs), but not in LA."
  ats: Workday
  ats_id: "blackrock.wd1.myworkdayjobs.com, site 'BlackRock_Professional'"
  careers_url: "https://careers.blackrock.com/search-jobs"
  h1b: "unknown here (large sponsor firm-wide; not checked this session)"
  fit: "SF-fallback employer rather than an LA one."
  sources:
    - "https://blackrock.wd1.myworkdayjobs.com/BlackRock_Professional"
    - "https://careers.blackrock.com/search-jobs"
```

## Other LA/OC leads, not researched (all UNVERIFIED)
- **Canyon Partners** (Century City; credit hedge fund), **Crescent Capital Group** (LA; credit), **Aristotle Capital Management** (LA) / **Aristotle Pacific Capital** (Newport Beach, Pacific Life-affiliated), **FPA** (LA), **First Quadrant** (Pasadena quant; current status unknown), **PAAMCO Prisma** (Irvine; status unknown). These are mostly small or fundamental; check for quant/analytics roles.
- **PE firms**: Leonard Green (LA), Clearlake (Santa Monica), Platinum Equity (Beverly Hills). Few engineering roles.
- **Bulge-bracket and boutique IB offices in LA** (Goldman Sachs, Morgan Stanley, J.P. Morgan, BofA, Jefferies, Moelis, Evercore, Lazard). The LA offices are mostly banking and wealth management; engineering hubs are elsewhere.
- **Cap-exempt angle (important under the proposed $103K fee):** university investment offices in LA (e.g., USC Investment Office, Caltech Investment Office in Pasadena, UCLA Investment Company) are probably H-1B cap-exempt if they are part of, or a qualifying nonprofit affiliate of, the university. They would then skip both the lottery and the proposed fee. The teams are small and analyst-heavy. UNVERIFIED; ask an immigration attorney.
- **Mortgage and capital-markets fintech** (PennyMac in Westlake Village, loanDepot in Irvine, Acorns in Irvine) is covered by the fintech research stream.

## Firms with NO LA/OC office in the office lists seen (search snippets, Sept 2026)
- **Hudson River Trading**: US offices in NY, Austin, Boston, Boulder, Chicago, Seattle. No California. (hudsonrivertrading.com/offices)
- **Jane Street**: official offices are NY, London, HK, Singapore, Amsterdam. A San Francisco address (220 Montgomery St) also appears. No LA. (janestreet.com/culture/our-offices)
- **Citadel**: 24 offices, including San Francisco (4 Embarcadero Center). No LA seen. (citadel.com/who-we-are/office-locations)
- **Citadel Securities**: HQ Miami; offices include San Francisco. No LA. (builtinsf.com/company/citadel-securities/offices)
- **Optiver**: US offices Chicago, Austin, New York. No California. (optiver.com/join-us/locations)
- **IMC**: US offices Chicago and New York. No California. (imc.com/us/contact/offices)
- **DRW**: Chicago, Austin, Greenwich, Houston, New York. No California. (drw.com/contact-us)
- **Tower Research**: NY, Chicago, South Charleston, Iselin (US). No California. (tower-research.com/offices)
- **Headlands Technologies**: Chicago, San Francisco, London. No LA. Greenhouse board: job-boards.greenhouse.io/headlandstechnologiesllc.
- **Five Rings**: New York and London only.
- **Akuna Capital**: Chicago HQ plus Sydney, Shanghai, Singapore, London. No California.
- **XTX, Old Mission, Radix, Vatic Labs, Two Sigma, Man Group**: no California/LA office in the lists seen. Two Sigma's SF presence is Two Sigma Ventures.
- **Conflicting evidence, treat as "no LA hiring" unless a posting shows LA:**
  - **Jump Trading**: one aggregator lists LA and SF; other sources list only Chicago, NY, and Austin in the US.
  - **Susquehanna (SIG)**: one aggregator lists "Los Angeles"; the sig.com office list snippet shows San Francisco (101 California St), not LA.
  - **AQR**: one aggregator lists LA; the official pages seen show Greenwich HQ and no California office.
- The nearest California HFT/quant hubs are in the SF Bay Area: Citadel, Citadel Securities, SIG, Headlands, and a Jane Street address in SF, plus Voleon in Berkeley. These are covered by the CA-wide research stream.

## Visa-policy sources (from the parallel visa agent's searches)
- https://www.uscis.gov/newsroom/news-releases/dhs-proposes-additional-h-1b-fee
- https://www.federalregister.gov/documents/2026/08/25/2026-17324/fee-for-certain-h-1b-petitions
- https://www.fragomen.com/insights/united-states-uscis-proposes-new-fee-of-over-dollar100000-for-h-1b-cap-subject-petitions.html
- https://www.federalregister.gov/documents/2025/12/29/2025-23853/weighted-selection-process-for-registrants-and-petitioners-seeking-to-file-cap-subject-h-1b
- https://www.bakerlaw.com/insights/uscis-clarifies-when-100000-h-1b-fee-is-required-exempting-most-f-1-students/
- https://hrwatchdog.calchamber.com/2026/06/federal-court-strikes-down-100000-h-1b-visa-fee/
- https://www.fragomen.com/insights/united-states-dhs-optional-practical-training-fee-proposal-clears-federal-review.html
