---
type: paper
authors: Ahadi A., Kitto K., Rizoiu M.A., Musial K.
year: 2022
title: "Skills Taught vs Skills Sought: Using Skills Analytics to Identify the Gaps between Curriculum and Job Markets"
venue: 15th International Conference on Educational Data Mining (EDM 2022), poster
doi:
relevance: high
questions: [q-visualisation, q-skill-gap-direction, q-skill-taxonomy]
---

## Research Question
How can skills analytics identify and visualise gaps between skills taught in university curricula and skills sought by the job market, at the course-to-occupation level?

## Limitations of Existing Methods
Raw skill frequency counts are dominated by generic skills (creativity, communication, teamwork) that appear everywhere and mask meaningful discipline-specific gaps. Simple set-difference gap measures (which skills are missing) do not capture the relative importance of each skill in context. Existing gap reports tend to be narrative, not machine-readable or systematically visualised.

## Contribution
Application of **Revealed Comparative Advantage (RCA)** — a labour economics metric — to weight skill importance by contextual specialisation. RCA suppresses generic skills and elevates domain-specific ones. Heatmap visualisation with hierarchical clustering to show course-to-occupation alignment at a glance.

## Proposed Method
- **Curriculum data**: 2,747 university subjects parsed via EMSI/Burning Glass Technology API → 138,455 skill tags
- **Market data**: 144,000 job advertisements covering 612 occupations → 1.4M occupational skill tags
- **Skill taxonomy**: 33,000+ skills taxonomy (EMSI/Burning Glass)
- **Key metric**: Revealed Comparative Advantage (RCA) — skill frequency in occupation / skill frequency across all occupations; skills with RCA > 1 are comparatively important for that occupation
- **Visualisation**: Heatmap — rows = courses, columns = occupation groups; cell value = RCA-weighted similarity score; hierarchical clustering applied to both axes

## Key Findings
- RCA successfully downweights generic skills (creativity, teamwork) that appear in every course and occupation, elevating specialised technical skills that are genuinely discriminating
- IT courses show strong alignment with IT occupations but poor alignment with pharmacy roles — sanity check confirms method validity
- Unexpected finding: forensic science curriculum had **low skill gap** with data scientist roles — alternative career pathway surfaced that programme designers were unaware of
- Heatmap with hierarchical clustering is effective for conveying multi-course × multi-occupation gap landscape to academic administrators in a single view
- Single-year job ad dataset (2020, COVID-disrupted) limited RCA accuracy — temporal snapshot limitations acknowledged

## Limitations of This Paper
Poster-length — full experimental detail not provided. Relies on EMSI commercial API for skill tagging (not replicable without licence). 2020 data only — COVID year; RCA values may not reflect normal market conditions. Skill taxonomy (33K skills) is English-language; not applicable to Thai context directly.

## Concepts
[[skill-gap-quantification]] · [[curriculum-analytics]] · [[skill-taxonomy]]

## Questions Addressed
[[q-visualisation]] · [[q-skill-gap-direction]]

## Notes for Iris
**Two direct contributions to Iris design:**
1. **RCA as an alternative to raw frequency for skill weighting**: RCA is a strong candidate for our skill importance weighting in gap quantification. Instead of just counting how often a skill appears in job postings, RCA measures how comparatively specialised that skill is for the target career path vs. the market at large. This would downweight "Python" (appears everywhere) and elevate career-path-specific skills. Our Data Scientist should evaluate RCA alongside TF-IDF and KL divergence as weighting options.
2. **Heatmap as primary visualisation**: The heatmap (courses × occupations) is validated as effective for non-technical academic stakeholders. For Iris, a similar heatmap (courses × required skills, with gap magnitude in cells) would let curriculum designers see at a glance which courses address which skill gaps. The surprising-pathway finding (forensic science → data science) also shows that heatmaps can surface **opportunity insights** not just deficit signals — a strong product angle for Iris.
