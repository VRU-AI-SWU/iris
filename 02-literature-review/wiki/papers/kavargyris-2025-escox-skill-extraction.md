---
type: paper
authors: Kavargyris D.C., Georgiou K., Papaioannou E., Petrakis K., Mittas N., Angelis L.
year: 2025
title: "ESCOX: A tool for skill and occupation extraction using LLMs from unstructured text"
venue: Software Impacts 25 (2025) 100772, Elsevier
doi: 10.1016/j.simpa.2025.100772
relevance: high
questions: [q-skill-taxonomy, q-skill-extraction]
---

## Research Question
How can LLMs and text embeddings be combined with the ESCO taxonomy to extract skills and occupations from unstructured job postings and general text, with a usable open-source tool for researchers and practitioners?

## Limitations of Existing Methods
Traditional keyword-based skill extraction fails to capture semantic variation and cannot align to standardised taxonomies reliably. Existing tools either do not align to ESCO, require proprietary APIs, or lack usable interfaces for non-developers. No open-source tool combined LLMs + embeddings + ESCO taxonomy in a single pipeline.

## Contribution
ESCOX (ESCOSkillExtractor) — open-source Python tool combining LLMs and ESCO embeddings for skill and occupation extraction from job postings. Graphical web interface, pip-installable, deployed in production as part of EU Horizon SKILLAB project. Handles both skills and occupation classification (ISCO-08) in one pipeline.

## Proposed Method
- **Pipeline**: Text input → LLM-based skill span detection → ESCO embedding similarity matching → skill/occupation classification
- **Taxonomy**: ESCO (European Skills, Competences, Qualifications and Occupations) + ISCO-08 occupational codes
- **Embeddings**: ESCO skill embeddings (sentence-transformers) for semantic matching
- **LLM**: Used for span extraction and summarisation
- **Interface**: Flask web app + REST API; also Google Colab notebook
- **Case study**: ~6,500 Software Engineering job postings from EURES (European Employment Services); classified into 4 ISCO-08 groups
- **Top extracted skills from case study**: Java, SQL, DevOps, "work independently", Python, Agile, communication

## Key Findings
- LLM + embedding pipeline successfully extracts both technical (hard) and soft skills, aligning each to ESCO taxonomy entries
- Dominant SE job skills from EU EURES data: Java, SQL, DevOps, Python, Agile — consistent with industry expectations
- ISCO-08 occupation distribution: ICT Business Analyst, Project Manager, Computer Scientist dominate the extracted SE postings
- Open-source, pip-installable (`pip install esco-skill-extractor`), MIT licensed — maximum reuse potential
- Tool bridges "what someone can do" (skills) with "what someone is qualified for" (occupations) — dual extraction is a design advantage

## Limitations of This Paper
ESCOX is fully dependent on ESCO taxonomy — non-ESCO skills (emerging, domain-specific, regional) will be missed or misclassified. ESCO does not cover Thai-language skills or Thai-context terminology. Case study limited to EU labour market; no evaluation on non-European or non-English job postings. No published precision/recall evaluation against a held-out labelled skill dataset.

## Concepts
[[esco-ontology]] · [[rag-skill-extraction]] · [[skill-taxonomy]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-skill-extraction]]

## Notes for Iris
**Architecture reference for our AI Engineer.** The LLM + embedding + taxonomy pipeline in ESCOX is structurally similar to what Iris needs, but ESCO is not viable for Thai context. Key insight: the separation of (1) span detection via LLM and (2) taxonomy alignment via embedding similarity is a clean two-stage design we should adopt — using our emergent Thai skill vocabulary rather than ESCO for the alignment stage. The ESCOX case study top skills (Java, SQL, Python, Agile) provide a cross-check: if our Thai CS job postings don't surface similar skills in the top-N, something is wrong with our extraction. The open-source MIT license means we can inspect and adapt the pipeline code directly.
