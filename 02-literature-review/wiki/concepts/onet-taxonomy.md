---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](onet-taxonomy.th.md)

## Definition
**O*NET** (Occupational Information Network) is the US Department of Labor's occupational
database. Its unit of analysis is the **Detailed Work Activity (DWA)** — around 2,000
statements of what people *do* in a job ("analyze data to identify trends") — rather than
a skill someone *has*.

That framing distinguishes it from [[esco-ontology]]: DWAs describe tasks, ESCO describes
skills and competences. For curriculum work the difference matters, because a syllabus
states what a student will be able to do, which maps more naturally onto activities than
onto capability labels.

[[sabet-2024-course-skill-atlas]] is the largest application in this corpus: 3M+ US
syllabi mapped to O*NET DWAs, producing a national longitudinal Course-Skill Atlas.

## Papers That Discuss This
- [[sabet-2024-course-skill-atlas]] — O*NET DWAs as the fixed taxonomy for a
  national-scale syllabus study; also the source of the KL-divergence approach to
  curriculum↔market drift
- [[dixon-2023-occupational-models-42m]] — an alternative bounded vocabulary built from
  postings rather than expert curation

## Related Concepts
[[skill-taxonomy]] · [[esco-ontology]] · [[tpqi-framework]] · [[thailand-skill-mapping]] ·
[[curriculum-analytics]]

## Relevance to Iris
**Considered and not used.** O*NET is English-only and describes the US labour market; a
Thai TQF course description would have to be translated into it, and
[[arslan-2026-turkish-skill-extraction]] measured that translation-first extraction loses
to native-language extraction.

It matters as the **methodological precedent** rather than as a target.
[[sabet-2024-course-skill-atlas]] is the closest prior work to Iris in shape — a fixed
national taxonomy applied at scale to curriculum documents — and it is the source of two
things Iris carries forward and one it corrected. Carried forward: the course × skill
matrix as the core data structure, and the idea of measuring curriculum-to-market drift as
a distributional comparison. Corrected: Sabet et al. compute KL divergence over syllabus-
derived *distributions*, whereas the Thai standard publishes **prevalence**, which is not
a distribution — see [[q-prevalence-metrics]].

The other instructive contrast is level. O*NET DWAs, like ESCO skills, are binary
occupancy in Sabet et al.'s matrix. The Thai standard's graded criteria are what let Iris
ask a question O*NET-based work cannot ([[proficiency-levels]]).
