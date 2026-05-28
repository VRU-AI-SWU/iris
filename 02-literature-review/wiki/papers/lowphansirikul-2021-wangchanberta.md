---
type: paper
authors: Lalita Lowphansirikul, Charin Polpanumas, Nawat Jantrakulchai, Sarana Nutanong
year: 2021
title: "WangchanBERTa: Pretraining transformer-based Thai Language Models"
venue: arXiv:2101.09635 (cs.CL)
doi: 10.48550/arXiv.2101.09635
relevance: high
questions: [q-thai-nlp]
---

## Research Question
Can a Thai-specific transformer language model — trained on a large, deduplicated Thai corpus — outperform multilingual alternatives (mBERT, XLM-R) on Thai NLP tasks?

## Limitations of Existing Methods
Thai is a low-resource language. Multilingual models (mBERT, XLM-R) have limited Thai training data and underperform on Thai-specific tasks. Earlier Thai BERT models were trained on much smaller datasets, also leading to suboptimal performance. No large-scale, cleanly pretrained Thai language model existed.

## Contribution
WangchanBERTa — a RoBERTa-base model pretrained on 78 GB of deduplicated Thai text from social media, news, and public datasets. Three tokenisation strategies evaluated (word-level, syllable-level, SentencePiece). State-of-the-art results on multiple Thai NLP benchmarks.

## Proposed Method
RoBERTa-base architecture; Thai-specific text preprocessing rules emphasising space preservation; training on 78 GB diverse corpus; comparison of three tokenisation approaches. Evaluated on sequence classification and token classification tasks.

## Key Findings
wangchanberta-base-att-spm-uncased outperforms mBERT and XLM-R on Thai sequence and token classification tasks. SentencePiece tokenisation achieves the best downstream performance. State-of-the-art on Thai NLP benchmarks at time of publication.

## Limitations of This Paper
Evaluated only on monolingual Thai tasks — limited evidence for code-switched Thai-English text performance. Pretraining corpus is primarily informal register (social media, news) and may not represent formal academic Thai used in TQF documents. Benchmarks are general NLP tasks; no skill extraction evaluation.

## Concepts
[[thai-bert]] · [[thai-nlp]] · [[roberta-architecture]] · [[sentence-piece-tokenization]]

## Questions Addressed
[[q-thai-nlp]]

## Notes for Iris
WangchanBERTa is the foundational Thai NLP model for our project. Critical risk: its training data (social media, news) may not represent the formal academic Thai register of TQF course descriptions. This register mismatch could reduce extraction quality. Mitigation options: (1) fine-tune on a small set of TQF text, (2) use translation to English first and rely on English-trained models, (3) use a multilingual LLM (gemma-4-31b-it) that handles Thai without register mismatch. This is a key open question for Q3.
