---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](skill-taxonomy.th.md)

## Definition
A **skill taxonomy** is a curated, enumerated set of skills with stable identifiers,
against which text can be classified or linked. Distinguished from a
[[skill-ontology]], which additionally encodes relations between entries
(broader/narrower, prerequisite, part-of).

The major reference taxonomies:

| Taxonomy | Size | Languages | Note |
|---|---|---|---|
| [[esco-ontology]] (EU) | ~13,890 skills | 27, **no Thai** | Dominant in the literature |
| [[onet-taxonomy]] (US) | ~2,000 DWAs | English | Work-activity oriented |
| Lightcast | 34,000+ | English-led | Commercial, monthly updates |
| [[thailand-skill-mapping]] (สป.อว.) | **4,376** | **Thai + English** | Three graded levels per skill |

Size is not the interesting variable. [[dixon-2023-occupational-models-42m]] shows a
bounded **775-skill** vocabulary suffices to model occupations at US national scale from
42 million postings — evidence that a curated taxonomy in the low thousands is adequate,
and that coverage matters more than count.

The standing trade-off: a fixed taxonomy buys comparability and reproducibility, and pays
in coverage of emerging and domain-specific skills — a limitation
[[senger-2024-dl-skill-extraction-survey]] records as unsolved, and which
[[nil-entity-linking]] is the technical response to.

## Papers That Discuss This
- [[dixon-2023-occupational-models-42m]] — 775 skills suffice at national scale
- [[kavargyris-2025-escox-skill-extraction]] — ESCOX links text to ESCO with LLM +
  taxonomy embeddings
- [[ahadi-2022-skills-taught-vs-sought]] — course × occupation heatmaps over a fixed
  taxonomy, with RCA weighting
- [[chaiaroon-2025-thai-digital-workforce-matching]] — 20-category Thai digital *job*
  taxonomy (roles, not skills)
- [[fettach-2025-skill-demand-temporal-kg]] · [[seif-2024-dynamic-jobs-skills-kg]] —
  taxonomies embedded in temporal knowledge graphs
- [[zhang-2024-job-market-entity-linking]] — the cost of taxonomy size: Acc@1 23.55%
  against 13,890 ESCO skills
- [[sabet-2024-course-skill-atlas]] — O*NET DWAs applied to 3M+ US syllabi

## Related Concepts
[[thailand-skill-mapping]] · [[esco-ontology]] · [[onet-taxonomy]] · [[skill-ontology]] ·
[[skill-normalisation]] · [[nil-entity-linking]] · [[skill-entity-linking]]

## Relevance to Iris
Iris links to **Thailand Skill Mapping**, pinned by dated snapshot. See
[[q-skill-taxonomy]] for the decision and [[q-thai-ontology]] for why the earlier answer
("no suitable Thai taxonomy exists") reversed.

Two properties make it the right target beyond mere availability. It is **native Thai**,
so no translation step distorts the labels — the failure mode
[[arslan-2026-turkish-skill-extraction]] measured when forced to borrow ESCO. And it
grades every skill into three levels with written criteria ([[proficiency-levels]]),
which neither ESCO nor O*NET offers and which is what makes Iris's level-aware analysis
possible at all.

At 4,376 entries it sits comfortably above Dixon et al.'s 775-skill sufficiency threshold
and well below ESCO's 13,890 — a smaller candidate space than the setting where Acc@1 of
23.55% was measured, which is one reason to expect better.
