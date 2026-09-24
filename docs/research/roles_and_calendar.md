# Role Archetypes, Hiring Calendar and Project Positioning (as of 2026-09-24)

Candidate: MS EECS (UC Irvine) and BS CS. Strong Python and Java, some React. Self-built projects: an equity swing-signal system (~16k LOC, event-driven backtester, Optuna walk-forward, FastAPI/WebSocket monitor), a CS2 virtual-item trading agent (918 instruments, 3 years of OHLCV plus order-book depth), and a deployed Flask+React SaaS (375 tests). Course project: HMM + LSTM + XGBoost.

---

## 0. How to read this file

- **[S]** marks a fact taken from a 2025-2026 web-search result in this session. The link is given inline. Salary numbers are **posted base-salary ranges** unless labelled "Glassdoor", "levels.fyi" or "H-1B". CA, NY and IL require pay ranges in postings.
- **[B]** marks background knowledge I could **not** re-verify this session. Treat it as **unverified**.
- **Limits:**
  - Only search-result snippets were available; no page fetches.
  - The search tool summarizes, and it sometimes merges several listings. Re-open a posting before quoting its numbers to anyone.
  - LinkedIn postings with IDs starting 32 or 33 are from 2022-23 and are marked "older".
- **Search cap:** the session hit its 200-search cap partway through this task.
  - A1-A3 and A6 are mostly [S].
  - A4, A5 and A7 are mixed.
  - **Sections C and D are mostly [B].** They cite standard books and papers by title, not fresh 2025-26 recruiter posts.
  - Some [S] items come from searches run by other research agents in this same session (employer and H-1B scans). They are cited by URL.
- **Pay-data caveats:**
  - H-1B LCA wages are base pay, but they skew toward experienced hires.
  - levels.fyi and Glassdoor often mix base and total comp.
  - 6figr figures looked inflated and were ignored.

## Executive summary

1. **Best fit right now:**
   - (a) Quant developer or investment/portfolio-analytics engineer at SoCal asset managers (PIMCO, Capital Group, Research Affiliates, Pacific Life, TCW).
   - (b) Fintech backend SWE.
   - The backtester, data pipeline and FastAPI service map almost 1:1 onto PIMCO's stated quant-dev scope: "research infrastructure (market data, backtest, compute) and trading platform".
2. **Credit-risk / fraud DS is about 3-4 weeks of domain work away.** It has the densest SoCal employer base (Experian, Zest AI, Hyundai Capital America, Tala, loanDepot, PennyMac).
3. **Prediction-market / crypto pricing is the best story fit.** The CS2 agent is a real analog for a thin, retail-driven market with order-book data. Jobs cluster in NYC or remote. AQR now hires "Prediction Markets" quant analysts at **$200-230K base** [S].
4. **HFT trading-systems roles need C++ depth the candidate doesn't show yet.** The candidate's Java is an asset at IMC (Java accepted), bank e-trading and PIMCO trading tech.
5. **QR at top funds ($225-300K base) is a stretch at MS level** without visible statistical rigor. QRA roles at PIMCO, Research Affiliates, Pacific Life and BlackRock SF ($95-215K) are realistic.
6. **Calendar:** the 2027-start quant/prop cycle opened June-August 2026. Late September is mid-cycle, not closed, so apply this week. Fintech and asset-manager hiring is rolling.
7. **Projects:** lead with method (out-of-sample, costs, look-ahead control, multiple-testing control), not win rates. Rewrite "market-maker / main-force" narratives as order-flow and microstructure hypotheses. This matters most when interviewing at actual market makers.

---

## A. Role archetypes

### A1. Quant Developer / Quantitative Software Engineer (buy-side, systematic)

**Postings (evidence)**

