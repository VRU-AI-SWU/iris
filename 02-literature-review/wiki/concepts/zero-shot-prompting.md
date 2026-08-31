---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](zero-shot-prompting.th.md)

## Definition
**Zero-shot prompting** asks a language model to perform a task from an instruction alone,
with no examples and no retrieved context. It is the cheapest way to apply an LLM to a new
task and, across this corpus, consistently the weakest.

Measured results where a controlled comparison exists:

| Task | Zero-shot | Best alternative |
|---|---|---|
| Bloom's level classification, 6-way ([[kumar-2025-bloom-taxonomy-classification]]) | **0.72–0.73** | **94%** — SVM with augmentation |
| Course→skill extraction ([[xu-2025-llm-curricular-analytics]]) | baseline | RAG grounded in a skill base |
| Competency tagging ([[le-2026-competency-tagging-evidence]]) | outperformed | constrained, evidence-producing selection |

The pattern is uniform: whenever a paper compares zero-shot against a grounded,
constrained, or supervised alternative on the same data, zero-shot loses.

## Papers That Discuss This
- [[kumar-2025-bloom-taxonomy-classification]] — the sharpest measurement: 0.72–0.73 for
  zero-shot LLMs against 94% for SVM with augmentation on the same 600 learning outcomes
- [[xu-2025-llm-curricular-analytics]] — RAG beats zero-shot for course→skill extraction,
  especially on brief or abstract course descriptions
- [[le-2026-competency-tagging-evidence]] — the constrained pipeline outperforms zero-shot
  and few-shot LLM variants
- [[arslan-2026-turkish-skill-extraction]] — the best configuration uses *dynamic*
  few-shot, not zero-shot

## Related Concepts
[[few-shot-prompting]] · [[rag-skill-extraction]] · [[llm-skill-extraction]] ·
[[skill-entity-linking]]

## Relevance to Iris
**Iris's original design used zero-shot extraction, and that decision is reversed.**

The Phase 3 proposal chose it explicitly and reluctantly, recording that RAG was validated
as superior by [[xu-2025-llm-curricular-analytics]] but "requires a retrieval corpus not
yet available". [[thailand-skill-mapping]] supplies that corpus — 4,376 skill definitions
and 6,058 level criteria — so the constraint that forced the choice is gone. See
[[rag-skill-extraction]].

Zero-shot survives only as an **ablation baseline** in Sprint 4, to quantify what
retrieval grounding buys on Thai TQF text specifically. Reporting that delta is worth the
cost: it is the local evidence for a design decision currently justified by other people's
data on other languages.

The Bloom result is the one that changed the design rather than confirming it. It measures
zero-shot LLM classification of learning outcomes — precisely what level inference would
have been if implemented naively — and finds it 20+ points behind a classical verb-feature
classifier. Iris therefore derives level from declared document signals, with a non-LLM
baseline in the ablation. See [[q-level-inference]].
