# Money-adjacent employers in LA / Orange County / San Diego: research notes (as of 2026-09-24)

**Scope:** fintech, banks, lending and credit, credit bureaus and financial data, insurance and investments, payments, crypto, and pricing-heavy marketplaces or game economies in LA County, Orange County and San Diego.

**Candidate:** UC Irvine MS EECS. Strong in Python, Java and React, with self-built trading and pricing systems. Native Mandarin speaker. Likely needs H-1B sponsorship.

**Method:** WebSearch only (fetching and browsing were blocked). All evidence comes from search-result titles, snippets and URLs. ATS identifiers are taken from job-posting URLs I actually saw.

**How to read this file:**
- **Verified entries (the first 15 below):** every fact is backed by a search result listed under `sources`. Numbers in the H-1B field come from h1bdata, h1bgrader, 1point3acres or MyVisaJobs snippets. These counts are Labor Condition Application (LCA) filings, not approved visas. The sites do not always make clear which years they cover.
- **UNVERIFIED entries:** these come after the verified ones. The session-wide WebSearch limit (200 calls, shared with other agents) ran out partway through my list. I did not check the following companies at all:
  - Cathay Bank, City National Bank, Banc of California, Preferred Bank and SchoolsFirst FCU
  - Farmers Insurance, Mercury Insurance and Pacific Life
  - Whatnot, GOAT Group and Collectors/PSA
  - Blizzard and Riot Games
  - LPL Financial and Brandes
  - crypto employers, plus the planned searches for companies not on the original list

  In those entries, anything marked "UNVERIFIED (prior knowledge)" comes from memory, not from a search. Treat any ATS ID marked "guess" as something to confirm before relying on it.
- **Empty `sources` list:** nothing in that entry was confirmed in this session.

**Recommended follow-up:** raise `CLAUDE_CODE_MAX_WEB_SEARCHES_PER_SESSION` and re-run the unverified entries, Riot, Blizzard, Whatnot, GOAT and Collectors first. Those are the strongest fits for pricing and game economies.

