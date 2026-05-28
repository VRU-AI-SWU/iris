---
type: question
owner: Researcher + Domain Expert
status: open
---

## Question
What skill taxonomy or ontology should we use? (O*NET, ESCO, SFIA, or a Thai-specific custom taxonomy?)

## Why This Matters for Iris
The taxonomy choice determines how skills are named, grouped, and compared across programmes and job postings. A fixed taxonomy enforced at extraction time risks missing context-specific skills; a purely emergent vocabulary risks inconsistency across datasets.

## Initial Hypothesis
Use a data-driven emergent vocabulary at extraction time — let skills surface from the data without forcing a fixed taxonomy. Optionally map the resulting clusters to a reference taxonomy (O*NET, ESCO, SFIA) post-hoc for cross-context comparability and academic reporting.

## Papers Addressing This
- [[sabet-2024-course-skill-atlas]] — uses O*NET DWAs as fixed taxonomy; highlights the limitation that fixed taxonomies miss emerging skills
- [[senger-2024-dl-skill-extraction-survey]] — ESCO is dominant in the field; terminology inconsistency across the literature is a known problem
- [[luyen-2025-skill-decomposition-ontology]] — LLMs can decompose skills to align with ontologies; few-shot prompting improves ontology alignment
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill knowledge base outperforms zero-shot for curriculum skill extraction
- [[kavargyris-2025-escox-skill-extraction]] — ESCOX: LLM + ESCO embeddings pipeline; top extracted SE skills: Java, SQL, DevOps, Python, Agile — cross-check benchmark for our extraction
- [[dixon-2023-occupational-models-42m]] — 775-skill curated vocabulary sufficient for US national scale; confirms bounded vocabulary size is viable
- [[vo-2022-nlp-curriculum-learning-path]] — CSIT-NER: domain-specific BERTOverflow fine-tuning outperforms general BERT for CS/IT skill NER

## Current Working Answer
status: partial

Our emergent vocabulary approach is validated by the literature — fixed taxonomies (O*NET, ESCO) consistently miss emerging and domain-specific skills. ESCO is the most suitable reference taxonomy for post-hoc mapping given its multilingual nature, but lacks Thai language support. The literature shows RAG (retrieval over a growing skill vocabulary) outperforms zero-shot, suggesting we should evolve our extraction from zero-shot toward RAG as our skill vocabulary grows.

## Remaining Uncertainty
Does any Thai-specific skill taxonomy exist that could serve as a starting point? (Q2 not yet answered.) How should we seed the RAG knowledge base before the first TQF extractions?
