---
type: concept
---

## Definition
**PyThaiNLP** is the standard open-source Thai NLP toolkit: word tokenisation, sentence
segmentation, POS tagging, normalisation, transliteration, spell checking, and Thai
lexical resources. It is the practical default for Thai text preprocessing because it is
maintained, permissively licensed, and covers the tasks Thai's writing system makes
non-trivial ([[thai-tokenization]]).

Its tokenisers span a speed/accuracy range — dictionary-based `newmm`, `longest`, and
neural options such as `attacut` and `deepcut`.

## Papers That Discuss This
- [[phatthiyaphaibun-2023-pythainlp]] — the toolkit paper; standard toolkit for Thai
  tokenisation, segmentation, and preprocessing
- [[lowphansirikul-2021-wangchanberta]] — Thai LM pretraining, where tokenisation choices
  interact with subword vocabulary ([[sentence-piece-tokenization]])
- [[nonesung-2025-thaiocrbench]] — ⚠️ documents that Thai document pipelines fail at the
  *character* level, upstream of anything a tokeniser can fix

## Related Concepts
[[thai-nlp]] · [[thai-tokenization]] · [[thai-pdf-text-integrity]] · [[wangchanberta]]

## Relevance to Iris
Used for two specific jobs, both narrower than the toolkit's range.

**1. Lexicon-based `ำ` restoration.** The KU document collapsed every `ำ` into `า`
(`คำอธิบาย` → `คาอธิบาย`), which is lossy — nothing in the text distinguishes an original
`า` from a collapsed `ำ`. PyThaiNLP's Thai lexicon is what makes a principled guess
possible, and the residual error rate is reported rather than hidden. See
[[thai-pdf-text-integrity]].

**2. Tokenisation for lexical candidate retrieval.** Thai has no spaces between words, so
BM25-style matching against Thai skill titles needs segmentation first.

⚠️ **The order matters and is easy to get wrong.** Iris's earlier design listed PyThaiNLP
preprocessing as the first pipeline stage. It cannot be: the integrity gate must run
first, because a tokeniser fed `ข-อมูล` will segment it confidently and wrongly, and
nothing downstream will notice. Preprocessing assumes correct input; on real มคอ.2 files
that assumption does not hold. The Thai NLP literature generally shares this blind spot —
see [[q-thai-nlp]].
