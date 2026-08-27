---
type: concept
---

## Definition
**Skill entity linking** is the task of mapping a span of free text to an entry in a
fixed, controlled skill vocabulary. It differs from *skill extraction*, which produces
open-vocabulary surface strings:

| | Skill extraction | Skill entity linking |
|---|---|---|
| Output | arbitrary strings | IDs in a fixed vocabulary |
| Evaluation | needs normalisation before it can be scored | precision/recall directly computable |
| Failure mode | vocabulary drift and near-duplicates | missed links, spurious links, wrong sense |
| Consistency | varies run to run | identical given the same vocabulary |

The standard modern approach is retrieve-then-adjudicate: generate candidates from the
vocabulary (dense embeddings, lexical matching, or both), then have a model decide which
candidates genuinely apply — a constrained selection task rather than open generation.

## Papers That Discuss This
- [[kavargyris-2025-escox-skill-extraction]] — LLM + ESCO-embedding pipeline; the closest
  published analogue to what Iris does, against ESCO instead of the Thai standard
- [[senger-2024-dl-skill-extraction-survey]] — surveys the field; ESCO-linked approaches
  dominate, and terminology inconsistency in open extraction is a recognised problem
- [[luyen-2025-skill-decomposition-ontology]] — LLM decomposition aligned to expert
  ontologies; few-shot prompting closes the granularity gap between text and taxonomy
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill base beats zero-shot for
  course→skill extraction, and copes with brief or abstract course descriptions
- [[dixon-2023-occupational-models-42m]] — a bounded vocabulary (775 skills) is sufficient
  at national scale, supporting the viability of a fixed-vocabulary approach

## Related Concepts
[[thailand-skill-mapping]] · [[rag-skill-extraction]] · [[proficiency-levels]] · [[esco-ontology]]

## Relevance to Iris
This is now the **core research task**. The pivot converted Iris's central problem from
"extract skills and cluster them into a vocabulary" into "link Thai TQF course
descriptions to the 4,376-entry national vocabulary" — which is better defined, directly
evaluable against expert annotation, and reproducible.

It also retroactively resolves a Phase 3 constraint. The earlier design chose zero-shot
extraction because RAG "requires a retrieval corpus not yet available". The standard's
4,376 skill definitions and 6,058 level criteria *are* that corpus, so the approach
xu-2025 found superior is now available.
