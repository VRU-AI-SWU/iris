---
type: concept
---

## Definition
**Skill extraction** is the task of identifying skill mentions in free text — job
postings, syllabi, CVs — and returning them as strings. It is the *open-vocabulary*
counterpart to [[skill-entity-linking]]: the output is whatever surface form the text
used, not an identifier in a controlled set.

The field's recurring problem is that the output is not comparable across documents or
across systems. "SQL", "ภาษาเอสคิวแอล", "Structured Query Language" and "relational
querying" are one skill wearing four surfaces, and every downstream aggregation must
first decide that they are the same — a step called [[skill-normalisation]].
[[senger-2024-dl-skill-extraction-survey]] documents this terminology inconsistency as a
recognised, unsolved problem across the literature.

Approaches, roughly in order of appearance:

| Approach | Example |
|---|---|
| Keyword / dictionary matching | [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] |
| Supervised sequence labelling ([[deep-learning-ner]]) | [[vo-2022-nlp-curriculum-learning-path]], [[senger-2024-dl-skill-extraction-survey]] |
| Fine-tuned generative LLM | [[herandi-2024-skill-llm]] |
| Prompted LLM ([[llm-skill-extraction]]) | [[xu-2025-llm-curricular-analytics]] |

## Papers That Discuss This
- [[senger-2024-dl-skill-extraction-survey]] — the field survey; ESCO-linked approaches
  dominate precisely because open extraction suffers terminology inconsistency
- [[xu-2025-llm-curricular-analytics]] — LLM extraction from course documents; RAG beats
  zero-shot, and brief descriptions are the hard case
- [[vo-2022-nlp-curriculum-learning-path]] — CSIT-NER: domain-specific BERT fine-tuning
  beats general BERT for CS/IT skill NER in curriculum text
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — keyword matching on Thai job
  postings; the earliest Thai work in the corpus
- [[chaiaroon-2025-thai-digital-workforce-matching]] — skill-based classification of Thai
  digital jobs
- [[herandi-2024-skill-llm]] — fine-tuning a general LLM for extraction
- [[arslan-2026-turkish-skill-extraction]] — extraction *and* linking in a low-resource
  language; the LLM pipeline beats supervised sequence labelling

## Related Concepts
[[skill-entity-linking]] · [[skill-normalisation]] · [[llm-skill-extraction]] ·
[[deep-learning-ner]] · [[rag-skill-extraction]] · [[curriculum-analytics]]

## Relevance to Iris
**This was Iris's core task before 2026-08-27, and is no longer.** The original design
extracted open-vocabulary skill strings from TQF course descriptions and clustered them
into a vocabulary of its own — inheriting every problem above: unstable output across
runs, no ground truth to evaluate against, and results nobody else could reproduce.

Adopting [[thailand-skill-mapping]] converts the task to [[skill-entity-linking]]. The
distinction is not cosmetic: linking output is a set of identifiers, so precision and
recall are directly computable, and two runs produce the same answer.

The concept remains relevant in one place. Skills a course develops that the national
vocabulary does not name still surface as open-vocabulary strings — see
[[nil-entity-linking]] and [[q-out-of-vocabulary]] — and that residue is recorded, never
scored.
