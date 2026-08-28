---
type: concept
---

## Definition
**LLM-based skill extraction** uses a general-purpose language model, prompted rather than
trained, to identify skills in text. It displaced supervised
[[deep-learning-ner]] as the default approach because it needs no labelled data for the
target domain — decisive for languages and domains where none exists.

Three modes, in increasing reliability:

| Mode | Description | Evidence |
|---|---|---|
| [[zero-shot-prompting]] | Ask for skills, no examples | Baseline; weakest |
| [[few-shot-prompting]] | Supply examples, ideally retrieved per input | [[luyen-2025-skill-decomposition-ontology]]; dynamic few-shot is the best Turkish configuration |
| [[rag-skill-extraction]] | Ground the prompt in a retrieved skill base | [[xu-2025-llm-curricular-analytics]]: beats zero-shot |

The trajectory across the corpus is consistent: **the more the model is constrained by
retrieved, authoritative context, the better it performs.** In its strongest form the task
stops being extraction at all and becomes selection —
[[skill-entity-linking]] — which is what [[le-2026-competency-tagging-evidence]] calls a
"constrained, evidence-producing tagger".

Fine-tuning is the alternative branch ([[herandi-2024-skill-llm]]), requiring labelled
data that low-resource settings lack.

## Papers That Discuss This
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill base beats zero-shot for
  course→skill work; brief course descriptions are the hard case
- [[luyen-2025-skill-decomposition-ontology]] — few-shot prompting aligns LLM output to
  expert ontology granularity
- [[arslan-2026-turkish-skill-extraction]] — LLM pipeline beats supervised sequence
  labelling in a low-resource language; **native-language beats translation**; 0.56
  end-to-end
- [[le-2026-competency-tagging-evidence]] — constrained selection with evidence spans
  beats unconstrained prompting *and* supervised classifiers
- [[kumar-2025-bloom-taxonomy-classification]] — ⚠️ counterweight: zero-shot LLMs reach
  0.72–0.73 on Bloom classification against 94% for SVM with augmentation
- [[saroglou-2025-esco-eqf-linking]] — ⚠️ supervised approaches beat decoder-only models
  on their ranking step
- [[herandi-2024-skill-llm]] — the fine-tuning branch

## Related Concepts
[[rag-skill-extraction]] · [[zero-shot-prompting]] · [[few-shot-prompting]] ·
[[skill-entity-linking]] · [[skill-extraction]] · [[deep-learning-ner]]

## Relevance to Iris
Iris uses an LLM in exactly one place — **adjudication**: given a course description and
~30 retrieved candidate skills with their official definitions, decide which apply and
return the evidence span. Everything else is deterministic.

That is the most constrained point on the scale above, and deliberately so. The
[[xu-2025-llm-curricular-analytics]] finding drove it; the earlier design accepted
zero-shot only because no retrieval corpus existed, and the standard's 4,376 definitions
supply one. It also allows a smaller local model than open generation would, since
selecting among candidates is easier than composing an answer.

The two counterweights are load-bearing and are why the Sprint 4 ablation includes
non-LLM baselines. [[kumar-2025-bloom-taxonomy-classification]] shows a classical
classifier beating zero-shot LLMs by 20+ points on level classification — so level is
inferred from declared document signals, not asked of the model.
[[saroglou-2025-esco-eqf-linking]] found supervised ranking beating decoder-only models —
so a supervised ranker is measured against LLM adjudication rather than assumed inferior.
