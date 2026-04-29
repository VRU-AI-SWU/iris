---
type: paper
authors: Elena Senger, Mike Zhang, Rob van der Goot, Barbara Plank
year: 2024
title: "Deep Learning-based Computational Job Market Analysis: A Survey on Skill Extraction and Classification from Job Postings"
venue: NLP4HR 2024 @ EACL; arXiv:2402.05617
doi: 10.48550/arXiv.2402.05617
relevance: high
questions: [q-skill-taxonomy, q-implied-skills]
---

## Research Question
What deep learning methods exist for skill extraction and classification from job postings, and what terminology, dataset, and evaluation inconsistencies exist in the field?

## Limitations of Existing Methods
The field lacks consistent terminology — even core concepts like "hard skill", "soft skill", and the sub-tasks of skill extraction are defined differently across papers. No comprehensive survey existed covering deep learning approaches specifically, and dataset documentation is fragmented, making comparison and replication difficult.

## Contribution
Systematic survey of deep learning-based skill extraction from job postings. Consolidation of publicly available datasets with consistent descriptions. A proposed terminology framework for the field. Identification of open problems and future directions.

## Proposed Method
Survey methodology: catalogued papers, datasets, and evaluation approaches; established consistent terminology; mapped relationships between tasks (entity recognition, classification, normalisation, matching).

## Key Findings
ESCO is the dominant taxonomy used across the field. BERT-based models substantially outperform earlier methods for skill extraction. Inconsistent terminology and lack of benchmark standardisation are the field's main obstacles. The majority of work focuses on English job postings with very limited coverage of non-English, especially low-resource, languages.

## Limitations of This Paper
English-centric — no coverage of Thai or other Southeast Asian languages. Survey scope is job postings only, not curriculum documents. Does not address the curriculum-to-market gap analysis task directly.

## Concepts
[[skill-extraction]] · [[esco-ontology]] · [[deep-learning-ner]] · [[job-posting-analysis]] · [[skill-normalisation]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-implied-skills]]

## Notes for Iris
The field's terminology inconsistency is precisely why our emergent vocabulary approach is defensible — there is no universally agreed definition of "skill" even in the literature. ESCO's dominance is worth noting but its English/European focus limits applicability for Thai TQF. The English-centric gap in the literature is a genuine research contribution opportunity for Iris. Skill normalisation (mapping differently-worded skills to the same concept) maps directly to our embedding-based clustering step.
