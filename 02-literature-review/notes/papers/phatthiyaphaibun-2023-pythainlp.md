---
type: paper
authors: Wannaphong Phatthiyaphaibun, Korakot Chaovavanich, Charin Polpanumas, Arthit Suriyawongkul, Lalita Lowphansirikul, Pattarawat Chormai, Peerat Limkonchotiwat, Thanathip Suntorntip, Can Udomcharoenchaikit
year: 2023
title: "PyThaiNLP: Thai Natural Language Processing in Python"
venue: NLP-OSS 2023 @ EMNLP, Singapore
doi: https://arxiv.org/abs/2312.04649
relevance: medium
questions: [q-thai-nlp]
---

## Research Question
How can Thai NLP tools be made accessible, standardised, and reproducible for the research community through an open-source library?

## Limitations of Existing Methods
Thai NLP tools are fragmented across different implementations; no unified library existed for common Thai NLP tasks. Researchers had to assemble preprocessing pipelines from disparate sources, making reproducibility difficult. Thai-specific challenges (no whitespace between words, complex tokenisation) were handled inconsistently.

## Contribution
PyThaiNLP — an open-source Python library providing pre-trained models, datasets, and tools for Thai NLP tasks including tokenisation, word segmentation, POS tagging, NER, transliteration, and text classification. Community-maintained with wide adoption.

## Proposed Method
Unified API design wrapping multiple Thai NLP models and tools; integration with WangchanBERTa and other pre-trained models; curated Thai NLP datasets; community contribution model.

## Key Findings
PyThaiNLP has become the standard Thai NLP library; supports a wide range of tasks; facilitates reproducible Thai NLP research. Actively maintained by a community of Thai NLP researchers.

## Limitations of This Paper
Library scope is broad rather than deep — some tasks have limited or no pre-trained model options. Skill-specific extraction is not directly supported. NER models are general-purpose, not domain-specific. Documentation quality varies by module.

## Concepts
[[thai-nlp]] · [[pythainlp]] · [[thai-tokenization]]

## Questions Addressed
[[q-thai-nlp]]

## Notes for Iris
PyThaiNLP is the practical starting point for Thai text preprocessing in our pipeline — tokenisation and sentence segmentation of TQF course descriptions. For skill extraction specifically, we build on top of PyThaiNLP with WangchanBERTa or our LLM approach. The library is actively maintained (important for long-term reproducibility). Installation: `pip install pythainlp`. GitHub: pythainlp/pythainlp.
