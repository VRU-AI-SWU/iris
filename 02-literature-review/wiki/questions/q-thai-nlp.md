---
type: question
owner: AI Engineer + Data Scientist
status: open
---

## Question
How do we handle Thai-language skill extraction — translate to English first, or extract directly in Thai?

## Why This Matters for Iris
TQF documents are primarily in Thai. The approach chosen affects model selection, extraction accuracy, and downstream skill matching. Translating first introduces noise; extracting in Thai requires Thai-capable NLP models.

## Initial Hypothesis
None yet. The decision depends on the quality of available Thai NLP models versus translation quality, and whether skill terms are more standardised in English or Thai in this domain.

## Papers Addressing This
- [[lowphansirikul-2021-wangchanberta]] — WangchanBERTa is the state-of-the-art Thai NLP model; outperforms mBERT and XLM-R on Thai tasks
- [[phatthiyaphaibun-2023-pythainlp]] — PyThaiNLP is the standard Thai NLP toolkit for preprocessing (tokenisation, segmentation)
- [[lertmethaphat-2025-thai-job-market-nlp]] — **Critical finding**: WangchanBERTa FAILS to discriminate closely related Thai job titles (97.21% similarity between Physician and Dentist); USE + XGBoost (~90% accuracy) outperforms WangchanBERTa for Thai job title classification
- [[xu-2025-llm-curricular-analytics]] — RAG outperforms zero-shot for curriculum skill extraction; LLMs handle brief/abstract documents well

## Current Working Answer
status: partial

**Revised recommendation — do NOT rely on WangchanBERTa alone.** lertmethaphat-2025 directly demonstrates WangchanBERTa fails at discriminating semantically related Thai terms. This is a critical finding for skill extraction: skill terms like "data analysis" vs. "data engineering" vs. "data science" are exactly the kind of closely related terms WangchanBERTa will conflate.

Revised pipeline:
- **PyThaiNLP**: preprocessing only (tokenisation, segmentation, stop word removal) — well-suited for this
- **Skill extraction from text**: multilingual LLM (gemma-4-31b-it) — handles Thai natively, no register mismatch, no disambiguation failure
- **Skill matching/embedding**: Universal Sentence Encoder (USE) or multilingual sentence-transformers — validated over WangchanBERTa for disambiguation
- **Avoid**: WangchanBERTa as a standalone classification model for fine-grained skill terms

## Remaining Uncertainty
Register mismatch of WangchanBERTa on formal TQF Thai needs empirical testing. Whether gemma-4-31b-it handles formal Thai well enough for skill extraction from TQF descriptions is unvalidated. No Thai-specific skill extraction benchmark exists to evaluate against.
