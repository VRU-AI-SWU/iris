---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](roberta-architecture.th.md)

## Definition
**RoBERTa** (Robustly Optimized BERT Pretraining Approach) is a refinement of BERT that
keeps the transformer encoder and changes the training recipe: masked language modelling
only (dropping next-sentence prediction), dynamic masking, larger batches, more data, and
longer training. The result is consistently better downstream performance from the same
architecture.

It became the default recipe for pretraining monolingual encoders in languages other than
English — including [[wangchanberta]] for Thai
([[lowphansirikul-2021-wangchanberta]]) — because it is well understood and needs no
architectural innovation, only corpus and compute.

## Papers That Discuss This
- [[lowphansirikul-2021-wangchanberta]] — WangchanBERTa follows the RoBERTa recipe for
  Thai, with [[sentence-piece-tokenization]] for subword vocabulary
- [[kumar-2025-bloom-taxonomy-classification]] — ⚠️ RoBERTa initially overcame overfitting
  on 600 learning outcomes but degraded during training; a classical SVM with augmentation
  reached 94%

## Related Concepts
[[wangchanberta]] · [[thai-bert]] · [[sentence-piece-tokenization]] · [[deep-learning-ner]]

## Relevance to Iris
Background rather than a design choice — Iris does not pretrain or fine-tune an encoder.
It matters for reading two papers correctly.

It explains what [[wangchanberta]] *is*, and therefore why its failure in
[[lertmethaphat-2025-thai-job-market-nlp]] is about the Thai corpus and objective rather
than about the architecture — the same recipe works well elsewhere.

More usefully, [[kumar-2025-bloom-taxonomy-classification]] provides a caution Iris acts
on. On 600 labelled learning outcomes, RoBERTa and BERT overfitted while an SVM with data
augmentation reached 94%. Iris's Sprint 4 annotation set is ~50 courses — a comparable
data regime. **Fine-tuning a transformer on it would very likely overfit**, which is one
reason the pipeline is built on retrieval plus a prompted model rather than on a
supervised classifier, and why the annotation budget goes to *evaluation* rather than to
training data.
