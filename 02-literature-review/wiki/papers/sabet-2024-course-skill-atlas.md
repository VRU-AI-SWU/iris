---
type: paper
authors: Alireza Javadian Sabet, Sarah H. Bana, Renzhe Yu, Morgan R. Frank
year: 2024
title: "Course-Skill Atlas: A national longitudinal dataset of skills taught in U.S. higher education curricula"
venue: Nature Scientific Data; arXiv:2404.13163
doi: 10.1038/s41597-024-03931-8
relevance: high
questions: [q-skill-taxonomy, q-gap-direction, q-temporal-drift]
---

## Research Question
Which skills are being taught in U.S. higher education, and how does curriculum skill coverage align with — and drift from — evolving labour market demands?

## Limitations of Existing Methods
Occupational skill frameworks (O*NET Detailed Workplace Activities) are well-established, but no comparable large-scale dataset exists for what skills are actually taught in courses. Programme-level curriculum analysis has relied on small-sample, manual methods that cannot scale or track change over time.

## Contribution
A longitudinal dataset of 3M+ course syllabi from ~3,000 U.S. institutions aligned to DOL Detailed Workplace Activities using NLP. Enables institutional- and major-level skill profiles and temporal drift measurement across years.

## Proposed Method
NLP alignment of course syllabus text to O*NET DWA descriptions; aggregation to institution and academic major level; KL divergence to quantify temporal drift between curriculum skill distributions and evolving labour market demand.

## Key Findings
Labour force skill distributions become increasingly dissimilar to older course syllabi over time, confirming rapid skill demand evolution. Significant variation in skill coverage exists across institutions and academic majors. KL divergence successfully captures curriculum-market drift direction and magnitude.

## Limitations of This Paper
U.S.-centric — uses O*NET/DOL taxonomy which does not map to Thai TQF context. English-language syllabi only. Relies on a fixed taxonomy (DWAs) rather than emergent vocabulary, which may miss domain-specific or emerging skills not yet in O*NET.

## Concepts
[[curriculum-analytics]] · [[onet-taxonomy]] · [[kl-divergence]] · [[skill-gap-quantification]] · [[temporal-drift]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-gap-direction]] · [[q-temporal-drift]]

## Notes for Iris
The most directly comparable study to Iris at scale. Key takeaway: KL divergence is a validated method for curriculum-market gap and temporal drift — supports our hybrid gap metric approach. The fixed O*NET taxonomy contrasts with our emergent vocabulary decision; the paper's limitation of missing emerging skills is exactly why we chose bottom-up extraction. Thai TQF context requires Thai NLP, which is outside this paper's scope.
