---
type: concept
---

## Definition
**NIL entity linking** (also *out-of-KB mention discovery*) is the sub-problem of entity
linking concerned with mentions that have **no correct entry** in the target knowledge
base. It splits into two tasks:

- **NIL detection** — recognising that a mention is unlinkable
- **NIL disambiguation** — deciding whether several unlinkable mentions refer to the same
  absent entity

Without it, a linker forced to always return its best candidate will confidently assign a
wrong entity to every mention the vocabulary does not cover — a failure that is silent,
because the output is well-formed.

The standard weak approach is a **similarity threshold**: link if the top candidate scores
above a cut-off, otherwise declare NIL. [[dong-2023-out-of-kb-mention-discovery]] shows
that modelling NIL as an **explicit prediction target** beats threshold and feature-based
methods across five datasets and three knowledge bases (UMLS, SNOMED CT, WikiData).

## Papers That Discuss This
- [[dong-2023-out-of-kb-mention-discovery]] — BLINKout: explicit NIL entity representation
  and classification, synonym enhancement, and KB Pruning/Versioning to generate out-of-KB
  evaluation data without new annotation
- [[senger-2024-dl-skill-extraction-survey]] — fixed taxonomies consistently miss emerging
  and domain-specific skills; a recognised, unsolved limitation of the field
- [[zhang-2024-job-market-entity-linking]] — evaluates against a single gold ESCO title per
  mention, which conflates "no valid link" with "not the one gold link"
- [[le-2026-competency-tagging-evidence]] — graph constraints suppress structurally
  inconsistent tags, an indirect route to the same goal

## Related Concepts
[[skill-entity-linking]] · [[thailand-skill-mapping]] · [[esco-ontology]]

## Relevance to Iris
Iris adopts a **fixed** 4,376-entry vocabulary derived from labour-market data, then
applies it to **academic curricula**. Those distributions differ: a degree programme
teaches theoretical foundations, research method, mathematics, and ethics that no job
advertisement describes. Every such course topic is a NIL case.

Getting this wrong is the most damaging failure mode available to the project. If the
linker maps *"ทฤษฎีการคำนวณ"* (theory of computation) to the nearest available
labour-market skill, the resulting programme profile is both wrong and confident — and a
curriculum committee will spot it immediately and stop trusting the whole report.

The design consequence is recorded in [[q-out-of-vocabulary]]: out-of-vocabulary is an
**explicit decision with its own output channel**, never a threshold and never a
nearest-neighbour fallback. The accumulated residue across programmes is also a
deliverable — a coverage report back to สป.อว./KMITL on what the standard does not name.
