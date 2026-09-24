# California / remote-from-California finance employers (outside LA & Orange County)

Research date: 2026-09-24. Scope: (A) quant / HFT / systematic / asset-manager firms with Bay Area or San Diego offices; (B) Bay Area or remote-US fintech, payments, crypto, prediction-market and sportsbook employers. Candidate: UCI MS EECS, strong Python/Java/React, equity signal system + backtester + walk-forward, CS2 order-book trading agent, deployed SaaS; likely needs visa sponsorship.

**How far to trust this file:**
- The session-wide WebSearch budget (200 calls, shared with the parallel research agents) ran out after Part A had been researched (~44 searches). **Part B could not be searched at all.**
- `VERIFIED` means the fact appeared in a 2025-2026 search result in this session; the URL is listed under `sources`. A few facts came from search results that parallel agents in this same session had already retrieved; these are marked "(sibling search)".
- `UNVERIFIED` means the item comes from the researcher's prior knowledge (training data, cutoff ~mid-2026) and must be checked. **Every Part B entry is UNVERIFIED end to end** (ATS tokens, remote policy, new-grad status, H-1B, company news).
- H-1B: **only Voleon's filings were confirmed** (h1bdata.info / 1point3acres). All other `h1b` values are UNVERIFIED.

```yaml
# ---------------- PART A: quant / trading / asset managers with a California office ----------------
- name: "The Voleon Group"
  city: "Berkeley"
  region: BAY
  category: quant_hedge_fund
  roles:
    - "VERIFIED: Software Engineer - University Hire 2026 (Berkeley; posted $160-190K; Python/Go/C++, Linux, backend, databases, large-scale data processing)"
    - "VERIFIED: Software Engineer Intern - Summer 2026 and Summer 2027 (Ashby posting for 2027 is live)"
    - "VERIFIED: Software Engineer (full-time, posted $135-185K); Senior Software Engineer, Platform Team"
    - "VERIFIED: work spans real-time trading systems, distributed data processing, ML research infrastructure"
  new_grad: "YES (VERIFIED) - explicit University Hire 2026 SWE posting plus 2027 intern pipeline"
  ats: "Ashby (current); Lever (legacy board still indexed)"
  ats_id: "voleon (jobs.ashbyhq.com/voleon); legacy jobs.lever.co/voleon"
  careers_url: "https://www.voleon.com/jobs/"
  h1b: "VERIFIED low-volume sponsor - LCA records for 'Voleon Capital Management LP' on h1bdata.info (incl. Senior Software Engineer, 2023) and 1point3acres (~11-21 records per snippets). One job-board copy of the posting mentions US work authorization, so confirm sponsorship with the recruiter."
  fit: "Best California quant match: ML-driven systematic fund, Python-heavy research and trading infrastructure, real new-grad pipeline. The backtester and walk-forward work maps directly. Very selective."
  sources:
    - "https://jobs.ashbyhq.com/voleon/57f1b666-2f4b-4bad-aac0-fa42a1c8fdf6"
    - "https://www.jointaro.com/jobs/the-voleon-group/software-engineer-university-hire-2026/"
    - "https://jobs.lever.co/voleon/?by=team&location=Berkeley%2C+CA"
    - "https://www.voleon.com/jobs/"
    - "https://haystackapp.io/jobs/29c1e278-60f6-4ae5-b6f3-b20ef4f1f573"
    - "https://h1bdata.info/index.php?em=voleon+capital+management+lp"
    - "https://h1bdata.info/index.php?em=VOLEON+CAPITAL+MANAGEMENT+LP&job=SENIOR+SOFTWARE+ENGINEER&city=&year="
    - "https://visa.1point3acres.com/h1b/salary/voleon-capital-management-lp"

- name: "Headlands Technologies"
  city: "San Francisco (4 Embarcadero Center, Ste 750)"
  region: BAY
  category: prop_trading
  roles:
    - "VERIFIED: C++ Software Developer - New Grad (Greenhouse job 4336806009; appeared in a 2026-09-17 job-scrape feed, so likely still open)"
    - "VERIFIED: C++ Software Developer (experienced; Greenhouse job 4227758009) - exchange connectivity, low-latency networking, distributed storage, research infrastructure"
  new_grad: "YES (VERIFIED) - dedicated New Grad posting; whether the new-grad seat is in SF or Chicago is UNVERIFIED"
  ats: "Greenhouse"
  ats_id: "headlandstechnologiesllc"
  careers_url: "https://www.headlandstech.com/careers/"
  h1b: "UNVERIFIED (search budget ran out before this check)"
  fit: "Genuine HFT / market maker with an SF office (Chicago, London, SF). Developer roles are C++-first, while the candidate is Python/Java, so this is a stretch target that needs visible C++ work."
  sources:
    - "https://job-boards.greenhouse.io/headlandstechnologiesllc"
    - "https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/4336806009"
    - "https://job-boards.greenhouse.io/headlandstechnologiesllc/jobs/4227758009"
    - "https://github.com/abhiramgorle/Job-Notifications/issues/12730"
    - "https://www.dnb.com/business-directory/company-profiles.headlands_technologies_llc.ed01e09645594908974ec3eb43e7fba6.html"
    - "https://en.wikipedia.org/wiki/Headlands_Technologies"
    - "https://www.headlandstech.com/careers/"

- name: "Citadel (hedge fund)"
  city: "San Francisco (4 Embarcadero Center, per office-locations search summary)"
  region: BAY
  category: quant_hedge_fund
  roles:
    - "VERIFIED: Software Engineer (general posting, citadel.com)"
    - "VERIFIED (sibling search): Quantitative Research Analyst - University Graduate (US), base $235-300K; listed locations New York, Miami, Greenwich (not SF)"
    - "VERIFIED (sibling search): Quantitative Research Engineer - University Graduate (US), base $200-250K"
    - "VERIFIED: LinkedIn showed ~16 Citadel jobs in the SF Bay Area (titles not captured)"
  new_grad: "YES firm-wide, but campus postings list NY/Miami/Greenwich; SF new-grad seats UNVERIFIED"
  ats: "Own careers site (citadel.com/careers/details/...); underlying ATS UNVERIFIED"
  ats_id: "n/a"
  careers_url: "https://www.citadel.com/careers/open-opportunities/"
  h1b: "UNVERIFIED in this session (prior knowledge: large, consistent sponsor)"
  fit: "Elite, very selective. The SF office is small, so plan on 'campus program anywhere, SF if offered'. Python and quant-research-engineer tracks suit the candidate."
  sources:
    - "https://www.citadel.com/who-we-are/office-locations/"
    - "https://www.builtinsf.com/company/citadel/offices"
    - "https://www.linkedin.com/jobs/citadel-jobs-san-francisco-bay-area"
    - "https://www.citadel.com/careers/details/software-engineer/"
    - "https://www.citadel.com/careers/details/quantitative-research-analyst-university-graduate-us/"
    - "https://www.citadel.com/careers/details/quantitative-research-engineer-university-graduate-us/"

- name: "Citadel Securities"
  city: "San Francisco (Built In SF lists SF as one of 3 offices; NOT confirmed on the official office page)"
  region: BAY
  category: prop_trading
  roles:
    - "VERIFIED (sibling search): Software Engineer - University Graduate (US), base $235-300K"
    - "VERIFIED: Software Engineer - Intern (US); C++ Software Engineer (base $150-300K); Senior Python Software Engineer (base $125-350K); Full Stack Software Engineer; Quantitative Developer/Research Engineer (base $250-350K)"
  new_grad: "YES (University Graduate SWE program); the SF location for new grads is UNVERIFIED (Miami/NYC/Chicago are the usual locations)"
  ats: "Own careers site (citadelsecurities.com/careers/details/...); underlying ATS UNVERIFIED"
  ats_id: "n/a"
  careers_url: "https://www.citadelsecurities.com/careers/open-opportunities/"
  h1b: "UNVERIFIED (prior knowledge: large sponsor)"
  fit: "Top market maker with Python and full-stack SWE tracks that suit the candidate. Its SF presence is unconfirmed, so apply with location flexibility."
  sources:
    - "https://www.builtinsf.com/company/citadel-securities/offices"
    - "https://www.builtinsf.com/company/citadel-securities"
    - "https://www.citadelsecurities.com/careers/details/software-engineer-university-graduate-us/"
    - "https://www.citadelsecurities.com/careers/details/software-engineer-intern-us/"
    - "https://www.citadelsecurities.com/careers/details/c-software-engineer-2/"
    - "https://www.citadelsecurities.com/careers/details/senior-python-software-engineer/"
    - "https://www.citadelsecurities.com/careers/details/quantitative-developer-research-engineer/"
    - "https://www.citadelsecurities.com/who-we-are/office-locations/"

- name: "Susquehanna International Group (SIG)"
  city: "San Francisco (101 California St, Suite 3250)"
  region: BAY
  category: prop_trading
  roles:
    - "No SF-specific engineering or quant posting found. SIG's 2026 campus SWE/quant programs appear in Bala Cynwyd/Chicago/NYC/London (SF seats UNVERIFIED)"
  new_grad: "YES firm-wide (well-known campus programs); SF seats UNVERIFIED"
  ats: "UNVERIFIED"
  ats_id: "UNVERIFIED"
  careers_url: "https://sig.com/who-we-are/office-locations/ (careers section of sig.com; exact path UNVERIFIED)"
  h1b: "UNVERIFIED (prior knowledge: established sponsor)"
  fit: "An SF office exists and Glassdoor has SF salary entries, but what the SF team does is unknown. Apply through SIG's main programs and ask about SF."
  sources:
    - "https://sig.com/who-we-are/office-locations/"
    - "https://www.glassdoor.com/Location/Susquehanna-International-Group-SIG-San-Francisco-Location-EI_IE24446.0,35_IL.36,49_IC1147401.htm"
    - "https://www.glassdoor.com/Salary/Susquehanna-International-Group-SIG-San-Francisco-Salaries-EI_IE24446.0,35_IL.36,49_IM759.htm"

- name: "Numerai"
  city: "San Francisco"
  region: BAY
  category: quant_hedge_fund
  roles:
    - "VERIFIED: Quantitative Research Engineer (posted Jan 16, 2026; systems supporting Numerai's data, research and trading pipeline)"
    - "VERIFIED: Lead Software Engineer (new team building autonomous AI for quant research; listing ran to 9/22/2026)"
  new_grad: "LOW - small team; postings read mid/senior"
  ats: "UNVERIFIED (postings seen via Wellfound, Built In SF, Long Journey VC job board)"
  ats_id: "UNVERIFIED"
  careers_url: "https://wellfound.com/company/numerai/jobs"
  h1b: "UNVERIFIED"
  fit: "Crypto-native (NMR) crowd-sourced ML hedge fund. Walk-forward validation and signal work are exactly on theme. Hiring volume is small, so contact the team directly."
  sources:
    - "https://www.builtinsf.com/company/numerai"
    - "https://www.builtinsf.com/company/numerai/jobs"
    - "https://wellfound.com/jobs/1260403-quantitative-research-engineer"
    - "https://jobs.longjourney.vc/companies/numerai/jobs/65302148-quantitative-research-engineer"
    - "https://bebee.com/us/jobs/lead-software-engineer-numerai-san-francisco--lensa-7428_7a66be10acb13cf139689fa4f8b333501f06c5bb0fc25b6bc396ad1861fb94a2"
    - "https://cryptocurrencyjobs.co/startups/numerai/"

- name: "BlackRock (San Francisco - Aladdin engineering, systematic/quant research)"
  city: "San Francisco"
  region: BAY
  category: asset_manager
  roles:
    - "VERIFIED: Full Stack Java Engineer - Aladdin Product Engineering, Associate (SF, $132.5-162K)"
    - "VERIFIED: AI-Augmented Full Stack Engineer, Aladdin Engineering, Post Trade Investment Operations - VP (SF, $162-215K)"
    - "VERIFIED: Associate, Application Engineer - Aladdin Trading (SF, Built In SF)"
    - "VERIFIED (Glassdoor snippet): Analyst, Quant Research ($112-133K); Quantitative/Systematic Research Associate ($133-162K); Associate Full Stack Engineer - SF"
    - "VERIFIED: an SF software-engineering posting with a $71.25-135K range (analyst-level)"
  new_grad: "YES - analyst-level SF engineering posting plus a campus Software Engineering program page; SF seats for the 2027 cycle UNVERIFIED"
  ats: "Workday (careers.blackrock.com front end)"
  ats_id: "blackrock.wd1.myworkdayjobs.com/BlackRock_Professional"
  careers_url: "https://careers.blackrock.com/location/san-francisco-jobs/45831/6252001-5332921-5391959/4"
  h1b: "UNVERIFIED in this session (prior knowledge: large sponsor)"
  fit: "Strong and accessible: Java full stack + React is exactly the Aladdin engineering profile, and SF also hosts BlackRock Systematic / quant research. Probably the most realistic large-employer target in SF."
  sources:
    - "https://careers.blackrock.com/job/san-francisco/full-stack-java-engineer-aladdin-product-engineering-associate/45831/82938495872"
    - "https://careers.blackrock.com/job/san-francisco/ai-augmented-full-stack-engineer-aladdin-engineering-post-trade-investment-operations-vice-president/45831/92884734032"
    - "https://www.builtinsf.com/job/associate-application-engineer-aladdin-trading/4416057"
    - "https://careers.blackrock.com/employment/san-francisco-california-united-states-software-engineering-jobs/45831/8771056/6252001-5332921-5391997-5391959/4"
    - "https://blackrock.wd1.myworkdayjobs.com/BlackRock_Professional"
    - "https://careers.blackrock.com/students-and-graduates-functions-software-engineering"
    - "https://www.glassdoor.com/Jobs/BlackRock-San-Francisco-Jobs-EI_IE9331.0,9_IL.10,23_IC1147401.htm"

- name: "Charles Schwab"
  city: "San Francisco (corporate HQ is Westlake, TX - prior knowledge, UNVERIFIED)"
  region: BAY
  category: asset_manager
  roles:
    - "VERIFIED: 'Engineering & Software Development' job listings filtered to San Francisco and to California on schwabjobs.com"
    - "VERIFIED (location UNVERIFIED): Quantitative Software Engineer (Python); Sr Specialist Quantitative Software Engineer"
    - "VERIFIED: requisition 2026-123172 engineering role at $50.48-60.10/hr (type and location UNVERIFIED)"
  new_grad: "UNVERIFIED (prior knowledge: tech internships and new-grad programs exist, mostly in TX/AZ/CO)"
  ats: "schwabjobs.com (Radancy front end); underlying ATS UNVERIFIED"
  ats_id: "UNVERIFIED"
  careers_url: "https://www.schwabjobs.com/"
  h1b: "UNVERIFIED"
  fit: "Brokerage and asset manager with Python quant-SWE roles. SF engineering openings exist, but much of Schwab's tech hiring is in Texas/Colorado/Arizona."
  sources:
    - "https://www.schwabjobs.com/employment/san-francisco-california-united-states-engineering-and-software-development-jobs/33727/8421664/6252001-5332921-5391997-5391959/4"
    - "https://www.schwabjobs.com/employment/california-united-states-engineering-and-software-development-jobs/27326/8421664/6252001-5332921/3"
    - "https://www.themuse.com/jobs/charlesschwab/quantitative-software-engineer-python"
    - "https://www.themuse.com/jobs/charlesschwab/sr-specialist-quantitative-software-engineer-72d01b"

- name: "Dodge & Cox"
  city: "San Francisco (HQ)"
  region: BAY
  category: asset_manager
  roles:
    - "VERIFIED: software development roles (design/develop/install software solutions) among ~10-11 open US jobs"
    - "VERIFIED: Portfolio Analyst / Investment Associate; client service; operations"
  new_grad: "LOW-MEDIUM - ~376 employees (Jan 31, 2026); tech new-grad intake UNVERIFIED"
  ats: "Workday"
  ats_id: "dodgeandcox.wd5.myworkdayjobs.com/Dodgecox"
  careers_url: "https://dodgeandcox.wd5.myworkdayjobs.com/Dodgecox"
  h1b: "UNVERIFIED"
  fit: "Stable fundamental manager (>$475B AUM) with few tech openings and 4 days/week in office. Weak match for the trading-systems interest."
  sources:
    - "https://dodgeandcox.wd5.myworkdayjobs.com/Dodgecox"
    - "https://www.glassdoor.com/Jobs/Dodge-and-Cox-Jobs-E31663.htm"
    - "https://www.indeed.com/cmp/Dodge-&-Cox"

- name: "Franklin Templeton"
  city: "San Mateo (HQ, One Franklin Parkway)"
  region: BAY
  category: asset_manager
  roles:
    - "VERIFIED: Senior Software Engineer (Workday req 864529)"
    - "VERIFIED: Senior AI/ML Engineer, Equity Research Analyst, SVP roles in San Mateo (6-20 San Mateo listings per Indeed/LinkedIn)"
  new_grad: "LOW-MEDIUM (UNVERIFIED) - the San Mateo openings seen were senior"
  ats: "Workday"
  ats_id: "franklintempleton.wd5.myworkdayjobs.com/en-US/Primary-External-1"
  careers_url: "https://careers.franklintempleton.com/us/en"
  h1b: "UNVERIFIED"
  fit: "Large asset manager HQ'd in the Bay Area. AI/ML and data-engineering roles fit the Python side, but there are few entry-level seats."
  sources:
    - "https://franklintempleton.wd5.myworkdayjobs.com/en-US/Primary-External-1/job/Senior-Software-Engineer_864529"
    - "https://www.linkedin.com/jobs/franklin-templeton-jobs-san-mateo-ca"
    - "https://careers.franklintempleton.com/us/en"
    - "https://www.franklintempletoncareers.com/country-location/us/san-mateo"

# ---------------- PART B: fintech / payments / crypto / prediction markets / sportsbooks ----------------
# EVERYTHING BELOW IS UNVERIFIED (no search evidence; the session search budget was exhausted). Prior knowledge only.
- name: "Robinhood"
  city: "Menlo Park (HQ)"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: backend SWE (brokerage, options, crypto, clearing, prediction-markets/event contracts), Software Engineer New Grad, data/ML"]
  new_grad: "UNVERIFIED - historically yes (new-grad SWE in Menlo Park/NYC)"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "robinhood (UNVERIFIED)"
  careers_url: "https://careers.robinhood.com/ (UNVERIFIED)"
  h1b: "UNVERIFIED (prior knowledge: regular sponsor)"
  fit: "Top Bay Area fintech fit: retail trading platform, Python/Go backend. Mostly in-office. Prediction-markets product is on-interest."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Stripe"
  city: "South San Francisco / San Francisco"
  region: BAY
  category: payments
  roles: ["UNVERIFIED: Software Engineer New Grad; backend/infra SWE; stablecoin/crypto (Bridge) teams"]
  new_grad: "UNVERIFIED - historically an annual 'Software Engineer, New Grad' posting"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "stripe (UNVERIFIED)"
  careers_url: "https://stripe.com/jobs"
  h1b: "UNVERIFIED (prior knowledge: very large sponsor)"
  fit: "Payments infrastructure, Java/Ruby. Strong brand and sponsor. Remote-US roles exist mainly for experienced hires (UNVERIFIED)."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Coinbase"
  city: "Remote-first (no HQ); SF presence"
  region: REMOTE
  category: crypto
  roles: ["UNVERIFIED: backend SWE (exchange, trading, derivatives), University Grad SWE"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "Greenhouse (UNVERIFIED; coinbase.com/careers/positions/<id>?gh_jid=...)"
  ats_id: "coinbase (UNVERIFIED)"
  careers_url: "https://www.coinbase.com/careers"
  h1b: "UNVERIFIED (prior knowledge: large sponsor)"
  fit: "Best remote-from-California crypto option: exchange plus derivatives (Deribit acquisition 2025, UNVERIFIED). Go/Python."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Kraken (Payward Inc.)"
  city: "Remote-first (historically SF-based)"
  region: REMOTE
  category: crypto
  roles: ["UNVERIFIED: exchange/trading-engine backend (Rust), NinjaTrader futures integration"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "Ashby (UNVERIFIED; previously Lever)"
  ats_id: "kraken.com (UNVERIFIED); legacy Lever site 'kraken123' (UNVERIFIED)"
  careers_url: "https://www.kraken.com/careers"
  h1b: "UNVERIFIED"
  fit: "Fully remote crypto exchange. Rust-heavy core; few new-grad seats."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Ripple"
  city: "San Francisco (HQ)"
  region: BAY
  category: crypto
  roles: ["UNVERIFIED: SWE (cross-border payments, custody, stablecoin, prime brokerage via Hidden Road), intern/new-grad program"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "ripple (UNVERIFIED)"
  careers_url: "https://ripple.com/careers/"
  h1b: "UNVERIFIED (prior knowledge: regular sponsor)"
  fit: "SF crypto-payments company. The 2025 prime-broker acquisition (Hidden Road, UNVERIFIED) adds trading-infrastructure work."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Plaid"
  city: "San Francisco (HQ)"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE (Go/Python/TypeScript), new grad historically"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "Lever (UNVERIFIED; may have migrated)"
  ats_id: "plaid (UNVERIFIED)"
  careers_url: "https://plaid.com/careers/"
  h1b: "UNVERIFIED (prior knowledge: sponsor)"
  fit: "Fintech data infrastructure. Solid SWE brand, but less trading-centric."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Chime"
  city: "San Francisco (HQ)"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE, risk/fraud ML, data"]
  new_grad: "UNVERIFIED - limited"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "chime (UNVERIFIED)"
  careers_url: "https://careers.chime.com/"
  h1b: "UNVERIFIED"
  fit: "Consumer neobank (public since mid-2025, UNVERIFIED). Risk and fraud data work is money-adjacent."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Brex"
  city: "San Francisco"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE (spend management, payments)"]
  new_grad: "UNVERIFIED - limited"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "brex (UNVERIFIED)"
  careers_url: "https://www.brex.com/careers"
  h1b: "UNVERIFIED"
  fit: "Corporate cards and spend management. A Capital One acquisition was reportedly announced in Jan 2026 (UNVERIFIED), so hiring may be in flux."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "SoFi"
  city: "San Francisco (HQ)"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE, data, risk; SoFi Invest / crypto"]
  new_grad: "UNVERIFIED"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "sofi (UNVERIFIED)"
  careers_url: "https://www.sofi.com/careers/"
  h1b: "UNVERIFIED (prior knowledge: sponsor)"
  fit: "Bank + brokerage + crypto. Many tech roles sit outside CA (TX/UT/WA, UNVERIFIED)."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Wealthfront"
  city: "Palo Alto (HQ)"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE (Java backend, web/mobile), new grad"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "Lever (UNVERIFIED)"
  ats_id: "wealthfront (UNVERIFIED)"
  careers_url: "https://www.wealthfront.com/careers"
  h1b: "UNVERIFIED (prior knowledge: sponsor)"
  fit: "Automated investing and tax-loss harvesting. The Java backend + React stack matches the candidate well. Reportedly IPO'd Dec 2025 (UNVERIFIED)."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Block (Square, Cash App)"
  city: "Oakland (HQ) / San Francisco; location-flexible"
  region: BAY
  category: payments
  roles: ["UNVERIFIED: SWE (Cash App, Square, bitcoin/Proto/Bitkey), new grad historically"]
  new_grad: "UNVERIFIED - historically yes; 2026 status unknown"
  ats: "UNVERIFIED (block.xyz/careers)"
  ats_id: "UNVERIFIED"
  careers_url: "https://block.xyz/careers"
  h1b: "UNVERIFIED (prior knowledge: large sponsor)"
  fit: "Payments + bitcoin with a Java/Kotlin backend, a good fit. Reportedly made deep layoffs in early 2026 (UNVERIFIED), so check whether it is hiring."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "PayPal"
  city: "San Jose (HQ)"
  region: BAY
  category: payments
  roles: ["UNVERIFIED: SWE (Java), risk/fraud data science, early-career SWE"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "Workday (UNVERIFIED)"
  ats_id: "paypal.wd1.myworkdayjobs.com/jobs (UNVERIFIED)"
  careers_url: "https://careers.pypl.com/"
  h1b: "UNVERIFIED (prior knowledge: very large sponsor)"
  fit: "Java-heavy payments plus risk ML at a big, steady sponsor in San Jose."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Visa"
  city: "San Francisco (HQ) / Foster City"
  region: BAY
  category: payments
  roles: ["UNVERIFIED: SWE, data engineering, early-career SWE (Foster City)"]
  new_grad: "UNVERIFIED - historically yes"
  ats: "SmartRecruiters (UNVERIFIED)"
  ats_id: "Visa (UNVERIFIED; jobs.smartrecruiters.com/Visa)"
  careers_url: "https://corporate.visa.com/en/jobs/"
  h1b: "UNVERIFIED (prior knowledge: very large sponsor)"
  fit: "Payments network and strong sponsor. Less trading-centric."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Intuit (incl. Credit Karma)"
  city: "San Diego (large campus) + Mountain View HQ"
  region: SD
  category: fintech
  roles: ["UNVERIFIED: new-grad SWE, rotational development program, QuickBooks/TurboTax/Credit Karma data & ML"]
  new_grad: "UNVERIFIED - historically a large new-grad intake, including San Diego"
  ats: "UNVERIFIED (jobs.intuit.com front end)"
  ats_id: "UNVERIFIED"
  careers_url: "https://jobs.intuit.com/"
  h1b: "UNVERIFIED (prior knowledge: very large sponsor)"
  fit: "San Diego is the nearest non-LA/OC option to Irvine. The work is money-adjacent (tax, credit, SMB finance) rather than trading."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Carta"
  city: "San Francisco"
  region: BAY
  category: fintech
  roles: ["UNVERIFIED: SWE (Python/Django), fund administration"]
  new_grad: "UNVERIFIED - limited"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "carta (UNVERIFIED)"
  careers_url: "https://carta.com/careers/"
  h1b: "UNVERIFIED"
  fit: "Python-heavy private-markets fintech (cap tables, fund admin)."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Mercury"
  city: "San Francisco; remote-first in US"
  region: REMOTE
  category: fintech
  roles: ["UNVERIFIED: SWE (Haskell backend, TypeScript/React frontend)"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "mercury (UNVERIFIED)"
  careers_url: "https://mercury.com/jobs"
  h1b: "UNVERIFIED"
  fit: "Startup banking. React fits; the Haskell backend does not."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Anchorage Digital"
  city: "San Francisco / remote-first"
  region: REMOTE
  category: crypto
  roles: ["UNVERIFIED: Go backend (custody, trading, staking, settlement)"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "Lever (UNVERIFIED)"
  ats_id: "anchorage (UNVERIFIED)"
  careers_url: "https://www.anchorage.com/careers"
  h1b: "UNVERIFIED"
  fit: "Federally chartered crypto bank with trading/custody work. Go-heavy, remote."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Alpaca"
  city: "San Mateo HQ; remote-first"
  region: REMOTE
  category: fintech
  roles: ["UNVERIFIED: Go backend, brokerage/trading API, crypto"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "Ashby (UNVERIFIED)"
  ats_id: "alpaca (UNVERIFIED)"
  careers_url: "https://alpaca.markets/careers"
  h1b: "UNVERIFIED"
  fit: "Brokerage API for algorithmic traders. The candidate's signal/backtest system is Alpaca's core use case, which makes a strong pitch."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Kalshi"
  city: "NYC HQ; CA or remote roles UNVERIFIED"
  region: REMOTE
  category: prediction_market
  roles: ["UNVERIFIED: SWE, exchange/matching engine, market operations, quant"]
  new_grad: "UNVERIFIED"
  ats: "UNVERIFIED (Ashby suspected)"
  ats_id: "UNVERIFIED"
  careers_url: "https://kalshi.com/careers (UNVERIFIED)"
  h1b: "UNVERIFIED"
  fit: "Squarely on-interest (CFTC-regulated prediction markets), but prior knowledge suggests mostly in-person NYC, so probably not a California option. Verify."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Polymarket"
  city: "NYC HQ; remote roles UNVERIFIED"
  region: REMOTE
  category: prediction_market
  roles: ["UNVERIFIED: SWE (exchange, smart contracts, data)"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "UNVERIFIED (Ashby suspected)"
  ats_id: "UNVERIFIED"
  careers_url: "UNVERIFIED"
  h1b: "UNVERIFIED"
  fit: "On-interest but a small team. Relaunched in the US after a 2025 acquisition of a CFTC-licensed exchange (UNVERIFIED)."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "DraftKings"
  city: "Boston HQ; no CA office known"
  region: REMOTE
  category: sportsbook
  roles: ["UNVERIFIED: sports trading/pricing, quant, SWE, DraftKings Predictions"]
  new_grad: "UNVERIFIED"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "draftkings (UNVERIFIED)"
  careers_url: "https://careers.draftkings.com/"
  h1b: "UNVERIFIED (prior knowledge: sponsor)"
  fit: "Pricing and trading work matches the interest, but roles sit outside CA and remote-from-CA eligibility is unverified. Online sports betting is not legal in California."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "FanDuel"
  city: "NYC HQ; LA-area presence (TVG/FanDuel TV, outside this file's scope; UNVERIFIED)"
  region: REMOTE
  category: sportsbook
  roles: ["UNVERIFIED: trading/pricing, quant, SWE; FanDuel Predicts"]
  new_grad: "UNVERIFIED"
  ats: "Greenhouse (UNVERIFIED)"
  ats_id: "fanduel (UNVERIFIED)"
  careers_url: "https://careers.fanduel.com/"
  h1b: "UNVERIFIED"
  fit: "Trading and pricing roles are usually NYC or overseas (UNVERIFIED). Any LA roles belong to the LA/OC research track."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "PrizePicks"
  city: "Atlanta HQ; remote-friendly (UNVERIFIED)"
  region: REMOTE
  category: sportsbook
  roles: ["UNVERIFIED: SWE, data, pricing/risk"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "UNVERIFIED"
  ats_id: "UNVERIFIED"
  careers_url: "https://www.prizepicks.com/careers (UNVERIFIED)"
  h1b: "UNVERIFIED"
  fit: "DFS pick'em. A California AG opinion (2025) reportedly treated DFS as illegal in CA (UNVERIFIED), which may limit CA-based hiring."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]

- name: "Underdog"
  city: "Brooklyn HQ; remote-first (UNVERIFIED)"
  region: REMOTE
  category: sportsbook
  roles: ["UNVERIFIED: SWE, pricing/risk, prediction-markets product"]
  new_grad: "LOW (UNVERIFIED)"
  ats: "UNVERIFIED"
  ats_id: "UNVERIFIED"
  careers_url: "https://underdogfantasy.com/careers (UNVERIFIED)"
  h1b: "UNVERIFIED"
  fit: "Same California DFS legal caveat as PrizePicks. Remote-from-CA eligibility unverified."
  sources: ["UNVERIFIED - no search evidence gathered (session WebSearch budget exhausted)"]
```

