---
type: concept
---

## Definition
Skill gap quantification is the process of measuring the difference between a supply-side skill distribution (what a programme teaches) and a demand-side skill distribution (what the market requires). Methods range from simple set difference (missing skills) to statistical measures like cosine similarity (overall alignment), KL divergence (asymmetric distributional difference), and chi-square tests (distributional equality testing).

## Papers That Discuss This
*(populated via Obsidian backlinks)*

## Related Concepts
[[kl-divergence]] · [[cosine-similarity]] · [[curriculum-analytics]] · [[temporal-drift]]

## Relevance to Iris
The core output of Iris's gap analysis engine. The literature supports a hybrid approach: set-based gap for human-readable reports (what's missing vs. what's surplus), KL divergence for the aggregate directional score, cosine similarity as an interpretable overall alignment metric. All three have been validated in the skill gap literature.
