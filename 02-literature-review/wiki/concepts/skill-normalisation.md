---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](skill-normalisation.th.md)

## Definition
**Skill normalisation** maps the many surface forms a skill takes in text onto one
canonical representation: `SQL`, `ภาษาเอสคิวแอล`, `Structured Query Language` and
`relational querying` become one entry.

It is the step that makes [[skill-extraction]] output comparable, and the step that
[[skill-entity-linking]] makes unnecessary — linking outputs canonical identifiers
directly, so there is nothing left to normalise.

Approaches: string matching and alias tables; embedding similarity; and full entity
linking against a [[skill-taxonomy]]. [[senger-2024-dl-skill-extraction-survey]] records
terminology inconsistency as a recognised, unsolved problem across the field, arising
precisely where this step is done ad hoc or skipped.

## Papers That Discuss This
- [[senger-2024-dl-skill-extraction-survey]] — terminology inconsistency across the
  literature; ESCO-linked approaches dominate because they sidestep it
- [[kavargyris-2025-escox-skill-extraction]] — normalisation via ESCO embeddings
- [[zhang-2024-job-market-entity-linking]] — normalisation as entity linking; the
  measured difficulty (Acc@1 23.55%)
- [[dong-2023-out-of-kb-mention-discovery]] — **synonym enhancement** strengthens
  canonical entries and reduces false NIL predictions

## Related Concepts
[[skill-entity-linking]] · [[skill-extraction]] · [[skill-taxonomy]] ·
[[nil-entity-linking]] · [[sentence-embedding]]

## Relevance to Iris
Normalisation is not a separate stage in Iris — it is what linking *is*. Adjudication
returns a national skill ID, so canonical form is guaranteed by construction rather than
recovered afterwards. This is the main practical benefit of the pivot away from
[[skill-extraction]].

The concept survives in one component. Candidate retrieval must match a Thai course
description against skills that may be written in Thai, English, or a transliteration, so
Iris uses all three surface forms the standard supplies per skill — Thai title, English
title, Thai definition. That is exactly the **synonym enhancement**
[[dong-2023-out-of-kb-mention-discovery]] had to construct, available here at no cost.

Lexical matching remains necessary alongside dense similarity for the `tools` type —
`Docker`, `.NET Core`, `Apache Spark` — where the Thai and English forms are often the
same token and embedding similarity is a poor discriminator between near-identical
product names.
