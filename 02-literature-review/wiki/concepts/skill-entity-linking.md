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
- [[zhang-2024-job-market-entity-linking]] — ⭐ the first span-level skill EL study;
  **BLINK Acc@1 23.55%, Acc@32 48.98%** against ESCO's 13,890 skills
- [[arslan-2026-turkish-skill-extraction]] — the same architecture in a low-resource,
  morphologically complex language; **0.56 end-to-end**, and native-language extraction
  beats translate-to-English
- [[saroglou-2025-esco-eqf-linking]] — Sentence Linking vs Entity Linking; EL Accuracy@1
  **0.2881**, and sentence context helps
- [[le-2026-competency-tagging-evidence]] — LLM as a *constrained, evidence-producing
  tagger*; micro-F1 0.57, MRR 0.82
- [[dong-2023-out-of-kb-mention-discovery]] — explicit NIL modelling for mentions with no
  vocabulary entry
- [[herandi-2024-skill-llm]] — the fine-tuning branch; extraction only, no linking

## Related Concepts
[[thailand-skill-mapping]] · [[nil-entity-linking]] · [[rag-skill-extraction]] · [[proficiency-levels]] · [[esco-ontology]]

## Relevance to Iris
This is now the **core research task**. The pivot converted Iris's central problem from
"extract skills and cluster them into a vocabulary" into "link Thai TQF course
descriptions to the 4,376-entry national vocabulary" — which is better defined, directly
evaluable against expert annotation, and reproducible.

It also retroactively resolves a Phase 3 constraint. The earlier design chose zero-shot
extraction because RAG "requires a retrieval corpus not yet available". The standard's
4,376 skill definitions and 6,058 level criteria *are* that corpus, so the approach
xu-2025 found superior is now available.

**Expected performance, from three independent studies.** Strict top-1 accuracy for
linking against a large occupational taxonomy sits near **0.23–0.29**
([[zhang-2024-job-market-entity-linking]] 23.55%, [[saroglou-2025-esco-eqf-linking]]
0.2881), and end-to-end pipeline scores near **0.56** ([[arslan-2026-turkish-skill-extraction]],
[[le-2026-competency-tagging-evidence]] micro-F1 0.57). Every one of these also reports
that *ranking* is far better than *selection* — Acc@32 roughly double Acc@1, MRR 0.82
against F1 0.57.

Two design conclusions follow, and both are already in Iris's plan: retrieve generously
and adjudicate, and **put a human review screen between the linker and any published
claim.** At these accuracy levels an unreviewed mapping is not evidence.