| Company, title (location) | What it asks for | Posted base | Source |
|---|---|---|---|
| PIMCO, Quantitative Developer (Newport Beach) | Across PIMCO QD listings: Master's in CS/math/STEM (top school preferred); 3+ yrs hands-on **Python + relational DBs**; work with quant PMs "converting research ideas into production trading strategies"; build "research infrastructure (market data, backtest, compute) and trading platform (position, risk, controls, strategy frameworks, deployment, visualization, observability)" | **$130K-$195K** + discretionary bonus | [S] [Built In LA](https://www.builtinla.com/job/quantitative-developer/6205246), [CAIA careers](https://careers.caia.org/jobs/20216285/quantitative-developer), [LinkedIn](https://www.linkedin.com/jobs/view/quantitative-developer-at-pimco-4224203756) |
| PIMCO, QD Securitized Products / QD Analytics Platform (older, ~2022-23) | 3-5 yrs financial software engineering in **C++ and Python**; "extensive C++ (STL, boost, design pattern, C++11/14)"; quantitative Master's (FE, physics, math) | n/a | [S] [LinkedIn 1](https://www.linkedin.com/jobs/view/quantitative-developer-securitized-products-at-pimco-3285919227), [LinkedIn 2](https://www.linkedin.com/jobs/view/quantitative-developer-analytics-platform-at-pimco-3351650957) |
| PIMCO, Quantitative Developer, SMA & Muni (2026) | Title only captured (fixed-income SMA/muni analytics) | n/a | [S] [Built In](https://builtin.com/job/quantitative-developer-sma-muni/7303326) |
| Capital Group, Quant Engineer (downtown LA or Irvine) | Translate complex quant models into working software; design experiments to validate models; "quickly understand capital markets (equity and fixed income), modern portfolio theory, various market data sources, industry standard portfolio risk models"; R/Python/MATLAB | **$148,045-$236,872** (SoCal) + individual and profitability bonus; 15% retirement contribution | [S] [Ladders](https://www.theladders.com/job/quant-engineer-thecapitalgroupcompaniesinc-irvine-ca_81237895?ir=1), [OpenQuant](https://openquant.co/job/quant-engineer-capital-group/1918), [Built In](https://builtin.com/job/quant-engineer/3559986) |
| Two Sigma, Quantitative Software Engineer (NYC) | BS CS/applied math; **min 1 yr experience** (1-10 preferred); numpy/scipy/scikit-learn; scientific computing; large-scale real-time distributed apps; multi-threaded C++; "financial experience is not a requirement" | not captured | [S] [Two Sigma](https://careers.twosigma.com/careers/JobDetail/New-York-City-United-States-Quantitative-Software-Engineer/13045), [Two Sigma (older)](https://careers.twosigma.com/careers/JobDetail/New-York-New-York-United-States-Quantitative-Software-Engineer/297) |
| Citadel, Quantitative Research Engineer, University Graduate (US) | BS/MS CS/eng; "exceptional programming (C++, Python preferred) and design"; probability and statistics | **$200K-$250K** | [S] [Citadel](https://www.citadel.com/careers/details/quantitative-research-engineer-university-graduate-us/), [Built In NYC](https://www.builtinnyc.com/job/quantitative-research-engineer-university-graduate-us/6554831) |
| Citadel Securities, Quantitative Developer / Research Engineer (experienced) | Automated trading software using statistical techniques | $250K-$350K | [S] [Citadel Securities](https://www.citadelsecurities.com/careers/details/quantitative-developer-research-engineer/) |
| Voleon (Berkeley), Software Engineer, University Hire 2026 | BS CS (class of 2026); Python/Go/C++; Linux; backend, databases, large-scale data processing; **US work authorization required** | **$160K-$190K** (other FT SWE listings $135-185K) | [S] [Taro](https://www.jointaro.com/jobs/the-voleon-group/software-engineer-university-hire-2026/) |
| Research Affiliates, Software Engineer, Investment Systems (Newport Beach) | Title only | n/a | [S] [RA careers](https://www.researchaffiliates.com/about-us/careers) |
| Crabel (LA), systematic futures/FX | No live posting text captured. Glassdoor has one "Software Developer" data point (~$123K), too thin to use | - | [S] [Crabel careers](https://crabel.com/careers/), [Glassdoor](https://www.glassdoor.com/Salary/Crabel-Capital-Management-Software-Developer-Salaries-E260982_D_KO26,44.htm) |

Market-wide: "Common postings ask for proficiency in at least one of Python, C++ or kdb+/q, plus git and Linux" [S] ([Tradermath](https://www.tradermath.org/articles/what-is-a-quant-developer)).

- **Must-have:**
  - Production-quality Python (pandas/numpy, vectorization) and SQL/relational modeling.
  - Testing, code review, Git and Linux.
  - Market-data pipelines and backtest infrastructure.
  - Enough statistics to talk with researchers.
  - At many shops (PIMCO analytics platform, Two Sigma, Citadel), **modern C++** too.
- **Nice-to-have:**
  - C++ via pybind11, kdb+/q, Parquet/Arrow, Dask/Ray/Spark.
  - AWS, Airflow, observability.
  - React dashboards, FastAPI services. The candidate has both.
- **Finance knowledge:**
  - Desk-specific. At PIMCO: fixed income (duration/convexity, curves, spreads; MBS prepayment for Securitized; munis for SMA).
  - At Capital Group, "modern portfolio theory" and "portfolio risk models" are explicit [S].
  - Everywhere: backtest pitfalls (look-ahead, survivorship) and transaction costs [B].
  - Two Sigma explicitly doesn't require finance [S].
- **Interview format** [B unless noted]:
  - Recruiter screen, then 1-2 coding rounds (LeetCode medium, often Python data-manipulation style).
  - A system-design round framed as a quant platform (e.g., "design a backtesting / market-data service").
  - Light probability/statistics.
  - A deep dive into your own projects. Expect the backtester to be grilled.
  - C++ internals at C++ shops.
  - Guides: [Quantt QD questions](https://www.quantt.co.uk/resources/quant-developer-interview-questions), [Two Sigma guide](https://www.techinterview.org/companies/two-sigma/) (titles/snippets only).
- **Entry-level base, California:**
  - SoCal asset managers: **~$120K-$160K** (PIMCO QD $130-195K posted; Capital Group SWE L1 ~$128K total comp on [levels.fyi, Greater LA](https://www.levels.fyi/companies/capital-group/salaries/software-engineer/locations/greater-los-angeles-area)).
  - Bay Area quant funds: $160-190K (Voleon).
  - Top NY/Chicago funds and prop shops: $200-300K.
  - LA quant-dev average (all levels): $166,736 ([Indeed](https://www.indeed.com/career/quantitative-developer/salaries/Los-Angeles--CA)) [S].
- **Gap vs this candidate:**
  - **Strengths:** closest overall match. Event-driven backtester, walk-forward optimization, data pipeline and real-time service equal PIMCO's stated scope.
  - **Gaps:**
    - (1) No C++, which closes the C++-platform roles.
    - (2) No professional experience, while many buy-side QD listings ask for 3+ years. Target new-grad/junior programs and smaller teams.
    - (3) Fixed-income domain for PIMCO and Capital Group.
    - (4) Evidence of production-grade scale: SQLite to Postgres/Parquet, CI, type checks, reproducible runs.

### A2. Quantitative Researcher / Quant Analyst (entry level, MS)

**Postings (evidence)**

| Company, title (location) | What it asks for | Posted base | Source |
|---|---|---|---|
| Citadel, Quantitative Research Analyst, University Graduate (NY/Miami/Greenwich) | BS/MS math/stats/physics/CS; "strong knowledge of probability and statistics (e.g., machine learning, time-series analysis, pattern recognition, NLP)"; data-driven research experience; models into code (Python/R/C++) | **$235K-$300K** (Citadel); $225K-$300K (Citadel Securities) | [S] [Citadel](https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/), [Citadel Securities](https://www.citadelsecurities.com/careers/details/quantitative-research-analyst-university-graduate-us/) |
| D. E. Shaw, Quantitative Analyst | (requirements not captured) | **$275K** BS/MS; $300K PhD | [S] [D. E. Shaw](https://www.deshaw.com/careers/quantitative-analyst-2636) |
| Jane Street, Quantitative Researcher (NY) | - | **$300K** | [S] [Jane Street](https://www.janestreet.com/join-jane-street/position/6302325002/) |
| AQR, Quantitative Research, Prediction Markets Analyst (Greenwich) | BS or higher (DS/CS/math/stats/OR) from a top institution; internship or academic data-driven research (model development and forecasting); strong coding, **Python preferred**; familiarity with "prediction markets, option and contingent claim pricing, and data science" | **$200K-$230K** | [S] [AQR](https://careers.aqr.com/jobs/research/greenwich-ct/quantitative-research-prediction-markets-analyst/8018219?gh_jid=8018219) |
| AQR, Research Analyst, Discretionary Macro | BS in a quantitative field | $150K-$175K | [S] [HiringCafe](https://hiringcafe.com/job/research-analyst-discretionary-macro-aqr-capital-management-greenwich-r8tl6mnn7pde8vyx) |
| PIMCO, Quantitative Research Analyst (Newport Beach) | "Demonstrated ability to solve complex, data-intensive problems using quantitative methods"; markets/products familiarity, **"especially fixed income"**, is a strong plus; communication; iterative development | Glassdoor estimate: total $164-226K, avg base ~$145K | [S] [Built In LA](https://www.builtinla.com/job/quantitative-research-analyst/6758286) |
| PIMCO, Quant Researcher/Developer, PM-Analytics, Portfolio Engineering & Implementation | Integrate systematic signals/models into the investment process; analyze signal inputs; deploy alpha strategies across asset classes | **$165K-$215K** (one listing shows $205-230K) | [S] [eFinancialCareers](https://www.efinancialcareers.com/jobs-USA-CA-Newport_Beach-Quantitative_Research_Analyst.id22524074), [magazine.org mirror](https://jobs.magazine.org/jobs/20215138/quantitative-research-analyst-developer) |
| PIMCO, QRA Execution Research; Systematic Quant Research Analyst; QRA (2026) | Titles only (posting dates unknown except the 2026 one) | - | [S] [Execution](https://www.builtinla.com/job/quantitative-research-analyst-execution-research/4519361), [Systematic](https://www.builtinla.com/job/systematic-quant-research-analyst/4096708), [QRA 2026](https://builtin.com/job/quantitative-research-analyst/7544279) |
| Research Affiliates, Researcher (Newport Beach) | Research drivers of risk and expected return; "analyzing and developing new signals and crafting them into quantitative investment strategies"; communicate through writing; proficient coding; data manipulation | **$95K-$125K** + bonus | [S] [Research Affiliates](https://www.researchaffiliates.com/about-us/careers/researcher) |
| Pacific Life, Quantitative Analyst, Investments (Newport Beach, hybrid) | Help PMs scale, optimize and monitor general-account portfolios; optimization models for investment strategy and credit analysis | **$111K-$135K** | [S] [Built In](https://builtin.com/job/quantitative-analyst/4694748) |
| BlackRock (San Francisco), Analyst Quant Research; Quantitative/Systematic Research Associate | - | $112K-$133K; $133K-$162K | [S] [BlackRock SF jobs](https://careers.blackrock.com/location/san-francisco-jobs/45831/6252001-5332921-5391959/4) |

- **Must-have:**
  - Probability and statistics depth: estimation, hypothesis testing, regression, time series.
  - ML with correct validation.
  - Python (pandas, statsmodels, scikit-learn) and large messy datasets.
  - Clear research writing. Research Affiliates says so explicitly.
- **Nice-to-have:**
  - C++, competitions (Kaggle, Putnam), publications.
  - Options pricing, optimization (cvxpy), Bayesian methods.
- **Finance knowledge:**
  - Factor models: Fama-French and Barra-style risk.
  - Portfolio construction and optimization.
  - Fixed-income analytics for PIMCO.
  - Options greeks and implied vol for derivatives and prediction-market desks. AQR asks for contingent-claim pricing [S].
- **Interview format** [B]:
  - Probability brainteasers and expected-value questions (Green Book / Heard-on-the-Street style).
  - Statistics and ML theory: bias-variance, regression assumptions, overfitting, multiple testing.
  - Python coding, sometimes LeetCode.
  - Research case or take-home: "here is a dataset, find and evaluate a signal".
  - Deep dive into the resume project.
  - At prop shops: market-making and betting games plus mental math.
- **Entry-level base, California:**
  - $95-135K (Research Affiliates, Pacific Life).
  - $112-162K (BlackRock SF).
  - ~$145K average base for PIMCO QRA (Glassdoor), up to $165-215K for PIMCO PM-analytics researcher/dev.
  - $200-300K at top funds, almost all outside CA.
- **Gap vs this candidate:**
  - **Strengths:** the HMM/LSTM/XGBoost work and the 21-signal system show real interest.
  - **Gaps:**
    - QR interviews test statistical rigor the candidate hasn't shown yet: multiple-testing correction, HAC/Newey-West errors, stationarity, IC/t-stat reporting.
    - There is no written research note yet.
    - The technical-analysis framing reads as unscientific (see C).
    - MS candidates compete with PhDs at top funds.
  - **Realistic targets:** asset-manager QRA roles, plus "quant analyst" roles at smaller funds.

### A3. Trading Systems / Execution / Market Data Engineer

**Postings (evidence)**

| Company, title (location) | What it asks for | Posted base | Source |
|---|---|---|---|
| Hudson River Trading, Software Engineer (C++ or Python), 2027 Grads (NY) | C/C++ or Python; CS fundamentals; Linux; "system/processor performance, and network communication"; low-level architecture a plus. The 2026-grads version (per snippet) required "full-time undergraduate students ... eligible for full-time roles in 2026", so **check whether MS grads qualify** | **$300K** (US) + sign-on + bonus | [S] [HRT 2027](https://www.hudsonrivertrading.com/hrt-job/software-engineer-c-or-python-2027-grads/), [HRT 2026](https://www.builtinnyc.com/job/software-engineer-c-or-python-2026-grads/6833743) |
| IMC, Graduate Software Engineer (Chicago; start Feb or Aug 2027) | Any language, **Java or C++ preferred**; graduating **Sep 2026 to Jul 2027**; algorithms and data structures; interest in markets | **$200K** | [S] [IMC](https://www.imc.com/us/careers/jobs/4818790101), [Built In Chicago](https://www.builtinchicago.org/job/graduate-software-engineer/6553930) |
| Optiver, Graduate Software Engineer (2026 start, Chicago) | C++, Python or Java; CS fundamentals; graduating Dec 2025 to Jun 2026 | **$200K** | [S] [Built In Chicago](https://www.builtinchicago.org/job/graduate-software-engineer-2026-start-chicago/6551990) |
| Akuna Capital, Software Engineer (Entry-Level), C++ (Chicago) | Low-latency C++ for trading strategies; training provided (Python track also exists) | **$145K** minimum. One reported offer: $150K base + $65K sign-on + $60K guaranteed | [S] [Built In](https://builtin.com/job/software-engineer-entry-level-c/6632355) |
| Citadel Securities, Software Engineer, University Graduate (US) | - | **$235K-$300K** | [S] [Citadel Securities](https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-us/) |
| Headlands Technologies (SF/Chicago), C++ Software Developer, New Grad | Exchange connectivity, low-latency networking, distributed storage, research infrastructure | not captured | [S] [Greenhouse](https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/4336806009) |
| Bank / JVM low-latency postings: Citi "Low Latency Electronic Trading Software Engineer – Java" (VP; Hong Kong/Canada) and a recruiter JVM trading-system posting | Across these (search summary merged them): ~7+ yrs Java/C++/Rust; market-data and order-lifecycle event processing; **FIX** and exchange connectivity; "GC-sensitive" Java with off-heap memory and binary protocols; sequencing gaps, snapshot/replay. Senior roles, shown only to illustrate the Java path | - | [S] [Citi](https://jobs.citi.com/job/kowloon/low-latency-electronic-trading-software-engineer-java-vice-president/287/95371118240), [mirror](https://freehire.me/jobs/low-latency-electronic-trading-software-engineer-java-vice-president-citi-2o2s32fo), [recruiter posting](https://freehire.me/jobs/senior-software-developer-jvm-low-latency-trading-system-motion-recruitment-partners-llc-ibwuoe53) |
| PIMCO, Software Engineer / Java Developer, Short Term (Trading) Technology (Newport Beach) | Trading and cash-management systems for Short Term, Cash and Collateral desks; **5+ yrs Java (17+/21)**, microservices, REST, event-driven; AWS/cloud-native; AI coding tools | not captured | [S] [Dice](https://www.dice.com/job-detail/af755a67-68ee-44fa-af55-9e08b5f8b86b), [mirror](https://freehire.me/jobs/java-developer-short-term-trading-technology-pimco-efinancialcareers-wjia2udn) |

- **C++ vs Python/Java shops:**
  - HFT and market makers (HRT, Jump, Tower, DRW, Citadel Securities, Optiver, Headlands) run C++ cores. "DRW is a low-latency C++ shop where C++ depth is a hard filter for core roles"; "Optiver and IMC focus on market-maker engineering with strong C++ and systems components" [S] ([Origami](https://origami.chat/blog/trading-firms-low-latency-infrastructure-hiring-signals)).
  - IMC explicitly accepts Java [S].
  - Bank e-trading is often Java: the LMAX Disruptor / Aeron / SBE stack [S].
  - Buy-side trading tech (PIMCO) is Java microservices [S].
  - HRT has a Python track [S]. Jane Street uses OCaml [B].
- **Must-have:**
  - C++ (STL, memory, performance) *or* low-latency Java (concurrency, GC).
  - DS&A, Linux, multithreading.
  - Networking basics: TCP/UDP, multicast.
- **Nice-to-have:**
  - Lock-free structures, profiling (perf), kernel bypass, FPGA interest.
  - FIX/ITCH/OUCH/SBE; kdb+ for tick capture.
- **Finance knowledge:**
  - Microstructure: order types, limit-order books, matching and queue priority, tick sizes, maker/taker fees.
  - Order lifecycle, pre-trade risk checks, L1/L2/L3 feeds.
- **Interview format:**
  - A DS&A screen.
  - C++ internals: "the memory model, lock-free programming, false sharing, branch prediction", container runtime behavior.
  - System design shaped like a trading pipeline ("market data ingest → strategy → risk checks → execution") with tight latency budgets and reasoning about cache and tail latency [S]. Sources: [techinterview.org](https://www.techinterview.org/post/3233474597/cpp-quant-interviews/), [HackerPrep, HRT](https://hackerprep.io/blog/hrt-low-latency-cpp-system-design-prep), [Quantt C++](https://www.quantt.co.uk/resources/cpp-quant-interview-questions).
  - Prop firms may add mental math and probability [B].
- **Entry-level base:**
  - $200-300K at Chicago/NY firms; Akuna from $145K.
  - California options are few: Headlands SF (pay not captured) and Voleon Berkeley ($160-190K).
  - SoCal buy-side trading tech mostly hires experienced Java engineers.
- **Gap vs this candidate:**
  - **Gaps:** the largest of all archetypes for HFT. There is no C++, no systems or latency work, and no FIX or feed-handler experience. The FastAPI+WebSocket monitor is "real-time" at millisecond scale, not microsecond.
  - **Strengths:** Java is a real asset for IMC, bank e-trading and PIMCO trading tech.
  - **To compete:** build a C++17/20 limit-order-book plus ITCH-style feed parser with latency histograms. Alternatively, build a Java version on Disruptor/Aeron.

### A4. Fintech Backend Software Engineer (payments, brokerage, lending)

**Postings (evidence)**

| Company, title (location) | What it asks for / scope | Pay signal | Source |
|---|---|---|---|
| Acorns, Software Engineer I, Recent Graduate (remote, Irvine or NY) | "Translating high-level business requirements... into the services and data models that power them"; work with mobile, frontend and QA. The prior posting went up 2024-12-10 for a ~2025-03-01 start | H-1B: SWE II median ~$161.7K; all titles ~$160K | [S] [Ashby](https://jobs.ashbyhq.com/Acorns/5618f1de-cf18-4114-9408-11cd73153a9d), [h1bdata](https://h1bdata.info/index.php?em=acorns+grow+inc&job=) |
| Dave (LA), Senior Software Engineer, Backend | Owns "Dave Bank accounts, debit cards, payment processing, and the integrations that connect with sponsor banks, payment processors". 11 openings in Sept 2026 (backend, fullstack, data eng, AI acceleration) | H-1B median ~$160K | [S] [Ashby](https://jobs.ashbyhq.com/dave/75e61fb3-3883-4d8f-8c2d-44f75ef9fc1a), [h1bdata](https://h1bdata.info/index.php?em=dave+inc) |
| PennyMac (Westlake Village/Moorpark), Digital Technology Organization Rotational Program (Technology Rotation Engineer I) | BS CS/SE; "strong programming skills (e.g., Java, Python, C++)"; SDLC. Rotations cover cloud platform, DevOps, app dev in **Finance and Enterprise Risk**, IT data analytics. **Jan or Jun 2027 cohorts** | Sr App Dev $90-150K; levels SWE median ~$145K total comp | [S] [USC listing](https://www.cs.usc.edu/newsletter/ug-ms-phd-pennymac-tech-rotational-program/), [PennyMac](https://careers.pennymac.com/jobs/37785?lang=en-us&previousLocale=en-US) |
| Experian (NA HQ Costa Mesa; remote), Software Engineer Xcelerator Rotation Program (Entry Level SWE) | 12 months, two 6-month rotations; starts **April and June** | Staff SWE Costa Mesa posted $115,747-$208,344 | [S] [Experian](https://jobs.experian.com/job/software-engineer-xcelerator-rotation-program-entry-level-swe-remote-in-united-states-jid-3269) |
| loanDepot (Irvine), Software Engineer (mello mortgage platform) | Consumer, ops and enterprise apps | Lead FE (Angular/React) $138-191K; H-1B median $114K | [S] [loanDepot](https://careers.loandepot.com/job-detail/6199), [1point3acres](https://visa.1point3acres.com/h1b/salary/loandepot-com-llc) |
| BlackRock (SF), Full Stack Java Engineer, Aladdin Product Engineering (Associate) | Java full stack | **$132.5K-$162K** | [S] [BlackRock](https://careers.blackrock.com/job/san-francisco/full-stack-java-engineer-aladdin-product-engineering-associate/45831/82938495872) |
| Hyundai Capital America (Irvine), Application Developer Associate (SQL/PL-SQL); Sr Software Developer (Salesforce) | Auto-finance and insurance platforms | Sr SW Dev $132-205K | [S] [Glassdoor posting](https://www.glassdoor.com/job-listing/sr-software-developer-salesforce-hyundai-capital-america-JV_IC1146798_KO0,32_KE33,56.htm?jl=1010188704906) |
| First American (Santa Ana), Software Engineer; SWE intern (BS CS, 0-2 yrs) | Title/escrow fintech | - | [S] [First American](https://careers.firstam.com/job/santa-ana/software-engineer/39054/82742984080) |
| Stripe, Robinhood, Coinbase, Affirm, Plaid, Chime, Ramp, Brex, SoFi | **Not searched this session** | unverified | [B] |

- **Must-have:**
  - One backend language at production depth: Java/Kotlin, Go, Python or TypeScript.
  - API design, SQL/Postgres (transactions, isolation, migrations), automated tests, cloud (AWS), CI/CD.
- **Nice-to-have:**
  - Kafka/event-driven design, Docker/K8s, observability.
  - Payment rails (ACH, cards, RTP/FedNow), KYC/AML, PCI-DSS.
  - React for fullstack roles [B].
- **Finance knowledge (light)** [B]:
  - Payments: auth, capture, settlement, refunds, chargebacks.
  - Double-entry ledgers and reconciliation; idempotency.
  - Brokerage: order types, T+1 settlement, corporate actions.
  - Lending: origination, servicing, delinquency.
  - Regulatory vocabulary: Reg E, FCRA, BSA/AML.
- **Interview format** [B]:
  - Online assessment (HackerRank/CodeSignal), then LeetCode-medium coding.
  - System design, e.g., payment/ledger service, idempotent API, rate limiter.
  - Behavioral round.
  - Some fintechs (Stripe is the commonly cited example) use practical "real-code" rounds instead of puzzles [B, unverified].
- **Entry-level base, SoCal:**
  - **~$90K-$160K** (levels.fyi Irvine entry-level SWE range [S] [levels](https://www.levels.fyi/t/software-engineer/levels/entry-level/locations/irvine-usa)).
  - Payscale Irvine entry-level average $87.8K ([Payscale](https://www.payscale.com/research/US/Job=Software_Engineer/Salary/c0aa9efa/Entry-Level-Irvine-CA)) [S].
  - FloQast SE1 in LA $91-143K ([levels](https://www.levels.fyi/companies/floqast/salaries/software-engineer/levels/software-engineer-1/locations/greater-los-angeles-area)) [S].
  - Bay Area big fintechs pay more [B, unverified].
- **Gap vs this candidate:**
  - **Strengths:** strong on paper. A deployed multi-user SaaS with JWT, a paid tier, a scheduler, alerts and 375 tests is exactly what backend screens reward.
  - **Gaps:**
    - The showcase stack is Flask/SQLite/VPS. The candidate should show Java services and Postgres, plus money-correctness patterns (idempotency keys, double-entry ledger, reconciliation) and AWS.
    - System-design interviews need practice.
- **Market context** [S]:
  - 2026 tech layoffs are elevated (52,050 tech cuts in Q1 2026 per [Kore1](https://www.kore1.com/tech-layoffs-2026/); California is "the epicenter" per the [SF Chronicle](https://www.sfchronicle.com/tech/article/tech-layoff-job-worker-ai-california-22364424.php)).
  - Engineering roles are reported as the most resilient ([TechCrunch](https://techcrunch.com/2026/06/24/ai-was-supposed-to-kill-engineering-jobs-but-new-data-suggests-theyre-the-most-resilient/)).
  - Local WARN notices: Experian Costa Mesa ([WARN tracker](https://www.warntracker.com/layoff/experian-2026-05-22)).

### A5. Credit Risk / Fraud Data Scientist / Risk Analytics (lenders, auto finance, bureaus)

**Postings (evidence; thinner, because the search cap was hit)**

| Company, title (location) | Scope | Pay signal | Source |
|---|---|---|---|
| Zest AI (Burbank), Software Engineer; Machine Learning Engineer | ML credit underwriting for banks and credit unions | levels.fyi: SWE ~$143K, Data Scientist ~$170K; H-1B median $135K (Burbank $142K) | [S] [Greenhouse 1](https://job-boards.greenhouse.io/zestai/jobs/5645115004), [Greenhouse 2](https://job-boards.greenhouse.io/zestai/jobs/5591251004), [h1bdata](https://h1bdata.info/index.php?em=zestfinance+inc) |
| Experian, Data & Analytics Xcelerator Program (Entry Level, remote US) | Rotational analytics program | Experian H-1B median ~$108.6K | [S] [Experian](https://jobs.experian.com/job/data-and-analytics-xcelerator-program-entry-level-data-analytics-remote-in-united-states-jid-3270), [1point3acres](https://visa.1point3acres.com/h1b/salary/experian-services-corporation) |
| Tala (Santa Monica), Data Platform Engineer I | Infrastructure for "a best-in-class decision engine"; works with ML engineers and data scientists (mobile lending) | H-1B median ~$166K | [S] [Lever](https://jobs.lever.co/tala/82efbb9a-44ab-48e6-a578-5073dcb7e41c), [visa-bulletin](https://visa-bulletin.us/employer/inventure-capital-corporation-dba-tala-1/) |
| Hyundai Capital America (Irvine, auto finance) | Risk-analytics postings not captured; sponsors H-1B | H-1B median $131-150K (FY2025) | [S] [h1bgrader](https://h1bgrader.com/h1b-sponsors/hyundai-capital-america-x30qpq98kq) |
| Pacific Life (Newport Beach) | Lead "development, validation, and automation of cashflow and market-risk models for complex public and illiquid assets" (on-site) | - | [S] [Built In LA](https://www.builtinla.com/company/pacific-life/jobs) |
| DoubleLine (LA) | "Quantitative Risk Analyst" H-1B titles | H-1B median $117K | [S] [h1bdata](https://h1bdata.info/index.php?em=DOUBLELINE+GROUP+LP) |

- **Typical requirements** [B, unverified this session]:
  - Heavy SQL; Python (SAS still common at banks).
  - Logistic regression and GBMs.
  - Scorecard building: binning, WoE/IV.
  - Metrics: AUC/Gini, KS. Monitoring: PSI/CSI. Out-of-time validation. Reject inference.
  - Explainability for adverse-action reason codes (ECOA/Reg B, FCRA) and fair-lending testing.
  - Model risk management (Fed SR 11-7).
  - Loss forecasting: PD/LGD/EAD, CECL, vintage and roll-rate curves.
  - Fraud: class imbalance, anomaly detection, device/graph features, real-time scoring.
- **Nice-to-have:** credit-bureau attributes, survival models, causal/uplift methods for credit-line strategies, Spark.
- **Interview format** [B]:
  - SQL live test and a pandas exercise.
  - Statistics/ML: interpreting logistic coefficients, imbalanced-class metrics, leakage.
  - Business case, e.g., "set an approval cutoff" or "credit-line-increase strategy" with P&L trade-offs.
  - Frequently a take-home on a loan dataset.
- **Entry-level base, SoCal:** **~$100K-$150K** (H-1B medians above; entry-specific figures unverified).
- **Gap vs this candidate:**
  - **Strengths:** ML skills transfer (XGBoost/HMM/LSTM). The signal-return verification loop is essentially model monitoring.
  - **Gaps:** no credit domain, no SQL-heavy analytics portfolio, no explainability or fairness work.
  - **Fix in ~3 weeks** [B]: a public-data credit project (Home Credit Default Risk, Lending Club or Freddie Mac loan-level). Include a scorecard plus a GBM challenger, out-of-time validation, PSI monitoring, SHAP reason codes and a fairness check.
  - **Upside:** the SoCal employer set is dense (Experian, Zest AI, Hyundai Capital, Honda Finance, Tala, loanDepot, PennyMac).

### A6. Investment / Portfolio Analytics Engineer, Investment Data Engineer (asset managers)

**Postings (evidence)**

| Company, title (location) | Scope | Pay | Source |
|---|---|---|---|
| Capital Group, Quant Engineer (see A1); Machine Learning Engineer (Irvine) | Quant models into production; portfolio risk models | **$148,045-$236,872** (SoCal) | [S] [LinkedIn jobs](https://www.linkedin.com/company/capital-group/jobs), [OpenQuant](https://openquant.co/job/quant-engineer-capital-group/1918) |
| Capital Group, CAMPUS: Software Development Engineer Associate; CAMPUS: Technology Rotational Experience (TREx) Associate (2026); CAMPUS: Data Engineer (2024, Irvine) | New-grad cohorts. TREx rotates across solutions engineering, software dev, architecture, infosec | levels.fyi SWE L1 ~$128K total comp (Greater LA); H-1B SDE II median $192K | [S] [LinkedIn](https://www.linkedin.com/jobs/view/campus-software-development-engineer-associate-at-capital-group-4051427718), [The Muse](https://www.themuse.com/jobs/capitalgroup/campus-technology-rotational-experience-trex-associate-2026), [Workday](https://capgroup.wd1.myworkdayjobs.com/en-US/capitalgroupcareers/job/Irvine/CAMPUS--Data-Engineer--2024-_JR1815), [h1bdata](https://h1bdata.info/index.php?em=capital+group+companies+global) |
| PIMCO, Quant Researcher/Developer, PM-Analytics, Portfolio Engineering & Implementation; Senior Developer, Investment Accounting; QRA Client Solutions & Analytics | Signal and model implementation; investment accounting systems | $165-215K; Sr Dev $168-240K. PIMCO H-1B median $155K (one aggregator) / $168K (h1bdata, 103 records; 33% above $200K). Tech Analyst intern $52.88/hr | [S] [eFinancialCareers](https://www.efinancialcareers.com/jobs-USA-CA-Newport_Beach-Quantitative_Research_Analyst.id22524074), [Indeed](https://www.indeed.com/q-pimco-careers-l-newport-beach,-ca-jobs.html), [h1bdata](https://h1bdata.info/index.php?em=pacific+investment+management+company+(pimco)&city=newport+beach), [intern](https://builtin.com/job/2026-summer-intern-technology-analyst-software-engineering/7009931) |
| Research Affiliates, Software Engineer, Investment Systems | **Note:** RAFI Indices sold to TMX VettaFi (US$490M; announced Jun 2026; VettaFi reports the deal completed), so team changes at Research Affiliates are possible | H-1B median $127.5K (14 records) | [S] [VettaFi](https://www.vettafi.com/insights/indexing-article-tmx-vettafi-completes-acquisition-of-rafi-indices-from-research-affiliates), [h1bdata](https://h1bdata.info/index.php?em=research+affiliates+llc) |
| TCW (LA), Senior Developer Analyst (H-1B title); current tech postings skew Salesforce/corporate | - | H-1B $156.5K | [S] [h1bdata](https://h1bdata.info/index.php?city=los+angeles&em=tcw+llc&job=senior+developer+analyst) |
| Pacific Life, Quantitative Analyst ($111-135K); Summer 2026 SWE internship | Portfolio optimization models | see A2 | [S] [Workday](https://pacificlife.wd1.myworkdayjobs.com/PacificLifeCareers/job/Newport-Beach-CA-700/Summer-2026-Software-Engineering-Internship-Program_R15496) |
| BlackRock (SF), Aladdin engineering (Associate $132.5-162K; SWE $71.25-135K) | Aladdin platform | - | [S] (see A4) |
| DoubleLine, Director, Data Technology (LA); HQ now Tampa | - | - | [S] [Built In LA](https://www.builtinla.com/company/doubleline-group-lp/jobs), [Wikipedia](https://en.wikipedia.org/wiki/DoubleLine_Capital) |

- **Must-have:**
  - Python + SQL, ETL/ELT with data-quality checks.
  - Services/APIs, dashboards.
  - A cloud data platform (Snowflake, Databricks, AWS or Azure) [B partly].
- **Nice-to-have:**
  - dbt, Airflow, Spark.
  - React (already used), BI tools.
  - Vendor data: Bloomberg, FactSet, MSCI/Barra, ICE. Aladdin exposure.
- **Finance knowledge** [B]:
  - Return math (TWR/MWR), Brinson attribution.
  - Tracking error, VaR, factor exposures.
  - Fixed-income analytics (duration/convexity/OAS/key rates).
  - Security master and reference data, corporate actions, IBOR/ABOR, benchmarks, portfolio-compliance rules.
- **Interview format** [B]:
  - Python/SQL data-manipulation coding and light LeetCode.
  - Data-modeling and pipeline design.
  - Finance fundamentals ("what is duration?").
  - Culture/behavioral rounds weigh heavily at PIMCO and Capital Group.
- **Entry-level base, SoCal:** **~$110K-$150K**. Mid-level postings run $148-240K.
- **Gap vs this candidate:**
  - **Strengths:** strong fit on pipelines, dashboards, React and tests.
  - **Gaps:** domain vocabulary (attribution, risk models, FI analytics, reference data) and the enterprise data stack.
  - **Location:** best fit of all archetypes (Newport Beach, Irvine, LA).

### A7. Crypto / Prediction-Market / Sportsbook Trading and Pricing Engineer

**Postings (evidence)**

| Company, title (location) | What it asks for | Posted base | Source |
|---|---|---|---|
| AQR, Quantitative Research, Prediction Markets Analyst (Greenwich) | "Seek out reliable prediction markets trading strategies across all types of event contracts, including financial, economic, sports, politics, culture, and crypto"; acquire and clean data, build models, analyze backtested strategies, turn research into trading; Python; option/contingent-claim pricing | **$200K-$230K** | [S] [AQR](https://careers.aqr.com/jobs/research/greenwich-ct/quantitative-research-prediction-markets-analyst/8018219?gh_jid=8018219) |
| AQR, 2027 Quantitative Prediction Markets Research Summer Analyst; Prediction Markets VP | The team is expanding; institutional quant money is entering event contracts | - | [S] [AQR intern](https://careers.aqr.com/jobs/open-positions/greenwich-ct/2027-quantitative-prediction-markets-research-summer-analyst/8122378?gh_jid=8122378), [VP](https://talents.vaia.com/companies/aqr-capital-management/greenwich/quantitative-research-prediction-markets-vp-90591530/) |
| Kalshi, Polymarket, DraftKings, FanDuel, Underdog, PrizePicks, Coinbase, Kraken, Wintermute, Jump Crypto, Cumberland (DRW), SIG | **Not searched this session** | unverified | [B] |

- **Must-have** [B]:
  - Python plus probabilistic modeling with calibrated probabilities.
  - Real-time data (WebSocket order books).
  - Millisecond-level backend services; exposure and risk limits.
- **Nice-to-have** [B]:
  - Rust/Go/C++ for crypto HFT; on-chain/EVM data.
  - Sports models: Elo, Poisson/Dixon-Coles, Bradley-Terry, in-play models.
  - Binary-option pricing; Kelly sizing.
- **Finance knowledge** [B]:
  - Implied probability and overround ("vig") removal; calibration (Brier score, log loss).
  - Market making: inventory risk, adverse selection, Avellaneda-Stoikov.
  - Crypto: perpetual funding, basis, exchange/custody risk.
  - Regulatory landscape: CFTC-regulated event contracts, state sports-betting rules.
- **Interview format** [B]: probability/expected-value puzzles and betting games; a "price this contract" modeling case; coding; real-time pricing/risk system design.
- **Pay:** AQR $200-230K base [S]. Others unverified.
- **Gap vs this candidate:**
  - **Strengths:** best narrative fit. The CS2 agent (918 thin, retail-driven instruments with order-book depth, walk-forward tests, a live verification loop) is a genuine analog.
  - **Gaps:** explicit calibration work, market-making theory, event-contract or sports data, and Rust/C++ for crypto HFT.
  - **Location:** mostly NYC or remote (unverified), so it's a poor match for LA/OC.

### Cross-archetype comparison (my assessment; fit 1-5)

| Archetype | Fit now | Biggest gap | Entry base, CA (evidence) | SoCal employer density |
|---|---|---|---|---|
| A1 Quant dev (buy-side) | 4 | C++; production scale; fixed-income domain | $130-195K PIMCO; Voleon $160-190K | Medium (PIMCO, Capital Group, RA, Crabel) |
| A2 Quant researcher | 2-3 | Visible stats rigor; research write-up; PhD competition | $95-135K RA/PacLife; $112-162K BlackRock SF | Low-medium |
| A3 Trading systems | 1-2 (C++) / 3 (Java shops) | C++/low-latency, FIX/feeds | Few CA roles; $200-300K NY/Chicago | Low |
| A4 Fintech backend | 4 | Java/Postgres/ledgers; system design | ~$90-160K | High |
| A5 Credit/fraud DS | 3 | Credit domain, SQL, explainability | ~$100-150K | High |
| A6 Investment analytics eng | 4 | Domain vocabulary; cloud data stack | ~$110-150K | High (Newport/Irvine/LA) |
| A7 Crypto / prediction mkt / sportsbook | 3 | Calibration, market making; location | AQR $200-230K (CT) | Low |

**Three gap-closing mini-projects** [B], each 1-3 weeks, reusable across archetypes:

1. **Research note (PDF + repo)** re-running the equity system with the section-C checklist: nested walk-forward, costs, deflated Sharpe, and a factor-adjusted alpha. Helps A1, A2 and A7.
2. **C++ (or Java) limit-order book and feed parser** with latency percentiles. Helps A3 and A1.
3. **Credit scorecard project** on public loan data (A5), *or* a **ledger/idempotent-payments module** plus a Postgres migration in the SaaS (A4).

---

## B. Hiring calendar (as of late September 2026)

**Dated evidence**

| Evidence | What it shows | Source |
|---|---|---|
| AQR: summer-2027 internship applications **opened June 30, 2026** and "remain open through mid-August" | Quant hedge-fund campus cycle starts about June | [S] [Extern](https://www.extern.com/post/aqr-capital-internship-guide) |
| HRT: "Software Engineer (C++ or Python) – **2027 Grads**" and "Internship – Summer 2027" both live | 2027-grad full-time roles are open in the fall of 2026 | [S] [HRT FT](https://www.hudsonrivertrading.com/hrt-job/software-engineer-c-or-python-2027-grads/), [HRT intern](https://www.hudsonrivertrading.com/hrt-job/software-engineering-internship-c-or-python-summer-2027/) |
| IMC: Graduate SWE, start **Feb or Aug 2027**, for students graduating **Sep 2026 to Jul 2027** | A Dec-2026 MS grad is explicitly eligible | [S] [IMC](https://www.imc.com/us/careers/jobs/4818790101) |
| Optiver: "Graduate SWE (**2026 Start**)" for Dec 2025 to Jun 2026 grads | Prop firms hire about 9-15 months before start | [S] [Built In Chicago](https://www.builtinchicago.org/job/graduate-software-engineer-2026-start-chicago/6551990) |
| Voleon: "SWE, University Hire 2026" plus "SWE Intern (Summer 2027)" | Same pattern | [S] [Taro](https://www.jointaro.com/jobs/the-voleon-group/software-engineer-university-hire-2026/), [Ashby](https://jobs.ashbyhq.com/voleon/57f1b666-2f4b-4bad-aac0-fa42a1c8fdf6) |
| Headlands: "C++ Software Developer – New Grad" Greenhouse posting live; a 2026-09-17 job-notification scrape came up in the same search | Some new-grad roles are open in late September (the posting's open date is unverified) | [S] [Greenhouse](https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/4336806009), [GitHub scrape](https://github.com/abhiramgorle/Job-Notifications/issues/12730) |
| Citadel / Citadel Securities: "University Graduate (US)" postings | Evergreen, rolling | [S] (A2/A3 links) |
| Pacific Life: summer-2027 postings "expected to open around September to October 2026"; Summer 2027 Actuarial Intern already on Workday | SoCal insurers and asset managers recruit interns in the fall | [S] [Extern](https://www.extern.com/post/pacific-life-internship-guide), [Workday](https://pacificlife.wd1.myworkdayjobs.com/PacificLifeCareers/job/Newport-Beach-CA-700/Summer-2027-Actuarial-Intern--Newport-Beach-_R17460) |
| PennyMac: rotational program for **Jan or Jun 2027** cohorts, applications live | Rotational full-time programs with two start dates | [S] (A4 links) |
| TCW: 2026 internships for grads Dec 2026 to Jun 2027; "successful interns may receive an offer to join the full-time analyst program" | Asset-manager analyst seats are largely filled via interns | [S] [TCW iCIMS](https://careers-tcw.icims.com/jobs/2120/summer-2026-internship-program/job) |
| Experian Xcelerator: starts in **April and June** | Rolling entry programs | [S] (A4 link) |
| Acorns: SWE I, Recent Graduate posted **2024-12-10** for a ~**2025-03-01** start | Fintech new-grad requisitions also appear in winter | [S] (A4 link) |

**Typical windows by employer type**

- **Quant hedge funds and prop/market makers (2027 start):**
  - Postings open **June-August** [S].
  - Review is rolling. Most offers go out Sept-Dec, and seats fill first-come; a few stay open into spring [B].
  - **Late September is past the early wave but not closed.** Apply within days and use referrals [B].
- **Banks (technology analyst programs)** [B, unverified]:
  - Most 2027 full-time seats are filled by converting summer-2026 interns.
  - Remaining full-time postings usually appear Aug-Oct.
  - So late September is late, but some are still viable.
- **Asset managers (PIMCO, Capital Group, TCW, Pacific Life):**
  - Campus hiring runs through internships a year ahead [S: TCW, Pacific Life].
  - Junior and experienced requisitions (PIMCO QD, Capital Group Quant Engineer) post year-round [S].
  - Late September is not late for requisition-based roles.
- **Fintech and tech:**
  - Rolling. Bursts in Aug-Nov and Jan-Mar [B], plus winter postings (Acorns example) [S].
  - Late September is fine.

**If the candidate graduates in 2026**

- **Graduating December 2026:**
  - The candidate counts as a 2027 new grad (IMC's window explicitly covers Sep 2026 to Jul 2027).
  - Apply to open 2027-grad quant/prop roles **now**: HRT Python track (confirm MS eligibility), IMC (Java), Citadel/Citadel Securities UG, D. E. Shaw, Headlands, Voleon.
  - In parallel, apply to SoCal asset-manager requisitions.
- **Already graduated (spring or summer 2026):**
  - Some roles targeted at the "20XX grad" year may exclude the candidate. HRT's 2026-grads posting asked for "full-time undergraduate students"; Optiver's 2026 window ended June 2026 [S].
  - Focus on:
    - (a) Evergreen "University Graduate" roles (Citadel) [S].
    - (b) Rotational programs with rolling starts: Experian (Apr/Jun), PennyMac (Jan/Jun 2027), Capital Group CAMPUS [S].
    - (c) "Junior" or "0-2 yrs" requisitions at fintechs and asset managers.
    - (d) Experienced-hire quant roles with a 1-year minimum (Two Sigma QSE) once the candidate has ~12 months of experience [S].
  - "Available to start immediately" helps with off-cycle requisitions [B].
  - Coordinate with OPT timing (see the separate visa research).
- **Next 8 weeks** [B]:
  - Weeks 0-2: all open quant/prop and asset-manager applications.
  - Weeks 1-6: fintech and credit applications (Acorns, Dave, Experian, Zest AI, Tala, Hyundai Capital, PennyMac, loanDepot).
  - Throughout: ship mini-project #1 (the research note), because it upgrades every application.
  - Jan-Mar 2027: second wave.

---

## C. Presenting self-directed trading projects

*Evidence level: mostly [B]. It draws on standard practitioner and academic literature, cited by title at the end. I could not pull fresh 2025-26 recruiter posts before the search cap. The advice is conventional among quant interviewers, but treat it as unverified.*

### What impresses

1. **A falsifiable hypothesis with an economic reason:** why the edge exists, who is on the other side, and why it persists.
2. **Clean data:**
   - Point-in-time data and a survivorship-free universe that includes delisted names.
   - Corporate-action adjustments and correct timestamps.
   - For CS2: platform fees, trade holds, and items that disappeared.
3. **Look-ahead control:**
   - Signal on close t, trade at the next open.
   - Regime and sector filters computed from past data only.
   - **HMM regimes use filtered, not smoothed, probabilities.** Forward-backward smoothing leaks the future. This is a strong talking point given the course project.
4. **Honest out-of-sample testing:**
   - Walk-forward with *nested* Optuna tuning.
   - Purging and embargo when labels overlap.
   - A final untouched holdout.
   - Show the in-sample vs out-of-sample decay.
5. **Costs and capacity:**
   - Commissions, spread, and slippage scaled to volatility/ADV.
   - Short-borrow costs and market impact.
   - Turnover and an estimate of capacity.
6. **Risk-adjusted reporting:**
   - Annualized return and volatility; Sharpe with a t-stat or confidence interval; Sortino.
   - Max drawdown and its duration.
   - Hit rate **together with** payoff ratio.
   - Beta and exposure.
   - **Alpha vs benchmark and factors** (market, size, value, momentum, short-term reversal).
7. **Multiple-testing awareness:**
   - State how many configurations were tried (21 signals × Optuna trials).
   - Report the deflated Sharpe ratio, White's Reality Check or Hansen SPA, or the probability of backtest overfitting.
8. **Robustness:**
   - Parameter heatmaps showing plateaus, not spikes.
   - Sub-periods, universes and regimes.
   - A random-entry placebo with the same holding-time distribution.
   - Ablation: which of the 21 signals actually matter.
9. **Engineering quality:**
   - Unit and golden tests for backtester accounting (fills, partial fills, position limits).
   - Config-driven, seeded, reproducible runs; a README and architecture diagram; profiling notes.
10. **Documented negative results.** "Signals X and Y died after costs" builds credibility.

### What hurts

- "Smart money / main force / market makers trap retail" language without statistics.
- Chart-pattern lore and TA hype words.
- Headline win rates or big CAGRs without drawdown, costs or a benchmark.
- An equity-curve screenshot as the "result".
- The Optuna best trial reported as performance, i.e., in-sample results presented as the result.
- Unverifiable live-P&L claims or brokerage screenshots. These are also a compliance smell.
- A complex LSTM on small data with no simple baseline (buy-and-hold, plain momentum).
- Vague ownership. The candidate must be able to explain every line of the backtester.
- Pitching "I want to keep running my strategy". Firms restrict personal trading (pre-clearance, holding periods, often no single stocks or crypto) [B].
- **Special risk at real market makers** (Optiver, IMC, SIG, Citadel Securities, Jane Street): interviewers *are* the market makers. Narratives about market makers manipulating prices will land badly. Frame it as **inventory management, adverse selection and liquidity provision** instead.

### Translation table: narrative → quant language → how to test

| Discretionary / "market-maker" narrative | Rigorous framing | Test to show |
|---|---|---|
| "Main force accumulating" | Persistent informed order flow; volume-return divergence (high volume, low absolute return); Kyle (1985) price impact | Cross-sectional IC and predictive regressions of h-day forward returns on volume-surprise × \|return\|, Newey-West t-stats; control for size, liquidity and sector |
| "Shakeout / washout" | Temporary price pressure and short-term reversal (temporary vs permanent impact) | Event study: cumulative abnormal returns after large down-moves on high vs low volume; compare with the standard reversal factor |
| "Support / resistance" | Price clustering; limit-order depth at salient levels; conditional breakout hazard | Placebo against randomized levels; in CS2, measure actual order-book depth at those levels |
| "Breakout with volume confirmation" | Time-series momentum conditioned on volume | Sharpe with vs without the volume filter; bootstrap test of the difference |
| "Only trade in bull regimes" | State-dependent exposure; volatility/trend regimes (HMM) | Past-only regime labels; report detection lag; performance by regime |
| "Strong sectors" | Industry momentum (Moskowitz and Grinblatt 1999) | Compare against a known industry-momentum factor |
| "Sell-signal monitor" | Exit rule as a conditional forward-return distribution or hazard model | Compare with trailing-stop and fixed-horizon baselines; measure giveback |
| "70% win rate" | Expectancy = p·avgWin − (1−p)·avgLoss; profit factor; per-trade t-stat | Distribution of trade returns, not just the hit rate |
| "Optimized 21 signals" | Model selection under multiple testing | Nested walk-forward; report the trial count; deflated Sharpe or SPA p-value |
| CS2 "supply/demand depth" | Order-book imbalance, order-flow imbalance (Cont, Kukanov and Stoikov 2014), spread, Amihud illiquidity | Walk-forward IC of imbalance features; cost of crossing the spread; capacity |
| CS2 "signal-return verification loop" | Live out-of-sample monitoring: IC decay, calibration, drift (PSI) | Rolling IC chart; pre-registered vs realized results |

### Resume bullet templates (fill with real numbers only)

- "Built an event-driven equity backtester (Python, ~16k LOC) modeling position limits, commissions and volatility-scaled slippage. Verified the accounting with N unit/golden tests."
- "Evaluated 21 price-volume signals on a survivorship-free US universe (YYYY-YYYY) with nested walk-forward (K folds, M Optuna trials). Out-of-sample net Sharpe S (t = T), max drawdown D, turnover X/yr; deflated-Sharpe p = P. Documented which signals failed after costs."
- "Built a CS2 secondary-market dataset (918 instruments, 3 years of daily bars plus order-book depth). Order-book-imbalance features validated walk-forward, net of platform fees. Live forward-test loop tracks IC decay."
- "Deployed a FastAPI + WebSocket real-time signal monitor (p95 latency Z ms) and a multi-user Flask/React SaaS (JWT, paid tier, 375 tests)."

### Interview questions to rehearse

- "How do you know it's not overfit?"
- "What is the Sharpe after costs, and what is its standard error?"
- "Why would this edge exist and persist?"
- "What is the capacity?"
- "Worst bug you found in your backtester?"
- "How did you avoid look-ahead in the regime and sector filters?"
- "Which single signal would you keep, and why?"

### References for section C

Standard literature, cited by title; not re-checked this session.

- Bailey and López de Prado (2014), *The Deflated Sharpe Ratio*, JPM.
- Bailey, Borwein, López de Prado and Zhu (2014), *Pseudo-Mathematics and Financial Charlatanism*, Notices of the AMS.
- Bailey et al. (2017), *The Probability of Backtest Overfitting*, J. Computational Finance.
- White (2000), *A Reality Check for Data Snooping*, Econometrica.
- Hansen (2005), *A Test for Superior Predictive Ability*, JBES.
- Sullivan, Timmermann and White (1999), *Data-Snooping, Technical Trading Rule Performance, and the Bootstrap*, JF.
- Brock, Lakonishok and LeBaron (1992), *Simple Technical Trading Rules...*, JF.
- Lo, Mamaysky and Wang (2000), *Foundations of Technical Analysis*, JF.
- Harvey, Liu and Zhu (2016), *...and the Cross-Section of Expected Returns*, RFS.
- Kyle (1985), *Continuous Auctions and Insider Trading*, Econometrica.
- Glosten and Milgrom (1985), JFE.
- Cont, Kukanov and Stoikov (2014), *The Price Impact of Order Book Events*, JFEc.
- Avellaneda and Stoikov (2008), *High-frequency trading in a limit order book*, QF.
- Amihud (2002), *Illiquidity and Stock Returns*, JFM.
- Moskowitz and Grinblatt (1999), *Do Industries Explain Momentum?*, JF.
- López de Prado (2018), *Advances in Financial Machine Learning*.
- Aronson (2006), *Evidence-Based Technical Analysis*. This is the best bridge from TA to statistics for this candidate.

---

## D. Certifications and learning resources (practical)

| Item | Verdict for this path | Notes |
|---|---|---|
| **CFA Level I** | **Not now** for quant dev, trading systems, fintech or QR. **Maybe later** for investment-analytics or portfolio-engineering roles at asset managers | PIMCO's QRA listings mention "educational/CFA certification reimbursement" as a benefit [S] ([search result, PIMCO QRA listings](https://www.efinancialcareers.com/jobs-USA-CA-Newport_Beach-Quantitative_Research_Analyst.id22524074)), so let an employer pay. Roughly 300 study hours; about $1K+ in fees [B, unverified]. Studying the fixed-income and portfolio chapters (free notes) gives most of the interview value |
| **SIE (FINRA)** | Skip unless targeting broker-dealer ops or trading-assistant roles | About $80, no firm sponsor needed, valid 4 years [B]. Engineers don't need it; trader registrations (e.g., Series 57) are firm-sponsored [B] |
| **FRM Part I** | Optional for A5/A6 risk roles; low priority | Cost and time are high relative to a project [B] |
| **CQF / MFE certificates** | Skip at this stage | [B] |
| **AWS Associate (Developer or Solutions Architect)** | Modest plus for A4/A6 | [B] |

**Books and resources by need** (all [B] except where marked)

- **Quant interviews:**
  - *A Practical Guide to Quantitative Finance Interviews* (Xinfeng Zhou, "Green Book").
  - *Heard on the Street* (Timothy Falcon Crack).
  - *Quant Job Interview Questions and Answers* (Joshi et al.).
  - *Fifty Challenging Problems in Probability* (Mosteller).
  - Ross, *A First Course in Probability*.
  - Practice sites: QuantGuide, OpenQuant ([openquant.co](https://openquant.co/), seen as a quant job board [S]), Brainstellar, Jane Street monthly puzzles.
  - Zetamac-style arithmetic drills for prop-trading and market-making interviews.
- **Research rigor:**
  - López de Prado, *Advances in Financial Machine Learning*.
  - Aronson, *Evidence-Based Technical Analysis*.
  - Ernest Chan, *Quantitative Trading* / *Algorithmic Trading*.
  - Grinold and Kahn, *Active Portfolio Management*.
  - Ilmanen, *Expected Returns*; Pedersen, *Efficiently Inefficient*.
- **Microstructure and trading systems:**
  - Harris, *Trading and Exchanges*.
  - Barry Johnson, *Algorithmic Trading and DMA*.
  - Williams, *C++ Concurrency in Action*.
  - *Hacking the Trading Systems Engineer Interview (C++ Edition)* ([Amazon](https://www.amazon.com/Hacking-Trading-Systems-Engineer-Interview/dp/B089M5B3R7)) [S exists].
  - Optiver's CppCon low-latency talk ([Optiver blog](https://www.optiver.com/insights/technology-blog/designing-low-latency-cpp-systems/)) [S].
- **Fixed income (PIMCO, Capital Group):**
  - Donald Smith, *Bond Math*.
  - Tuckman and Serrat, *Fixed Income Securities*.
  - Hull, *Options, Futures, and Other Derivatives*.
- **Credit risk:**
  - Siddiqi, *Intelligent Credit Scoring*.
  - Baesens, Rösch and Scheule, *Credit Risk Analytics*.
- **Fintech backend:**
  - Kleppmann, *Designing Data-Intensive Applications*.
  - Alex Xu, *System Design Interview* vols 1-2.
  - LeetCode (NeetCode 150).
- **Courses:**
  - Georgia Tech ML4T (CS 7646) public materials.
  - MIT OCW 18.S096 (Mathematics with Applications in Finance).
  - Columbia's *Financial Engineering and Risk Management* (Coursera).
- **Verifiable track-record platforms** (better than certificates for quant roles):
  - Kaggle market competitions (Jane Street, Optiver).
  - Numerai tournament.
  - WorldQuant BRAIN.
  - Results there are third-party verifiable, unlike personal P&L.
