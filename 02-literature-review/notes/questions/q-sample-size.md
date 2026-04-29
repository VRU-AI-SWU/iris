---
type: question
owner: Data Scientist
status: open
---

## Question
What is the minimum number of job postings needed to produce a stable, representative skill distribution for a given career path?

## Why This Matters for Iris
If we need thousands of postings per career path to get a stable distribution, our data collection scope changes significantly. If a few hundred is sufficient, we can scope v1 more narrowly.

## Initial Hypothesis
None. This is an empirical question that prior work in labour market analytics may have addressed. Stability likely depends on the variance of skill requirements within the career path.

## Papers Addressing This
- [[sabet-2024-course-skill-atlas]] — uses 3M+ U.S. syllabi and national job posting datasets; not directly applicable to Thai career path scope
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — small-scale Thai study; sample size not reported
- [[chaiaroon-2025-thai-digital-workforce-matching]] — covers 20 digital job categories from Thai platforms; sample size not disclosed

## Current Working Answer
status: open

The literature does not provide a specific minimum sample size for stable career-path-level skill distributions. Observations from the literature:
- Large-scale studies (US, EU) operate at hundreds of thousands to millions of postings — not achievable for a Thai career-path-specific study
- Thai studies use smaller samples but do not report convergence thresholds
- Stability likely depends on: skill vocabulary size, career path specificity, and market homogeneity

**Working estimate (not literature-validated):** For a specific Thai CS career path (e.g., Data Science), 200–500 postings likely produce a stable top-N skill distribution. This needs empirical validation in Phase 4.

## Remaining Uncertainty
No paper has studied sample size convergence for skill distributions at the career path level in a small-to-medium labour market like Thailand. This is likely a genuine research gap. We should design our Phase 4 evaluation to include a convergence analysis (plot skill distribution stability vs. posting count) to answer this empirically and contribute it as a methodological finding.
