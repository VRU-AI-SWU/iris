---
type: concept
---

## Definition
**Deep-learning NER** treats skill extraction as supervised sequence labelling: tag each
token BIO-style as inside or outside a skill span, using a BiLSTM-CRF or a fine-tuned
transformer encoder. It was the field standard before prompted LLMs
([[llm-skill-extraction]]) displaced it.

Its strength is precise span boundaries and, given enough in-domain labels, high accuracy.
Its cost is exactly that requirement: thousands of manually annotated spans per language
and domain. [[senger-2024-dl-skill-extraction-survey]] surveys the resulting body of work
and documents how the annotation bottleneck shaped it.

Domain adaptation matters as much as architecture:
[[vo-2022-nlp-curriculum-learning-path]] shows CSIT-NER, a domain-specific fine-tune,
beating general BERT for CS/IT skill NER in curriculum text.

## Papers That Discuss This
- [[senger-2024-dl-skill-extraction-survey]] — the survey; sequence-labelling approaches
  and their annotation dependency
- [[vo-2022-nlp-curriculum-learning-path]] — CSIT-NER; domain-specific fine-tuning beats
  general BERT on curriculum text
- [[arslan-2026-turkish-skill-extraction]] — ⚠️ an LLM pipeline **outperformed** supervised
  sequence labelling in a low-resource language
- [[herandi-2024-skill-llm]] — fine-tuned generative LLM positioned against NER baselines
- [[kumar-2025-bloom-taxonomy-classification]] — BERT and RNNs overfitted badly on 600
  labelled sentences

## Related Concepts
[[skill-extraction]] · [[llm-skill-extraction]] · [[roberta-architecture]] ·
[[skill-entity-linking]] · [[thai-bert]]

## Relevance to Iris
**Not viable, and the reason is data rather than merit.**

No annotated Thai skill-span corpus exists. Building one to the scale supervised NER needs
would consume the project's entire annotation budget — and that budget is committed to
*evaluation*, where it produces a defensible quality claim, rather than to training data,
where it produces a model with nothing left to validate it.

[[arslan-2026-turkish-skill-extraction]] is the decisive precedent: facing the same
absence in Turkish, an LLM pipeline with retrieval and re-ranking beat supervised sequence
labelling outright. Iris follows that branch.

[[kumar-2025-bloom-taxonomy-classification]] adds the corroborating warning from the other
direction — transformers overfitting on 600 labelled sentences, in the same data regime as
Iris's ~50-course annotation set.

The concept retains one live use. [[vo-2022-nlp-curriculum-learning-path]]'s result that
domain-specific tuning helps on *curriculum text specifically* stays relevant if Iris ever
accumulates enough reviewed links — every accepted or rejected link in the review screen is
a labelled example — to train a supervised **ranker**, which
[[saroglou-2025-esco-eqf-linking]] found can beat decoder-only LLMs at that step. That is a
post-gate possibility, not a v1 plan.
