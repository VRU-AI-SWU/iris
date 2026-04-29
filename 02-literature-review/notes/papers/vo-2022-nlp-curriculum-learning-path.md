---
type: paper
authors: Vo N.N.Y., Vu Q.T., Vu N.H., Vu T.A., Mach B.D., Xu G.
year: 2022
title: "Domain-specific NLP system to support learning path and curriculum design at tech universities"
venue: Computers and Education: Artificial Intelligence 3 (2022) 100042, Elsevier
doi: 10.1016/j.caeai.2021.100042
relevance: high
questions: [q-skill-taxonomy, q-skill-extraction, q-curriculum-analytics]
---

## Research Question
How can a domain-specific NLP system extract CS/IT skills from course content and job postings to support course recommendation and curriculum design at tech universities?

## Limitations of Existing Methods
Prior NER models for skill extraction in CS/IT were domain-general (not trained on CS/IT corpora) or used shallow CRF-based models without contextual embeddings. Existing course recommendation systems relied on collaborative filtering or simple word similarity, not on skill-level semantic matching. No end-to-end system connected university course content to industry job requirements at skill granularity.

## Contribution
(1) **CSIT-NER** — domain-specific Named Entity Recognition model for CS/IT skills, fine-tuned on StackOverflow + GitHub text using BERTOverflow embeddings. Outperforms general-domain NER baselines on all metrics. (2) **Hybrid CSIT-CRS** — course recommendation system using CSIT-NER skill extraction; provides multi-level recommendations (university courses, career paths, online MOOCs). Evaluated with 201 users (students and faculty in Australia and Vietnam).

## Proposed Method
- **CSIT-NER**: BERTOverflow embeddings (BERT pre-trained on StackOverflow data) + BiLSTM + CRF layer; trained and fine-tuned on CS/IT text from StackOverflow and GitHub; entity types: programming languages, frameworks, tools, concepts
- **CSIT-CRS**: Hybrid recommendation — (a) skill gap analysis between student profile and career path requirements, (b) course-skill similarity matching, (c) MOOC recommendation for skill gaps
- **Data**: StackOverflow + GitHub for NER training; job listings from real CS/IT companies for career path skill requirements
- **Evaluation**: Standard NER metrics (precision, recall, F1) vs. BERTOverflow baseline; user survey (201 participants, Australia + Vietnam)

## Key Findings
- CSIT-NER outperforms state-of-the-art NER models (including BERTOverflow) on CS/IT skill extraction across all evaluation metrics
- Transfer learning from a domain-specific corpus (StackOverflow/GitHub) substantially improves skill entity recognition accuracy vs. general BERT
- Hybrid recommendation (skills-based) is rated highly by students for relevance and usefulness in curriculum planning
- CS/IT skill vocabulary from StackOverflow/GitHub is highly English-language and tech-stack specific — good coverage for programming skills, weaker for soft/management skills

## Limitations of This Paper
Training corpus (StackOverflow + GitHub) is entirely English; model performance on bilingual (Thai+English) technical text is untested. StackOverflow data skews toward open-source/web development — may underperform for enterprise or non-coding roles. Course recommendation system assumes fixed course-skill mapping — does not extract skills from course syllabi dynamically. Evaluation is user satisfaction survey, not controlled experiment.

## Concepts
[[skill-extraction]] · [[curriculum-analytics]] · [[rag-skill-extraction]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-skill-extraction]] · [[q-curriculum-analytics]]

## Notes for Iris
**Two direct design implications for Iris:**
1. **Domain-specific embedding for skill NER**: The CSIT-NER result confirms that a BERTOverflow-style model (pre-trained on domain text) significantly outperforms general BERT for CS/IT skill extraction. For Iris, this means our skill extraction from TQF syllabi (which contain Thai + English CS terminology) should use a model with some CS/IT domain awareness — either BERTOverflow for English passages, or a multilingual equivalent. The Thai academic register is a challenge CSIT-NER does not address.
2. **Multi-level gap output**: The CSIT-CRS architecture (gap analysis → course match → MOOC gap fill) is structurally similar to our brainstorm's 3-tier scenario system. This is validation that the gap-then-recommend pipeline is a proven pattern in the literature.
