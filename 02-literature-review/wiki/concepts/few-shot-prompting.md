---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](few-shot-prompting.th.md)

## Definition
**Few-shot prompting** supplies worked examples in the prompt. **Dynamic few-shot**
selects those examples per input, retrieving the nearest labelled cases rather than using
a fixed set — which makes it a form of retrieval augmentation over examples instead of
over knowledge.

Its practical appeal in low-resource settings is that it needs tens of labelled examples
where supervised training needs thousands, and it conveys output *format* and *granularity*
that an instruction alone conveys poorly. [[luyen-2025-skill-decomposition-ontology]] uses
it specifically to close the granularity gap between free text and an expert ontology's
level of description.

[[arslan-2026-turkish-skill-extraction]] found dynamic few-shot the best configuration for
skill identification in a morphologically complex, low-resource language — reaching 0.56
end-to-end and beating supervised sequence labelling.

## Papers That Discuss This
- [[arslan-2026-turkish-skill-extraction]] — Claude Sonnet 3.7 with **dynamic** few-shot
  prompting is the best-performing skill-identification configuration
- [[luyen-2025-skill-decomposition-ontology]] — few-shot prompting improves alignment to
  expert-ontology granularity
- [[le-2026-competency-tagging-evidence]] — the constrained pipeline outperforms both
  zero-shot and few-shot LLM variants, so few-shot alone is not the ceiling
- [[xu-2025-llm-curricular-analytics]] — grounding in a retrieved skill base is the
  stronger intervention for course→skill work

## Related Concepts
[[zero-shot-prompting]] · [[rag-skill-extraction]] · [[llm-skill-extraction]] ·
[[skill-entity-linking]]

## Relevance to Iris
Available and not yet committed to. Iris's adjudication is a *selection* task —
"which of these 30 candidate skills does this course develop, at what level?" — where
retrieved candidates with official definitions already supply most of the grounding that
few-shot examples would otherwise provide.

The place it plausibly earns its cost is **calibration rather than knowledge**: showing
the model two or three adjudicated Thai courses teaches how strict to be about implicit
skills and how the three proficiency levels are applied in practice, which the criteria
text alone underdetermines. That is a judgement Iris's annotators will make in Sprint 4,
and the annotated set becomes the example pool for free.

Two cautions. [[le-2026-competency-tagging-evidence]] found their constrained pipeline
beating few-shot variants, so examples are not a substitute for constraining the output
space. And dynamic few-shot needs a labelled pool to retrieve from, which will not exist
before the Sprint 4 gate — so it is a **post-gate improvement**, evaluated on the held-out
split, not part of the first working pipeline.
