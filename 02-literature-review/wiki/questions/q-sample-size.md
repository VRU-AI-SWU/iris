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
- [[dixon-2023-occupational-models-42m]] — 42M US postings across 867 SOC codes; at national US scale, 775-skill vocabulary sufficient; implies ~50K+ postings per occupation code
- [[tipsena-2025-predicting-thai-digital-workforce]] — 24,494 Thai digital job positions across 5 segments (~4,900 per segment); this is the largest recent Thai benchmark

## Current Working Answer
status: partial

The literature does not provide a specific minimum sample size for stable career-path-level skill distributions. Updated observations:
- US national scale (dixon-2023): 42M postings → 775 skills / 867 occupation codes ≈ 48K postings per code. Not applicable to our scope.
- Thai digital industry (tipsena-2025): 24,494 positions across 5 segments ≈ 4,900 per segment. This is from 10 platforms over 2 years — a more realistic Thai benchmark.
- Thai studies use smaller samples but do not report convergence thresholds
- Stability likely depends on: skill vocabulary size, career path specificity, and market homogeneity

**Updated working estimate:** For a specific Thai CS career path (e.g., Data Science), targeting **1,000–2,000 postings** is realistic given the tipsena-2025 benchmark of ~4,900 per segment across 5 broader sectors. The 200–500 estimate from the previous working answer may be sufficient for a stable top-N but is at the lower bound of what the Thai literature suggests is feasible.

## Remaining Uncertainty
No paper has studied sample size convergence for skill distributions at the career path level in a small-to-medium labour market like Thailand. This is likely a genuine research gap. We should design our Phase 4 evaluation to include a convergence analysis (plot skill distribution stability vs. posting count) to answer this empirically and contribute it as a methodological finding. Contact tipsena-2025 authors (Khon Kaen University) to ask about their platform list and whether data can be shared.
