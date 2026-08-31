---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](sentence-piece-tokenization.th.md)

## Definition
**SentencePiece** learns a subword vocabulary directly from raw text, without requiring
pre-tokenised words. Because it treats the input as a character stream — encoding
whitespace as an ordinary symbol — it works for languages with no explicit word
boundaries.

That property makes it the natural fit for Thai ([[thai-tokenization]]): it sidesteps the
ambiguous word-segmentation step entirely rather than depending on a segmenter whose
errors would propagate into every training example. [[lowphansirikul-2021-wangchanberta]]
uses it for WangchanBERTa's Thai vocabulary.

## Papers That Discuss This
- [[lowphansirikul-2021-wangchanberta]] — subword vocabulary construction for Thai
  pretraining
- [[phatthiyaphaibun-2023-pythainlp]] — the explicit word-segmentation alternative

## Related Concepts
[[thai-tokenization]] · [[wangchanberta]] · [[roberta-architecture]] · [[thai-nlp]]

## Relevance to Iris
Iris does not train a tokeniser, but the choice is inherited from whichever embedding
model the Sprint 4 ablation selects, and it has one practical consequence worth checking.

Subword tokenisers segment **unseen or corrupted text into character-level fragments**. A
damaged Thai string like `ข-อมูล` will not be recognised as a word and will be split into
pieces, producing an embedding that carries little meaning. This is a quiet failure — no
error, just a degraded vector — and it is a second, independent reason the integrity gate
must precede embedding, alongside the tokenisation argument in [[thai-tokenization]].

It also suggests a cheap diagnostic worth having: the **average subword-tokens-per-Thai-word
ratio** of a document. An unusually high ratio indicates text the tokeniser does not
recognise as Thai — a corruption signal independent of the diacritic-rate check, and
therefore a useful cross-validation of it.