## Firms with NO California office found (Part A)

For all of these, the candidate would have to relocate. Evidence comes from search snippets of each firm's own office/contact page or a directory.

| Firm | Offices found | Confidence | Evidence |
|---|---|---|---|
| Hudson River Trading | NYC HQ, Austin, Chicago + other US/intl; no CA | High | https://www.hudsonrivertrading.com/offices/ |
| Jane Street | Official page: New York, London, Hong Kong, Singapore, Amsterdam. A Handshake profile shows a 220 Montgomery St, SF address (UNVERIFIED; not an official office). | High | https://www.janestreet.com/culture/our-offices/ ; https://app.joinhandshake.com/employers/jane-street-19062 |
| Two Sigma | NYC HQ, Houston + intl (London, HK, Tokyo). The only SF presence is a Two Sigma Ventures investing partner, not an engineering office. | Medium-high | https://twosigma.com/offices ; https://confluencevcweekly.beehiiv.com/p/vinay-iyengar-vc-two-sigma-ventures |
| Jump Trading | Chicago HQ, NYC, Austin + intl. One aggregator claims LA/SF; this conflicts with the other sources and is UNVERIFIED. Greenhouse token `jumptrading`. | Medium | https://craft.co/jump-trading/locations ; https://en.wikipedia.org/wiki/Jump_Trading ; https://job-boards.greenhouse.io/jumptrading/jobs/8003019 |
| Optiver | US: Chicago, Austin, NYC | High | https://www.optiver.com/join-us/locations/ ; https://www.optiver.com/about-us/contact/ |
| IMC Trading | US: Chicago, NYC | High | https://www.imc.com/us/contact/offices |
| DRW | US: Chicago, Austin, Greenwich, Houston, NYC | High | https://www.drw.com/contact-us |
| Akuna Capital | Chicago HQ + Sydney, Shanghai, Singapore, London | High | https://akunacapital.com/who-we-are/ |
| Five Rings | NYC + London | High | https://fiverings.com/contact/ |
| Tower Research | NYC HQ, Chicago (+NJ) + intl | High | https://tower-research.com/offices/ |
| XTX Markets | London, Singapore, NYC, Paris, Bristol, Mumbai, Yerevan, Kajaani | High | https://www.xtxmarkets.com/contact/ ; https://en.wikipedia.org/wiki/XTX_Markets |
| Old Mission | Chicago, NYC, London | High | https://www.oldmissioncapital.com/contact-us/ |
| Radix Trading | Chicago HQ (+NYC), Amsterdam | High | https://en.wikipedia.org/wiki/Radix_Trading ; https://www.radix-trading.com/ |
| Vatic Labs | NYC only | High | https://www.builtinnyc.com/company/vatic-labs ; https://www.vaticlabs.ai/ |
| AQR | Greenwich HQ + intl; no Bay Area/SD office. One older source mentions LA (UNVERIFIED; LA is outside this file's scope). AQR is hiring **Prediction Markets** quant research analysts in Greenwich (Greenhouse via careers.aqr.com, sibling search). | Medium | https://www.aqr.com/Our-Firm/About-Us ; https://craft.co/aqr/locations ; https://careers.aqr.com/jobs/research/greenwich-ct/quantitative-research-prediction-markets-analyst/8018219?gh_jid=8018219 |
| Man Group | US: NYC, Boston (+Stamford/Charlotte per one source). Greenhouse EU token `mangroup`. | High | https://www.man.com/contact ; https://job-boards.eu.greenhouse.io/mangroup/jobs/4798619101 |

Firms with a confirmed California office (Part A): Voleon, Headlands, Citadel, SIG, Numerai, BlackRock, Charles Schwab, Dodge & Cox, Franklin Templeton. Citadel Securities' SF office rests on Built In SF alone and is not confirmed.

## Not researched, possibly worth adding (UNVERIFIED, prior knowledge)
Affirm (SF, remote-first fintech), Upstart (San Mateo, ML credit models, remote-friendly), Addepar (Bay Area wealth tech, Java/Python), Marqeta (Oakland, card issuing), LendingClub (SF), Figure (SF, blockchain lending), Circle (remote-US, stablecoins), Ramp (NYC HQ with an SF office), Paradigm (SF crypto research/investing).

## Suggested follow-up searches if the budget is raised
- `<company> H1B software engineer salary` for Headlands, Citadel, SIG, BlackRock, Schwab, Dodge & Cox, Franklin Templeton, Numerai, Robinhood, Stripe, Coinbase, Wealthfront, Alpaca, Ripple.
- `"job-boards.greenhouse.io/<token>"` / `"jobs.ashbyhq.com/<org>"` / `"jobs.lever.co/<site>"` to confirm each Part B ATS token (robinhood, stripe, coinbase, ripple, brex, chime, sofi, carta, mercury, anchorage, alpaca, kalshi, polymarket, wealthfront, plaid).
- `Kalshi careers San Francisco OR remote`, `Polymarket jobs remote`, `DraftKings remote California trading analyst` to settle the prediction-market and sportsbook CA question.
- `Headlands "New Grad" San Francisco` to confirm the new-grad location, and `Susquehanna San Francisco office team` to learn what SIG's SF office does.
