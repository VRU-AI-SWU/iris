---
type: concept
---

## Definition
WangchanBERTa is a RoBERTa-base transformer model pretrained on 78 GB of Thai text (social media, news, public datasets). It is the state-of-the-art Thai language model for sequence and token classification tasks, outperforming multilingual models (mBERT, XLM-R) on Thai NLP benchmarks. Developed by the AI Research Institute of Thailand (ARIT) team. Best variant: `wangchanberta-base-att-spm-uncased`.

## Papers That Discuss This
*(populated via Obsidian backlinks)*

## Related Concepts
[[thai-bert]] · [[thai-nlp]] · [[roberta-architecture]] · [[pythainlp]]

## Relevance to Iris
Primary candidate model for Thai text encoding in our skill extraction pipeline. Register risk: training data (social media, news) may not match formal academic Thai in TQF course descriptions. Should be evaluated on a small TQF sample before committing. Available via Hugging Face: `airesearch/wangchanberta-base-att-spm-uncased`.
