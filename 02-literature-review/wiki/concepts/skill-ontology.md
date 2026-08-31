---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](skill-ontology.th.md)

## Definition
A **skill ontology** is a [[skill-taxonomy]] that also encodes *relations* between
entries — broader/narrower, prerequisite, part-of, equivalence — so the structure can be
reasoned over rather than merely looked up.

The relations are what enable operations a flat list cannot support: rolling a specific
skill up to its parent for aggregation, resolving granularity mismatches between a text
mention and a taxonomy entry ([[skill-decomposition]]), and constraining predictions so a
child cannot be assigned without its parent — the mechanism
[[le-2026-competency-tagging-evidence]] uses to suppress spurious tags.

[[esco-ontology]] is the field's reference: ~13,890 skills with a hierarchy and explicit
occupation–skill links. [[tpqi-framework]] is Thailand's nearest equivalent but operates
at occupational-competency granularity, not skill granularity, and is not
machine-readable as an ontology.

## Papers That Discuss This
- [[luyen-2025-skill-decomposition-ontology]] — LLM skill decomposition aligned to expert
  ontologies; few-shot prompting closes the granularity gap between text and ontology
- [[le-2026-competency-tagging-evidence]] — graph constraints over a competency structure
  measurably reduce spurious assignments
- [[senger-2024-dl-skill-extraction-survey]] — ontology-linked approaches dominate the
  field
- [[saroglou-2025-esco-eqf-linking]] — links to ESCO *and* the EQF qualification-level
  framework

## Related Concepts
[[skill-taxonomy]] · [[esco-ontology]] · [[tpqi-framework]] · [[skill-decomposition]] ·
[[thailand-skill-mapping]] · [[skill-entity-linking]]

## Relevance to Iris
**[[thailand-skill-mapping]] is a taxonomy, not an ontology.** Its 4,376 skills are a flat
list: no parent/child links, no prerequisite relations, no equivalences. The only
structure is a three-way type (`hard-skill` / `soft-skill` / `tools`) and membership in
career and industry sets.

That has a concrete cost. The graph constraints that improved
[[le-2026-competency-tagging-evidence]] have no direct analogue here — Iris cannot
suppress a prediction because its parent was not also predicted, since there are no
parents. Nor can it aggregate `มายเอสคิวแอล` (MySQL) up into `ฐานข้อมูล` (Databases) when
reporting, because nothing records that relation.

Three substitutes are available and untested: the skill *type* field, the
industry → career → skill membership structure, and the prerequisite graph of the
curriculum itself, which is a genuine ordering Iris extracts from the มคอ.2 and which no
skill taxonomy could supply. Whether any of these constrain usefully is an open question
for Sprint 4.

Building relations over the national vocabulary is out of scope: it would be Iris's own
inference layered on national reference data, which undermines the reproducibility that
motivated adopting the standard.
