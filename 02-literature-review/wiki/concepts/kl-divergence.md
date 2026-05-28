---
type: concept
---

## Definition
Kullback-Leibler (KL) divergence measures the asymmetric difference between two probability distributions P and Q. KL(P||Q) quantifies how much information is lost when Q is used to approximate P. In skill gap analysis, it measures how much the programme skill distribution diverges from the market demand distribution — and can also measure temporal drift between skill snapshots across time.

## Papers That Discuss This
*(populated via Obsidian backlinks)*

## Related Concepts
[[cosine-similarity]] · [[skill-gap-quantification]] · [[temporal-drift]]

## Relevance to Iris
KL divergence is validated in the literature (Course-Skill Atlas) for both curriculum-market gap and temporal drift measurement. It is naturally asymmetric — KL(market||programme) ≠ KL(programme||market) — which aligns with our need for a directional gap metric. Likely the best single-number aggregate score for Q10.
