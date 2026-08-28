---
type: concept
---

## Definition
Thai is written **without spaces between words**. Spaces mark phrase or clause boundaries
instead, so word segmentation is a required first step for almost any Thai NLP task, and
it is genuinely ambiguous: the same character sequence often admits several valid
segmentations with different meanings.

This is why Thai counts as a low-resource language for pipeline purposes even though it
has abundant text — every downstream component inherits the segmenter's errors.
Approaches range from dictionary-based longest-matching to neural sequence labelling,
available in [[pythainlp]].

Related complications: no inherent capitalisation, no inflectional morphology to signal
boundaries, and heavy Thai–English code-switching in technical writing — exactly the
register of a computer-science curriculum.

## Papers That Discuss This
- [[phatthiyaphaibun-2023-pythainlp]] — the standard toolkit; tokenisation and
  segmentation
- [[lowphansirikul-2021-wangchanberta]] — subword vocabulary construction for Thai
  ([[sentence-piece-tokenization]]) as an alternative to explicit word segmentation
- [[nonesung-2026-typhoon-ocr]] — names "the absence of explicit word boundaries" as a
  core obstacle for Thai document models

## Related Concepts
[[thai-nlp]] · [[pythainlp]] · [[sentence-piece-tokenization]] ·
[[thai-pdf-text-integrity]] · [[wangchanberta]]

## Relevance to Iris
Needed for **lexical candidate retrieval** — BM25-style matching between a Thai course
description and the 4,376 Thai skill titles requires both sides segmented consistently.
Dense retrieval does not need it, but lexical matching is what catches tool names and
exact terminology that embeddings blur, so both channels run.

Two Iris-specific notes.

**Segmentation is downstream of integrity.** A corrupted character sequence segments
without error and without meaning: `ข-อมูล` is not `ข้อมูล` to any tokeniser. The
diacritic gate runs first, always.

**Code-switching is the norm, not an edge case.** A มคอ.2 course description reads
`ภาษาเอสคิวแอล` in one clause and `React.js` in the next. Thai skill titles in the
standard do the same. Segmenters handle mixed scripts unevenly, which is one more reason
the bilingual channel — linking the English description independently where the document
provides one — is a useful cross-check rather than a redundancy.
