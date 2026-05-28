---
type: concept
---

## Definition
Thai NLP refers to natural language processing techniques applied to the Thai language. Key challenges: no whitespace between words (word segmentation required), tonal language, complex orthography, code-switching with English (common in technical and job posting contexts), low-resource relative to European languages.

## Papers That Discuss This
*(populated via Obsidian backlinks)*

## Related Concepts
[[wangchanberta]] · [[pythainlp]] · [[thai-tokenization]] · [[thai-bert]]

## Relevance to Iris
Thai NLP is central to our skill extraction pipeline. Core toolkit: PyThaiNLP (preprocessing) + WangchanBERTa (encoding) or gemma-4-31b-it (LLM extraction). Key open question: whether to extract skills directly in Thai or translate to English first (Q3). Register mismatch between WangchanBERTa training data and formal TQF text is a known risk.
