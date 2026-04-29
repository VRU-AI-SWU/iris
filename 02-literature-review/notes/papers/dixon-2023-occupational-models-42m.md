---
type: paper
authors: Dixon N., Goggins M., Ho E., Howison M., Long J., Northcott E., Shen K., Yeats C.
year: 2023
title: "Occupational models from 42 million unstructured job postings"
venue: Patterns 4 (2023) 100757, Cell Press / Elsevier
doi: 10.1016/j.patter.2023.100757
relevance: high
questions: [q-skill-taxonomy, q-sample-size, q-job-posting-sources]
---

## Research Question
How can 42 million unstructured US job postings be structured into occupational codes and skill associations, and how can these models be made openly available for research reuse?

## Limitations of Existing Methods
Existing SOC-code assignment tools (NIOCCS, SOCcer, O*NET Code Connector) are either web-only, require registration, are not FAIR-compliant, or do not expose model parameters. No openly available, offline-capable probabilistic model for occupations-to-skills associations existed at large scale.

## Contribution
Open data resource and `sockit` Python package with empirical probability models for: (1) job title → SOC code, (2) job description → skill keywords, (3) skill → occupation association. Curated 775-skill vocabulary from 42M postings. Deployed in production by US state labor departments for career recommendation.

## Proposed Method
- **Data**: 42,298,617 NLx Research Hub records (2019: 13.2M; 2021: 29.1M); US national job postings from 300,000 employers
- **Job title normalisation**: Prefix-tree (trie) based normalisation to reduce variant title forms; identified 849,284 distinct normalised titles from 3M+ raw variants
- **Skill extraction**: Curated 775-skill list (keyword matching via substring/prefix trees); computed P(skill | occupation) for each skill across all SOC occupation codes
- **Occupation coding**: SOCcer-derived codes as initial labels; refined via probabilistic model
- **Output**: `sockit` package (open-source, PyPI) with offline occupation assignment and skill parsing from job descriptions and resumes

## Key Findings
- Skill probabilities are consistent with the hierarchy of SOC occupational codes — validates the approach's coherence
- Job posting counts are an **imperfect proxy** for actual job openings (confirmed by comparison with BLS survey data) — posting volume inflates demand for some occupations
- 775-skill curated vocabulary is sufficient to describe the US occupational skill landscape at national scale
- Model deployed in career recommendation systems in 5 US states — real-world validation
- 849,284 distinct normalised job titles from 3M+ raw variants — demonstrates scale of title variation problem

## Limitations of This Paper
US-only dataset; skill vocabulary is English-only; SOC codes apply only to the US context. 775-skill list was curated, not emergent — vocabulary selection introduces bias. 2019 and 2021 snapshots only — no longitudinal analysis. Posting count ≠ job opening count (stated explicitly).

## Concepts
[[skill-taxonomy]] · [[job-posting-analysis]] · [[skill-gap-quantification]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-sample-size]] · [[q-job-posting-sources]]

## Notes for Iris
**Two high-value insights for Iris design:**
1. **Scale and vocabulary**: 775 curated skills is sufficient at national scale for the US. Our Thai context is smaller; this suggests our emergent vocabulary may converge to a smaller set (100–300 skills?). Useful for calibrating our vocabulary scope in Solution Design.
2. **Posting count caveat**: The explicit finding that posting count ≠ job opening count (from BLS comparison) should be cited when we discuss limitations of our job-posting-derived market signal. We have no equivalent survey data for Thailand to triangulate against.
3. **`sockit` methodology**: Prefix-tree substring matching for skill extraction is a computationally efficient baseline; relevant to our Data Engineer's pipeline design considerations.
4. **Open data precedent**: The FAIR-compliant open data approach validates our decision to publish Iris outputs openly.
