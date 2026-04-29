---
type: question
owner: Data Scientist + Product Manager
status: open
---

## Question
Should the skill gap be symmetric or directional? (Programme A lacks skill X vs Programme B has excess of skill Y)

## Why This Matters for Iris
A symmetric gap score treats both directions equally; a directional gap distinguishes deficit (missing required skills) from surplus (teaching skills not demanded). Academic administrators care more about deficits; curriculum designers may also care about surpluses.

## Initial Hypothesis
Hybrid approach: use set-based directional gap for human-readable reports (clearly shows what is missing vs excess), and cosine distance or KL divergence for aggregate scoring. KL divergence is naturally asymmetric and may be the right single-number summary.

## Papers Addressing This
- [[sabet-2024-course-skill-atlas]] — uses KL divergence to measure gap and temporal drift between curriculum and labour market skill distributions
- [[senger-2024-dl-skill-extraction-survey]] — gap framing is directional in the field: job market demand is the reference distribution, programme supply is compared against it

## Current Working Answer
status: partial

KL divergence is the validated aggregate metric — it is naturally asymmetric (market||programme ≠ programme||market), which is exactly right for our use case where the market is the reference. Set-based gap (what skills are in demand but absent from the programme) remains the most interpretable output for non-technical stakeholders. Hybrid approach stands: set-based for report, KL divergence for aggregate score.

## Remaining Uncertainty
How to handle skills that partially overlap (e.g. "machine learning" in programme vs "deep learning" in market)? Pure set-based gap treats these as a miss; cosine similarity in embedding space would capture partial alignment. Need a paper or experiment to determine whether embedding-based partial matching improves actionability of the output.
