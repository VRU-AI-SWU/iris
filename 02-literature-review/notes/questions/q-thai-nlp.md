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
- [[lertmethaphat-2025-thai-job-market-nlp]] — WangchanBERTa validated for Thai job posting NLP; bilingual Thai+English job titles common on Thai platforms
- [[xu-2025-llm-curricular-analytics]] — RAG outperforms zero-shot for curriculum skill extraction; LLMs handle brief/abstract documents well

## Current Working Answer
status: partial

Recommended pipeline: PyThaiNLP for Thai text preprocessing → WangchanBERTa or gemma-4-31b-it for encoding/extraction. Key risk: WangchanBERTa is trained on informal Thai (social media, news) and may underperform on formal academic Thai in TQF documents. A multilingual LLM (gemma-4-31b-it) that natively handles Thai may be more robust to register differences. Extraction-in-Thai is preferred over translate-first to avoid compounding translation errors in skill terms.

## Remaining Uncertainty
Register mismatch of WangchanBERTa on formal TQF Thai needs empirical testing. Whether gemma-4-31b-it handles formal Thai well enough for skill extraction from TQF descriptions is unvalidated. No Thai-specific skill extraction benchmark exists to evaluate against.
