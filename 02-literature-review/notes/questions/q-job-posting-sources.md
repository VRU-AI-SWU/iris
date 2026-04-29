---
type: question
owner: Data Engineer
status: open
---

## Question
Where can we obtain Thai job posting datasets ethically and legally?

## Why This Matters for Iris
Data sourcing affects the representativeness of the market skill distribution and the legality and reproducibility of the research. Academic publication requires defensible data provenance.

## Initial Hypothesis
Primary candidates: JobThai.com (largest Thai portal, likely scraping-friendly), JobsDB Thailand, Indeed Thailand. LinkedIn Thailand is a strong signal but has aggressive anti-scraping defences. A static snapshot dataset is preferred for v1 to avoid live scraping complexity.

## Papers Addressing This
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — uses JobThai.com and JobsDB Thailand via web scraping; confirms both are accessible for research
- [[lertmethaphat-2025-thai-job-market-nlp]] — uses "major Thai online job posting websites" (not named); confirms bilingual Thai+English postings are common
- [[chaiaroon-2025-thai-digital-workforce-matching]] — uses "Thailand's leading recruitment platforms" for digital sector analysis (platforms not named)
- [[tipsena-2025-predicting-thai-digital-workforce]] — scrapes **10 Thai job advertisement websites** (2023–2024); 24,494 positions; platform names not disclosed in paper

## Current Working Answer
status: partial

**Confirmed viable sources:**
- **JobThai.com** — largest Thai job portal; confirmed used in academic research (2018); web scraping feasible
- **JobsDB Thailand** — second major platform; confirmed used in academic research; third-party scraper tools exist (Apify)
- **Indeed Thailand** — global platform with Thai listings; bilingual content

**Likely additional sources** (implied by tipsena-2025's 10-platform list, names undisclosed):
- Jobbkk.com — major Thai portal
- Jobtopgun.com — tech-focused Thai portal
- Workventure.com — startup/tech focus
- SCB/SCG career portals — large corporate direct-hire
- Contact tipsena-2025 authors (wirach@kku.ac.th, Khon Kaen University) to request the full platform list

**Not yet confirmed for research use:**
- LinkedIn Thailand — strong signal but aggressive anti-scraping; supplementary only
- Platform-specific terms of service for academic use not yet verified

**Data ethics**: Scraping is technically feasible from the above. Academic use typically requires: no PII collection, aggregate analysis only, disclosure in methods. Thai PDPA (Personal Data Protection Act 2019) applies — company names and job requirements are generally not personal data, but applicant data would be.

## Remaining Uncertainty
Exact ToS status of all platforms for academic scraping. Whether a pre-existing Thai job posting dataset from tipsena-2025 or other groups is available for direct reuse. Whether PIER DP228 dataset is accessible.
