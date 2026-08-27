---
type: question
owner: Researcher + Domain Expert
status: answered
---

> ⚠️ **Answer replaced 2026-08-27.** The previous working answer — emergent vocabulary at
> extraction time, post-hoc ESCO mapping — is superseded by the adoption of the national
> standard. See [[q-thai-ontology]] for why.

## Question
What skill taxonomy or ontology should Iris use?

## Why This Matters for Iris
The taxonomy determines how skills are named, grouped, and compared. It also determines
whether results are reproducible and whether they can be compared with anyone else's.

## Papers Addressing This
- [[thailand-skill-mapping]] — ⭐ the adopted vocabulary: 4,376 Thai skills with
  definitions and three graded levels, official national standing
- [[dixon-2023-occupational-models-42m]] — a bounded 775-skill vocabulary suffices at US
  national scale; supports fixed-vocabulary viability, and 4,376 is comfortably above it
- [[kavargyris-2025-escox-skill-extraction]] — LLM + taxonomy-embedding linking pipeline
  against ESCO; the direct methodological template
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill base beats zero-shot for
  course→skill work; the standard's definitions supply that base
- [[senger-2024-dl-skill-extraction-survey]] — fixed taxonomies miss emerging and
  domain-specific skills; the cost being accepted here, tracked in [[q-out-of-vocabulary]]
- [[sabet-2024-course-skill-atlas]] — fixed O*NET DWAs applied to syllabi at national
  scale; the closest precedent for the curriculum side
- [[luyen-2025-skill-decomposition-ontology]] — few-shot decomposition to close
  text↔taxonomy granularity gaps
- [[vo-2022-nlp-curriculum-learning-path]] — domain-tuned NER for CS/IT curriculum text;
  an alternative candidate-generation route

## Current Working Answer
status: **answered — the national standard, pinned by snapshot**

Iris adopts **Thailand Skill Mapping** as its controlled vocabulary. The task becomes
[[skill-entity-linking]] rather than open extraction plus clustering.

What this buys:

| | Emergent vocabulary | National standard |
|---|---|---|
| Stability across runs | varies | fixed |
| Ground truth for evaluation | none | annotation is well defined |
| Comparability with other work | none | anyone using the standard |
| Reproducibility | poor | pinned snapshot |
| Proficiency grading | absent | three levels with criteria |
| Official standing | none | สป.อว. reference data |

The trade — coverage of skills outside the vocabulary — is accepted knowingly and
tracked in [[q-out-of-vocabulary]]. ESCO mapping is dropped: it was a proxy for the
comparability the national standard now provides directly, and translating Thai
curriculum content into a European English taxonomy would add noise for no gain.

## Remaining Uncertainty
- Coverage of academic CS content — [[q-out-of-vocabulary]]
- Retrieval depth `k` for candidate generation, and dense/lexical balance
- Snapshot refresh policy as the standard evolves