```yaml
- name: Acorns (Acorns Grow Inc.)
  city: Irvine (HQ; remote-first with optional Irvine office; NYC office too)
  region: OC
  category: fintech
  roles:
    - "Software Engineer I, Recent Graduate (remote or Irvine/NYC; Ashby req 5618f1de...; posted 2024-12-10, target start ~2025-03-01 — current-cycle status unverified)"
    - "Software Engineer / Software Engineer II / Sr. Software Engineer / Sr. SRE / Sr. Data Analyst / Engineering Manager (titles seen in H-1B LCA data)"
  roles_in_region: "Yes — Irvine HQ (optional office); most eng roles remote-or-Irvine."
  new_grad: "Strong — dedicated 'Software Engineer I, Recent Graduate' requisition on Ashby (also syndicated to ZipRecruiter, BuiltIn NYC, startup.jobs). Whether a 2026-27 cycle is open right now is unverified."
  ats: Ashby
  ats_id: "Acorns (jobs.ashbyhq.com/Acorns)"
  careers_url: "https://www.acorns.com/careers/"
  h1b: "strong — h1bdata: Acorns Grow Inc 93 records, median $160,000 (27% >$200K); top LCA titles SWE II (18), SWE (10), Sr. Data Analyst (7), Sr. SWE (7); SWE II median $161,679 (Irvine, 2024)."
  news: "Acquired EarlyBird (May 2025) and Zeta (June 2025) after GoHenry (2023); recurring IPO speculation (previous SPAC deal abandoned). No layoffs surfaced in searches."
  fit: "Top fit: consumer investing/banking in Irvine, a recent-grad SWE track, and a clear, well-paid H-1B record. Python/React and portfolio-monitoring SaaS experience map directly."
  sources:
    - https://jobs.ashbyhq.com/Acorns/5618f1de-cf18-4114-9408-11cd73153a9d
    - https://www.ziprecruiter.com/c/Acorns/Job/Software-Engineer-(Recent-Graduate)/-in-Irvine,CA?jid=251cf2c275bcdfec
    - https://www.builtinnyc.com/job/software-engineer-i-recent-graduate/4445004
    - https://www.acorns.com/careers/
    - https://h1bdata.info/index.php?em=acorns+grow+inc&job=
    - https://h1bdata.info/index.php?city=irvine&em=acorns+grow+incorporated&job=software+engineer+ii&year=2024
    - https://visa.1point3acres.com/h1b/salary/acorns-grow-incorporated
    - https://h1bgrader.com/h1b-sponsors/acorns-grow-incorporated-6g0648jp2q/salaries
    - https://forgeglobal.com/acorns_ipo/
    - https://fintech.global/tag/acorns/

- name: PennyMac Financial Services
  city: Westlake Village (HQ); tech also Moorpark / Agoura Hills; rotational postings also in Cary NC and Carrollton TX
  region: LA
  category: lending_credit
  roles:
    - "Technology Rotation Engineer I (Westlake Village; careers.pennymac.com job 37785)"
    - "Digital Technology Organization (DTO) Rotational Program - Engineer (January or June 2027 cohorts; teams: Cloud Platform Eng, DevOps, App Dev in Finance & Enterprise Risk, IT Data Analytics)"
    - "Associate Engineer, Software Rotation (LinkedIn)"
    - "Sr Application Developer ($90K-$150K), Sr DevOps Engineer ($95K-$155K) — Westlake Village"
    - "SVP, Software Engineering (Westlake Village, job 34956)"
  roles_in_region: "Yes — Westlake Village / Moorpark tech hub (LA County / Ventura line). Some rotational reqs are posted for NC/TX, so confirm the location for each req."
  new_grad: "Strong — the DTO / Tech Rotational Program targets recent grads (Java/Python/C++). USC Viterbi advertised it to UG/MS/PhD students; the 2027 cohort application is live. Contact: CampusRecruiting@pennymac.com."
  ats: iCIMS (front end careers.pennymac.com)
  ats_id: "careers-pennymac.icims.com"
  careers_url: "https://www.pennymac.com/techjobs"
  h1b: "unknown — searches returned no PennyMac-specific LCA data; ask campus recruiting whether the rotational program sponsors."
  news: "No layoffs or major news checked in this session."
  fit: "Best new-grad entry point found in LA-area lending: a structured rotation that includes Finance & Enterprise Risk app dev. The unanswered question is sponsorship."
  sources:
    - https://careers.pennymac.com/jobs/37785?lang=en-us&previousLocale=en-US
    - https://careers.pennymac.com/students-graduates
    - https://www.cs.usc.edu/newsletter/ug-ms-phd-pennymac-tech-rotational-program/
    - https://www.glassdoor.com/job-listing/digital-technology-organization-rotational-program-engineer-position-pennymac-JV_IC1138945_KO0,68_KE69,77.htm?jl=1009866307353
    - https://www.theladders.com/job/digital-technology-organization-rotational-program-engineer-position-pennymacfinancialservicesinc-carrollton-tx_83172618
    - https://www.linkedin.com/jobs/view/associate-engineer-software-rotation-at-pennymac-4136208831
    - https://careers.pennymac.com/jobs/34956?lang=en-us
    - https://careers-pennymac.icims.com/jobs/intro
    - https://www.pennymac.com/techjobs
    - https://www.ziprecruiter.com/co/Pennymac/Jobs/-in-Westlake-Village,CA?id=zUWwEa5W+btGzo_I8d_+DmU4fTY%3D

- name: Experian (North America HQ)
  city: Costa Mesa
  region: OC
  category: credit_data
  roles:
    - "Software Engineer Xcelerator Rotation Program (Entry Level SWE) - Remote, US (jid-3269)"
    - "Data & Analytics Xcelerator Program (Entry Level Data Analytics) - Remote, US (jid-3270)"
    - "Product Management Xcelerator Rotation Program - Remote, US (jid-3288)"
    - "Technical Program Associate (HYBRID) - Costa Mesa (jid-3318)"
    - "Staff Software Engineer - Costa Mesa (jid-1246; $115,747-$208,344)"
    - "Software Development Engineer Senior - Costa Mesa (jid-1178)"
    - "Software Development Staff Engineer - Costa Mesa (jid-1367)"
    - "Staff Software Engineer, Frontend - Costa Mesa (jid-1245)"
  roles_in_region: "Yes for senior and hybrid roles in Costa Mesa. The entry-level Xcelerator reqs are listed as Remote-US. Many SmartRecruiters SWE reqs are overseas (Hyderabad, Sofia, Cyberjaya, Nottingham)."
  new_grad: "Good — 12-month Xcelerator program with two 6-month rotations (SWE / Data & Analytics / PM) and April and June start dates. Sponsorship policy for Xcelerator not visible in snippets (unverified)."
  ats: SmartRecruiters (front end jobs.experian.com)
  ats_id: "Experian (jobs.smartrecruiters.com/Experian)"
  careers_url: "https://www.experian.com/careers/early-careers/north-america"
  h1b: "strong — 1point3acres: Experian Services Corporation 75 records, median $108,608, Costa Mesa a top city; h1bdata 2021: Experian Information Solutions Inc 121 records, median $132K."
  news: "Small rolling Costa Mesa WARN layoffs: 35 (effective 2026-03-23, mostly admin/support), 38 (filed 2026-03-30, effective 2026-05-22), plus a 28-person notice effective in December (year per source unverified)."
  fit: "Credit bureau with fraud, lending and decisioning data at scale. The Python/Java/data profile fits, and the Xcelerator program is the clearest new-grad route, but it may be remote rather than Costa Mesa."
  sources:
    - https://jobs.experian.com/job/software-engineer-xcelerator-rotation-program-entry-level-swe-remote-in-united-states-jid-3269
    - https://jobs.experian.com/job/data-and-analytics-xcelerator-program-entry-level-data-analytics-remote-in-united-states-jid-3270
    - https://jobs.experian.com/job/technical-program-associate-hybrid-in-costa-mesa-united-states-jid-3318
    - https://jobs.experian.com/job/staff-software-engineer-in-costa-mesa-united-states-jid-1246
    - https://jobs.experian.com/job/software-development-engineer-senior-in-costa-mesa-united-states-jid-1178
    - https://jobs.experian.com/job/software-development-staff-engineer-in-costa-mesa-united-states-jid-1367
    - https://jobs.experian.com/job/staff-software-engineer-frontend-in-costa-mesa-united-states-jid-1245
    - https://www.experian.com/careers/early-careers/north-america
    - https://careers.smartrecruiters.com/Experian?remoteLocation=true
    - https://jobs.smartrecruiters.com/Experian/744000143860629-software-engineer-i
    - https://visa.1point3acres.com/h1b/salary/experian-services-corporation
    - https://h1bdata.info/index.php?year=2021&em=experian+information+solutions+inc
    - https://www.warntracker.com/layoff/experian-2026-05-22
    - https://www.kadoa.com/layoffs/company/experian
    - https://whatnow.com/orange-county/local-news/30-year-old-data-and-technology-company-announces-28-layoffs-at-costa-mesa-location/

- name: East West Bank
  city: Pasadena (HQ); operations also in El Monte
  region: LA
  category: bank
  roles:
    - "Release Automation Engineer; Quantitative Analyst (Pasadena); Data Engineer (Glassdoor salary entries); Senior Network Engineer (snippet-level; no specific 2026 req IDs captured)"
  roles_in_region: "Yes — Pasadena / El Monte (100+ Pasadena openings of all types on job boards, Aug-Sep 2026)."
  new_grad: "Moderate — the bank advertises internships and trainee programs; whether any are tech-specific is unverified."
  ats: iCIMS
  ats_id: "careers-eastwestbank.icims.com"
  careers_url: "https://www.eastwestbank.com/en/careers/opportunities"
  h1b: "strong — h1bdata: 81 Pasadena records (2024 view), median $85,000 (74% under $100K); 2020: 46 records, median $132,500; 2021: 57 records, median ~$136,386."
  news: "Not checked in session."
  fit: "Chinese-American bank with US-China business. Mandarin is a real differentiator, and it is a steady H-1B filer. Look at risk/quant/data and core-banking tech. Salaries are lower than at fintechs."
  sources:
    - https://careers-eastwestbank.icims.com/jobs/intro
    - https://www.eastwestbank.com/en/careers/opportunities
    - https://h1bdata.info/index.php?em=east+west+bank&city=pasadena
    - https://h1bdata.info/index.php?year=2021&em=EAST+WEST+BANK
    - https://h1bdata.info/index.php?em=EAST+WEST+BANK&year=2020
    - https://h1bgrader.com/h1b-sponsors/east-west-bank-510jqgvl2v
    - https://www.glassdoor.com/Jobs/East-West-Bank-Pasadena-Jobs-EI_IE9089.0,14_IL.15,23_IC1146850.htm
    - https://www.glassdoor.com/Salary/East-West-Bank-Data-Engineer-Salaries-E9089_D_KO15,28.htm

- name: Zest AI (ZestFinance Inc.)
  city: Burbank
  region: LA
  category: lending_credit
  roles:
    - "Software Engineer (Burbank; Greenhouse jobs 5645115004 / 5591251004)"
    - "Machine Learning Engineer (Burbank)"
  roles_in_region: "Yes — Burbank."
  new_grad: "unknown — seniority of the posted SWE req not visible in snippets."
  ats: Greenhouse
  ats_id: "zestai (job-boards.greenhouse.io/zestai)"
  careers_url: "https://job-boards.greenhouse.io/zestai"
  h1b: "some — h1bdata: ZestFinance Inc 63 records, median $135,000; Burbank 6 records, median $142,150; h1bgrader also lists 'ZestFinance Inc dba ZestAI'."
  news: "None surfaced in session."
  fit: "AI credit underwriting for banks and credit unions. The Python + ML + Optuna + backtesting profile is a natural match. Small company, so openings are sporadic."
  sources:
    - https://job-boards.greenhouse.io/zestai/jobs/5645115004
    - https://job-boards.greenhouse.io/zestai/jobs/5591251004
    - https://h1bdata.info/index.php?em=zestfinance+inc
    - https://h1bdata.info/index.php?em=zestfinance+inc&city=burbank
    - https://h1bgrader.com/h1b-sponsors/zestfinance-inc-dba-zestai-10j7qpmg0v
    - https://www.myvisajobs.com/Visa-Sponsor/Zestfinance/1172428.htm

- name: Tala (Inventure Capital Corporation dba Tala)
  city: Santa Monica (HQ hub; remote-first)
  region: LA
  category: lending_credit
  roles:
    - "Data Platform Engineer I (builds the data platform behind Tala's credit decision engine; works with ML engineers, data scientists and analytics engineers)"
  roles_in_region: "Santa Monica HQ hub; remote-first company, so roles may be remote-US."
  new_grad: "Moderate — an 'Engineer I' level posting seen."
  ats: Lever
  ats_id: "tala (jobs.lever.co/tala)"
  careers_url: "https://jobs.lever.co/tala"
  h1b: "some — MyVisaJobs: Inventure Capital Corporation dba Tala filed 33 LCAs + 7 PERM (FY2022-24); visa-bulletin.us shows 100% approval rate, median ~$166K."
  news: "June 2026: cutting ~10% of Kenya staff (~95) in a global reorganisation that centralises functions at global HQ and shifts toward embedded finance. April 2025: 28 Kenya customer-ops layoffs."
  fit: "Mobile credit and decisioning ML for emerging markets. Signal/backtest/data-pipeline experience fits the data platform role. The small US team is being centralised, which could favour HQ hiring."
  sources:
    - https://jobs.lever.co/tala/82efbb9a-44ab-48e6-a578-5073dcb7e41c
    - https://www.myvisajobs.com/employer/inventure-capital/
    - https://visa-bulletin.us/employer/inventure-capital-corporation-dba-tala-1/
    - https://techweez.com/2026/06/25/tala-kenya-layoffs-global-restructuring/
    - https://www.ecofinagency.com/news-finances/2606-56843-tala-is-pulling-work-out-of-kenya-and-that-matters-more-than-the-100-jobs-its-cutting
    - https://en.wikipedia.org/wiki/Tala_Finance

- name: Dave Inc.
  city: Los Angeles
  region: LA
  category: fintech
  roles:
    - "Senior Software Engineer, Backend (owns Dave Bank accounts, debit cards, payment processing, sponsor-bank/processor integrations)"
    - "Senior Software Engineer, Fullstack"
    - "Staff AI Acceleration Engineer"
    - "Data Engineering roles (11 openings total as of Sep 2026 per snippet)"
  roles_in_region: "LA HQ; remote status per req unverified."
  new_grad: "Low — only senior and staff postings seen."
  ats: Ashby
  ats_id: "dave (jobs.ashbyhq.com/dave)"
  careers_url: "https://dave.com/careers"
  h1b: "some — 1point3acres: Dave Inc median $160,096 (top titles Sr SWE, Technical Team Lead, Data Scientist); Dave Operating LLC median $174,341; combined ~26% of LCAs under $100K."
  news: "Gopi Kuchimanchi appointed CTO (July 2026); a BNPL product is planned for 2026. The CEO has said Dave is hiring carefully but not planning cuts, and uses AI and Copilot for engineering efficiency."
  fit: "Excellent domain match (cash-advance underwriting, payments, banking core), but the openings are senior. Worth an early-career or referral approach."
  sources:
    - https://jobs.ashbyhq.com/dave/75e61fb3-3883-4d8f-8c2d-44f75ef9fc1a
    - https://builtin.com/job/senior-software-engineer-backend/10558585
    - https://www.dreamworkhq.com/job/44aad89f-c60c-4572-9e16-b193b84934aa
    - https://dave.com/careers
    - https://visa.1point3acres.com/h1b/salary/dave-inc
    - https://h1bdata.info/index.php?em=dave+inc
    - https://h1bgrader.com/h1b-sponsors/dave-operating-llc-g06npd1mkq/lca/2023
    - https://investors.dave.com/news-events/news-releases
    - https://www.americanbanker.com/news/how-ai-is-affecting-neobank-jobs

- name: Cotality (formerly CoreLogic)
  city: Irvine (HQ, 40 Pacifica Suite 900)
  region: OC
  category: credit_data
  roles:
    - "Sr. Professional, Software Engineering (Irvine, REQ18549)"
    - "Executive, Software Engineering (Irvine; $175.5K-$241.5K)"
    - "Senior Software Engineer; Principal Software Engineer (Irvine listings on Glassdoor / ZipRecruiter, 2025-26)"
  roles_in_region: "Yes — Irvine HQ; many postings say 100% remote within the US is allowed."
  new_grad: "Low — only Sr., Principal and Executive postings seen; no early-career program surfaced."
  ats: Workday
  ats_id: "cotality.wd5.myworkdayjobs.com (site: Global)"
  careers_url: "https://www.cotality.com/careers"
  h1b: "some — CoreLogic Solutions LLC: 107 LCAs across 9 states (Ellis), overall median ~$127K; 'Sr. Professional, Software Engineer' H-1B median $115,717. Filings are under legacy CoreLogic entity names."
  news: "Rebranded from CoreLogic to Cotality on 2025-03-24 (private since 2021). Glassdoor reviews describe recurring annual layoffs; no specific 2026 event confirmed."
  fit: "Property, mortgage and insurance risk data in Irvine. A reasonable data-engineering fit, but the postings are senior-leaning and the culture is remote-first."
  sources:
    - https://cotality.wd5.myworkdayjobs.com/en-US/Global/job/Irvine-CA/Sr-Professional--Software-Engineering_REQ18549-1
    - https://www.ziprecruiter.com/c/Cotality/Job/Executive,-Software-Engineering/-in-Irvine,CA?jid=8b9e5759fa52b5f3
    - https://www.glassdoor.com/Jobs/Cotality-Jobs-E30994.htm
    - https://www.cotality.com/careers
    - https://h1bdata.info/index.php?em=corelogic+solutions+llc
    - https://www.ellis.com/visa-sponsors/corelogic-solutions-llc/h1b
    - https://www.cotality.com/press-releases/meet-cotality
    - https://www.nationalmortgagenews.com/news/corelogic-renamed-cotality-four-years-after-going-private
    - https://www.glassdoor.com/Reviews/Cotality-layoff-Reviews-EI_IE30994.0,8_KH9,15.htm

- name: BlackLine
  city: Woodland Hills (HQ, Los Angeles); engineering also Pleasanton CA, Washington state, India
  region: LA
  category: fintech
  roles:
    - "Staff I Software Engineer (Los Angeles, job 6621)"
    - "Senior Software Engineer (Los Angeles, job 2970)"
    - "Staff II Software Engineer - Python/Agentic AI (Washington, job 7491)"
    - "Software Engineer AI/ML Ops (Pleasanton, job 7510); Sr/Senior Software Engineer (Pleasanton, jobs 7106, 7441); Staff Software Engineer (Washington, job 7506)"
  roles_in_region: "Some — LA postings are Senior or Staff. The more junior-sounding AI/ML Ops role is in Pleasanton (NorCal fallback)."
  new_grad: "Low — senior-heavy; cloud-engineering internships mentioned."
  ats: "Jibe-style front end at careers.blackline.com. A search snippet labels it 'Myworkdayjobs', so the backend is probably Workday (unverified)."
  ats_id: "careers.blackline.com/careers-home/jobs/<id>"
  careers_url: "https://careers.blackline.com/product-technology"
  h1b: "strong — h1bdata: Blackline Systems Inc 231 records, median $134,992; FY2024 median $118,165 (h1bgrader); not H-1B dependent."
  news: "SAP offered ~$4.5B and was rejected (June 2025), and reportedly weighed a new bid (Oct 2025). Employee forums and TrueUp report a ~7-9% layoff around Dec 2025 and repeated cuts (exact figures unverified). Acquired Wiselayer."
  fit: "Finance-operations SaaS in LA with a good sponsorship record, but the openings are senior and there is layoff and M&A risk."
  sources:
    - https://careers.blackline.com/careers-home/jobs/6621?lang=en-us
    - https://careers.blackline.com/careers-home/jobs/2970?lang=en-us
    - https://careers.blackline.com/careers-home/jobs/7491?lang=en-us
    - https://careers.blackline.com/careers-home/jobs/7510?lang=en-us
    - https://careers.blackline.com/product-technology
    - https://h1bdata.info/index.php?em=blackline+systems+inc
    - https://h1bgrader.com/h1b-sponsors/blackline-systems-inc-5g2rlpz32l
    - https://www.techzine.eu/news/applications/135798/sap-makes-bid-worth-billions-for-blackline/
    - https://www.trueup.io/co/blackline/layoffs
    - https://www.thelayoff.com/t/1kbkamxxz

- name: FloQast
  city: Los Angeles (Sherman Oaks HQ); many roles US-remote
  region: LA
  category: fintech
  roles:
    - "Principal Software Engineer, Applications (Lever)"
    - "Staff Software Engineer ($185K-$301K base)"
    - "Software Engineer, Mid-level (Consolidation); Software Development Engineer in Test II (BuiltIn)"
    - "Software Engineer I (older BuiltIn posting); US-remote Software Engineer (removed May 2025)"
  roles_in_region: "LA HQ; engineering roles are often US-remote."
  new_grad: "Low-moderate — an SE I req existed historically; current openings are senior."
  ats: Lever
  ats_id: "floqast (jobs.lever.co/floqast)"
  careers_url: "https://jobs.lever.co/floqast"
  h1b: "some — h1bgrader: FloQast Inc FY2026 LCA median $226,138 (suggests sponsorship at senior levels only)."
  news: "~850 employees (2026); positions itself as an AI accounting-transformation platform."
  fit: "Accounting-automation fintech. Less of a trading or pricing flavour, and sponsorship evidence is senior-only."
  sources:
    - https://jobs.lever.co/floqast/447eefa9-923a-444a-afd7-d880cfcc2151
    - https://builtin.com/job/software-engineer-i/3009315
    - https://builtin.com/job/software-engineer-ii-consolidation/3197124
    - https://builtin.com/job/software-development-engineer-test-ii/6250193
    - https://h1bgrader.com/h1b-sponsors/floqast-inc-okpre7vy24/salaries/2026
    - https://www.levels.fyi/companies/floqast/salaries/software-engineer
    - https://en.wikipedia.org/wiki/FloQast

- name: First American Financial Corporation
  city: Santa Ana
  region: OC
  category: insurance
  roles:
    - "Software Engineer (Santa Ana, R051099, posted 2025-06-19)"
    - "Software Engineer Lead (Hybrid) (Santa Ana, R055973, posted 2026-06-03; 3 days/week on-site)"
    - "Senior Software Engineer (Santa Ana, R053803)"
    - "Software Engineering Intern - REMOTE (R054629, posted 2026-02-18, summer 2026); Data Engineering Intern - REMOTE; Intern (Backend Software Engineering-Remote) R042842; Software Development Intern R043098"
  roles_in_region: "Yes — Santa Ana HQ with hybrid engineering roles."
  new_grad: "Moderate — structured 8-10 week internship (mentors, buddies, Intern Expo Day) for Bachelor's students; no new-grad SWE req seen."
  ats: Workday (front end careers.firstam.com)
  ats_id: "firstam.wd1.myworkdayjobs.com (site: firstamericancareers)"
  careers_url: "https://careers.firstam.com/technology-careers"
  h1b: "some (thin evidence) — h1bdata lists LCAs for 'First American Title Insurance Company', including a Lead Data Engineer in Santa Ana (~$151.7K). No SWE counts seen. The 0-LCA MyVisaJobs entry 'First American Financial & Investment' looks like a different entity."
  news: "Company cites 10 straight years on Fortune 100 Best Companies to Work For. No 2026 layoffs checked."
  fit: "Title and settlement fintech in Santa Ana with hybrid engineering. A steady employer, but less money-markets focused."
  sources:
    - https://careers.firstam.com/job/santa-ana/software-engineer/39054/82742984080
    - https://careers.firstam.com/job/santa-ana/software-engineer-lead-hybrid/39054/94309458208
    - https://firstam.wd1.myworkdayjobs.com/firstamericancareers/job/USA-California-Santa-Ana/Senior-Software-Engineer_R053803
    - https://careers.firstam.com/job/santa-ana/software-engineering-intern-remote/39054/91871549328
    - https://careers.firstam.com/job/santa-ana/data-engineering-intern-remote/39054/91950498096
    - https://careers.firstam.com/technology-careers
    - https://www.h1bdata.info/index.php?em=first+american+title+insurance+company
    - https://www.myvisajobs.com/employer/first-american-financial-investment/

- name: loanDepot
  city: Irvine (HQ; mello tech center on Irvine Center Drive); also Plano TX
  region: OC
  category: lending_credit
  roles:
    - "Lead Software Engineer (mello digital mortgage platform)"
    - "Senior Software Development Engineer in Test"
    - "Lead Front End Software Engineer (Angular/React; $138K-$191K)"
    - "Software Engineer, Technology Solutions (careers.loandepot.com job-detail/6199)"
    - "13 Senior Software Engineer openings in Irvine (ZipRecruiter, Jul 2026)"
  roles_in_region: "Yes — Irvine."
  new_grad: "Low — senior and lead roles dominate."
  ats: Jobvite (front end careers.loandepot.com)
  ats_id: "loandepot (jobs.jobvite.com/loandepot)"
  careers_url: "https://careers.loandepot.com"
  h1b: "some — 1point3acres: loanDepot.com LLC 51 records, median $114,080; top cities Plano and Irvine."
  news: "Years of large layoffs as mortgage volumes fell ('Vision 2025' plan) and a return-to-office policy. Employee reviews describe upheaval in the tech department. No specific 2026 tech layoff confirmed."
  fit: "Direct lending tech in Irvine and a good domain match, but a volatile employer with senior-weighted openings."
  sources:
    - https://careers.loandepot.com/job-detail/6199
    - https://jobs.jobvite.com/loandepot/search?l=Irvine,+CA+-+Irvine+Center+Drive+(mello)
    - https://www.ziprecruiter.com/co/loandepot/Jobs/Senior-Software-Engineer/-in-Irvine,CA
    - https://visa.1point3acres.com/h1b/salary/loandepot-com-llc
    - https://h1bgrader.com/h1b-sponsors/loandepot-60eq6zq90z/salaries/2025
    - https://www.doddfrankupdate.com/dfu/articlesdfu/loandepot-lays-off-thousands-as-part-of-new-strate-85809.aspx
    - https://www.insidemortgagefinance.com/articles/227842-loandepot-institutes-rto-policy-more-layoffs?v=preview
    - https://www.glassdoor.com/Reviews/loanDepot-layoff-Reviews-EI_IE375743.0,9_KH10,16.htm

- name: Hyundai Capital America
  city: Irvine (HQ, 3161 Michelson Dr)
  region: OC
  category: lending_credit
  roles:
    - "Sr. Software Developer (Salesforce) (Irvine; $132K-$205K; posted 2026-07-02)"
    - "Sr. AI Agent / Prompt Engineer"
    - "Application Developer Associate, Insurance Platform (SQL, PL/SQL)"
    - "Manager, Software Developer (Blaze) (H-1B LCA title, FY2025)"
  roles_in_region: "Yes — about 32 Irvine openings of all types on ZipRecruiter."
  new_grad: "Low-moderate — 'Associate' developer titles exist; no formal new-grad program seen."
  ats: unknown
  ats_id: "unknown — no myworkdayjobs hits; careers page is hyundaicapitalamerica.com"
  careers_url: "https://www.hyundaicapitalamerica.com/Careers.html"
  h1b: "some but cooling — h1bgrader FY2025 median $149,781 (another view: 43 records, median $130,749). Snippet says 0 LCAs filed in FY2026."
  news: "None checked."
  fit: "Auto lending, leasing and insurance tech in Irvine with some AI work. H-1B appetite looks weak in 2026."
  sources:
    - https://www.glassdoor.com/job-listing/sr-software-developer-salesforce-hyundai-capital-america-JV_IC1146798_KO0,32_KE33,56.htm?jl=1010188704906
    - https://www.ziprecruiter.com/co/Hyundai-Capital-America/Jobs/-in-Irvine,CA
    - https://www.hyundaicapitalamerica.com/Careers.html
    - https://h1bgrader.com/h1b-sponsors/hyundai-capital-america-x30qpq98kq
    - https://h1bgrader.com/h1b-sponsors/hyundai-capital-america-x30qpq98kq/salaries/2025
    - https://h1bgrader.com/h1b-sponsors/hyundai-capital-america-x30qpq98kq/lca/manager-software-developer-blaze-30qjjpv8kq/c/2025
    - https://h1bdata.info/index.php?em=hyundai+capital+america

- name: American Honda Finance Corp (Honda Financial Services)
  city: Torrance
  region: LA
  category: lending_credit
  roles:
    - "Unit Manager, Dealer and Field applications (leads software teams for sales/service/parts/financing platforms; Torrance)"
    - "Mostly analyst/accounting roles seen; tech sits largely in American Honda Motor IT"
  roles_in_region: "Yes — Torrance main campus."
  new_grad: "unknown"
  ats: "careers.honda.com portal (underlying ATS unverified)"
  ats_id: "careers.honda.com/us/en"
  careers_url: "https://careers.honda.com/us/en"
  h1b: "minimal — American Honda Motor Co Inc filed 4 LCAs in FY2025 (h1bgrader). No finance-arm-specific data found."
  news: "None checked."
  fit: "Captive auto finance with a weak sponsorship signal. Low priority."
  sources:
    - https://careers.honda.com/us/en
    - https://careers.honda.com/us/en/search-results
    - https://www.ziprecruiter.com/Jobs/American-Honda-Finance/-in-Torrance,CA
    - https://h1bgrader.com/h1b-sponsors/american-honda-motor-co-inc-d0g9w44wko
    - https://www.myvisajobs.com/employer/american-honda-motor/

- name: Auto Club Enterprises (AAA - Automobile Club of Southern California) [discovered incidentally]
  city: Costa Mesa
  region: OC
  category: insurance
  roles:
    - "Cloud Data DevOps Engineer (Costa Mesa, CA / Remote; JR202634087)"
  roles_in_region: "Yes — Costa Mesa."
  new_grad: "unknown"
  ats: Workday
  ats_id: "ace.wd5.myworkdayjobs.com (site: careers)"
  careers_url: "https://ace.wd5.myworkdayjobs.com/careers"
  h1b: "unknown"
  news: "Not checked."
  fit: "Auto and home insurance data work in Costa Mesa. Lower priority; seen by chance while searching for Experian."
  sources:
    - https://ace.wd5.myworkdayjobs.com/careers/job/Costa-Mesa-CA--Remote/Cloud-Data-DevOps-Engineer_JR202634087-1

# ---------------- UNVERIFIED entries (search budget exhausted; prior knowledge only) ----------------

- name: Riot Games
  city: "Los Angeles (West LA HQ) — UNVERIFIED (prior knowledge)"
  region: LA
  category: game_economy
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: commerce/store, payments and anti-fraud, player platform, economy/monetization, data science and analytics teams for LoL/Valorant/TFT."
  roles_in_region: "UNVERIFIED — HQ engineering is in LA."
  new_grad: "UNVERIFIED — has historically run internships and associate-level hiring."
  ats: "UNVERIFIED guess: Greenhouse"
  ats_id: "UNVERIFIED guess: riotgames — verify"
  careers_url: "UNVERIFIED — riotgames.com work-with-us jobs page"
  h1b: "unknown in session (prior knowledge: historically a regular H-1B filer)"
  news: "UNVERIFIED (prior knowledge): Tencent-owned; Jan 2024 layoff of ~530 staff (~11%)."
  fit: "Potentially strong for a virtual-economy and pricing background. Mandarin could help with China/Tencent-linked work. Re-verify first."
  sources: []

- name: Blizzard Entertainment
  city: "Irvine (HQ) — UNVERIFIED (prior knowledge)"
  region: OC
  category: game_economy
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: Battle.net commerce/shop and payments, anti-fraud, data engineering and analytics, and game economy/monetization for WoW, Diablo, Overwatch and Hearthstone."
  roles_in_region: "UNVERIFIED — Irvine campus."
  new_grad: "UNVERIFIED — has historically hired interns and associates."
  ats: "UNVERIFIED guess: Workday (Activision Blizzard tenant)"
  ats_id: "UNVERIFIED guess: activision.wd1.myworkdayjobs.com / External — verify"
  careers_url: "UNVERIFIED — careers.blizzard.com"
  h1b: "unknown in session (prior knowledge: historically a significant filer)"
  news: "UNVERIFIED (prior knowledge): part of Microsoft Gaming since Oct 2023; hit by the Jan 2024 Microsoft Gaming layoffs (~1,900) and later Microsoft cuts. Check 2026 hiring status."
  fit: "The only large game-economy employer in Irvine, and closest to the candidate. The Diablo/WoW auction-house-style economies match the CS2 market-agent project. Layoff risk is high, so verify first."
  sources: []

- name: Whatnot
  city: "Los Angeles (Marina del Rey roots; 'remote co-located' hubs) — UNVERIFIED (prior knowledge)"
  region: LA
  category: marketplace
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: marketplace/payments, trust & safety, pricing and seller tools, data/ML."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED — prior knowledge suggests occasional new-grad SWE reqs."
  ats: "UNVERIFIED guess: Ashby"
  ats_id: "UNVERIFIED guess: whatnot — verify"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): $265M Series E at ~$5B valuation (Jan 2025); fast-growing live-commerce marketplace for trading cards and collectibles."
  fit: "Collectibles and trading-card marketplace. Very close to the CS2-skins market work. High priority to verify."
  sources: []

- name: GOAT Group
  city: "Culver City (HQ) — UNVERIFIED (prior knowledge)"
  region: LA
  category: marketplace
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: marketplace pricing/data, payments, fraud and authentication, search."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: "UNVERIFIED guess: Greenhouse"
  ats_id: "UNVERIFIED guess: goatgroup — verify"
  careers_url: "UNVERIFIED"
  h1b: "unknown (prior knowledge: legal entity may file as '1661, Inc.')"
  news: "UNVERIFIED"
  fit: "Resale marketplace with bid/ask price discovery, analogous to skins trading. Verify openings."
  sources: []

- name: Collectors (PSA, PCGS, Goldin)
  city: "Santa Ana (HQ) — UNVERIFIED (prior knowledge)"
  region: OC
  category: marketplace
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: collectibles grading plus marketplace/auction (Goldin), vault and price-guide/valuation data products."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): taken private in 2021 and expanded via acquisitions (e.g., Goldin)."
  fit: "Collectible pricing and valuation data in OC. Strong thematic fit with the virtual-item market work. Verify."
  sources: []

- name: Pacific Life
  city: "Newport Beach (HQ) — UNVERIFIED (prior knowledge)"
  region: OC
  category: insurance
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: software engineering, data/analytics, investments and annuity technology."
  roles_in_region: "UNVERIFIED — Newport Beach HQ (also Omaha/Lincoln offices)."
  new_grad: "UNVERIFIED — prior knowledge suggests internships."
  ats: "UNVERIFIED guess: Workday"
  ats_id: "UNVERIFIED guess: pacificlife.wd1.myworkdayjobs.com — verify"
  careers_url: "UNVERIFIED"
  h1b: "unknown in session (prior knowledge: files LCAs)"
  news: "UNVERIFIED"
  fit: "Insurance and investments tech in OC. Worth checking for data and investment-tech roles."
  sources: []

- name: LPL Financial
  city: "San Diego (major HQ office) — UNVERIFIED (prior knowledge)"
  region: SD
  category: fintech
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: large technology org in San Diego (advisor platforms, trading/brokerage tech, data)."
  roles_in_region: "UNVERIFIED — San Diego, plus Fort Mill SC and Austin TX."
  new_grad: "UNVERIFIED"
  ats: "UNVERIFIED guess: Workday"
  ats_id: "UNVERIFIED guess: lplfinancial.wd1.myworkdayjobs.com — verify"
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): acquired Commonwealth Financial Network (announced 2025)."
  fit: "Brokerage and trading-platform tech in San Diego (fallback region)."
  sources: []

- name: Brandes Investment Partners
  city: "San Diego — UNVERIFIED (prior knowledge)"
  region: SD
  category: other
  roles:
    - "UNVERIFIED — not searched. Small asset manager; tech hiring likely sparse."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED"
  fit: "Investment management; low volume of engineering roles."
  sources: []

- name: Cathay Bank
  city: "Los Angeles (HQ, Chinatown); operations El Monte — UNVERIFIED (prior knowledge)"
  region: LA
  category: bank
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: IT application development, data/BI, credit-risk and BSA/AML analytics."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED"
  fit: "Chinese-American bank where Mandarin is an asset. Check tech and risk openings and sponsorship directly."
  sources: []

- name: Preferred Bank
  city: "Los Angeles (downtown HQ) — UNVERIFIED (prior knowledge)"
  region: LA
  category: bank
  roles:
    - "UNVERIFIED — not searched. Small IT team."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED"
  fit: "Chinese-American commercial bank where Mandarin helps. Few engineering roles."
  sources: []

- name: City National Bank (RBC)
  city: "Los Angeles (downtown HQ) — UNVERIFIED (prior knowledge)"
  region: LA
  category: bank
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: sizeable tech/data org."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): RBC subsidiary; 2024 OCC penalty over risk-management deficiencies and subsequent restructuring and layoffs."
  fit: "Large LA bank. Verify tech openings and sponsorship."
  sources: []

- name: Banc of California
  city: "Los Angeles (HQ after 2023 PacWest merger) — UNVERIFIED (prior knowledge)"
  region: LA
  category: bank
  roles:
    - "UNVERIFIED — not searched. Prior knowledge: owns a payments-processing unit (Deepstack) — verify."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): merged with PacWest (2023)."
  fit: "Regional bank; the payments unit could be interesting if confirmed."
  sources: []

- name: SchoolsFirst Federal Credit Union
  city: "Santa Ana / Tustin — UNVERIFIED (prior knowledge)"
  region: OC
  category: bank
  roles:
    - "UNVERIFIED — not searched."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown (credit unions rarely sponsor — verify)"
  news: "UNVERIFIED"
  fit: "Large OC credit union; sponsorship is doubtful."
  sources: []

- name: Farmers Insurance (Farmers Group)
  city: "Woodland Hills (HQ) — UNVERIFIED (prior knowledge)"
  region: LA
  category: insurance
  roles:
    - "UNVERIFIED — not searched."
  roles_in_region: "UNVERIFIED — tech may be split across several US hubs."
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED (prior knowledge): ~2,400 layoffs in 2023; Zurich-affiliated."
  fit: "Insurance pricing and data roles are possible. Verify."
  sources: []

- name: Mercury Insurance
  city: "Los Angeles (HQ); IT campus in Brea (OC) — UNVERIFIED (prior knowledge)"
  region: LA
  category: insurance
  roles:
    - "UNVERIFIED — not searched."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "UNVERIFIED"
  h1b: "unknown"
  news: "UNVERIFIED"
  fit: "Auto and home insurer; pricing and data roles are possible. Verify."
  sources: []

- name: "Crypto / trading platforms in LA-OC"
  city: "n/a"
  region: LA
  category: crypto
  roles:
    - "UNVERIFIED — no LA/OC crypto or trading-platform employer confirmed in this session (searches not run)."
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "n/a"
  h1b: "unknown"
  news: "n/a"
  fit: "Most US crypto and trading-app engineering is in SF, NYC or remote. Remote roles at those firms are the realistic path."
  sources: []

- name: "Unverified leads worth checking (not on original list)"
  city: "various"
  region: SD
  category: other
  roles:
    - "Intuit (San Diego campus; TurboTax/Credit Karma; historically strong new-grad hiring and H-1B filer) — UNVERIFIED"
    - "Axos Bank, Kyriba (treasury SaaS), Encore Capital Group (credit/collections analytics), Mitek (identity/check capture) — San Diego — UNVERIFIED"
    - "Scopely and Jam City (Culver City; mobile-game economies/monetization), Activision (Santa Monica) — UNVERIFIED"
    - "TrueCar and Edmunds (Santa Monica; car-pricing marketplaces), Wedbush Securities (LA brokerage tech) — UNVERIFIED"
  roles_in_region: "UNVERIFIED"
  new_grad: "UNVERIFIED"
  ats: unknown
  ats_id: unknown
  careers_url: "n/a"
  h1b: "unknown"
  news: "n/a"
  fit: "Intuit San Diego and Scopely are the likeliest high-value additions. Verify when search budget allows."
  sources: []
```
