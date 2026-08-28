---
type: concept
---

## Definition
Thai text extracted from PDFs is frequently corrupted in ways that are **invisible to a
naive parser**: the extraction succeeds, returns plausible-looking Thai, and silently
drops or substitutes combining marks.

Two failure modes measured on real มคอ.2 documents (see
[`data-feasibility.md`](../../../03-solution-design/data-feasibility.md)):

**1. Glyph substitution (SWU, Bullzip PDF Printer).** Thai set in TH SarabunPSK under
**WinAnsi** encoding, which has no Thai codepoints. Marks that stack at the second level
above a consonant land in font-private glyph slots with no `ToUnicode` entry and extract
as ASCII. Retention against a clean baseline:

| Mark | Retained | |
|---|---|---|
| ั ิ ี ึ ื ุ ู | 88–134 % | vowels intact |
| ็ | 59 % | partial |
| ่ mai ek | 48 % | partial |
| ้ mai tho | 14 % | severe |
| ์ karan | 1 % | severe |

Result: `ผลการเรียนรู2`, `ข-อมูลทั่วไป`, `วิเคราะห=`, `เป?น`, `ป‚ญญา`. Because the marks
are *substituted* rather than deleted — total marks per 1,000 Thai characters returns to
the clean baseline once substitutions are counted — the damage is **deterministically
reversible** with a table keyed on `(substitute glyph, preceding character)`.

**2. Sara-am collapse (KU, Word 2013).** `ำ` (U+0E33) appears zero times in 22,177 Thai
characters; every one has become `า` (`คำอธิบาย` → `คาอธิบาย`). This **is** lossy —
nothing distinguishes an original `า` from a collapsed `ำ` without a lexicon.

PyMuPDF and poppler produce byte-identical output on both documents: the defect is in
the PDF, not the extractor.

## Diagnostic
The rate of Thai combining marks per 1,000 Thai characters, compared per-mark against a
clean-document baseline (~171 total), detects both modes cheaply and deterministically —
and is the basis of Iris's ingestion gate (`clean` / `repairable` / `unusable`).

## Papers That Discuss This
No paper addresses **PDF text-layer corruption** in Thai — that gap stands. Two 2025–26
papers do document the same vulnerability from the vision side, which is independent
corroboration that Thai diacritics are where Thai document processing breaks:

- [[nonesung-2025-thaiocrbench]] — 2,808 samples, 13 tasks; names "hallucinated or missing
  diacritics" as a systematic VLM failure on Thai, alongside language bias and structural
  mismatch
- [[nonesung-2026-typhoon-ocr]] — ⭐ a Thai-tuned 3B VLM reaches **Levenshtein 0.04 on Thai
  government forms** (GPT-4o 0.57, Gemini 2.5 Flash 0.15); the viable fallback for
  documents whose text layer is lossy rather than merely substituted
- [[phatthiyaphaibun-2023-pythainlp]] — like the Thai NLP literature generally, assumes
  correct input text

## Related Concepts
[[thai-nlp]] · [[curriculum-analytics]] · [[structure-aware-retrieval]]

## Relevance to Iris
Every downstream stage depends on the input text being correct: a missing karan turns
`คอมพิวเตอร์` into `คอมพิวเตอร`, and matching against a correctly-spelled national
vocabulary degrades accordingly. Because the corruption is silent, a pipeline without a
gate would produce confident, wrong results.

The literature offers nothing on this — Thai NLP papers assume clean text, and PDF
extraction papers do not address Thai mark stacking. **The diagnostic and repair method
is therefore a small methodological contribution in its own right**, reusable by anyone
mining Thai institutional PDFs.

**Revised policy after the 2026-08-28 review round.** The original conclusion — "no OCR
needed" — was right for the SWU document, where damage is substitution and repair is exact.
It was wrong as a general rule: KU's `ำ` collapse is genuinely lossy, and
[[nonesung-2026-typhoon-ocr]] shows a self-hostable 3B Thai VLM handles government forms at
Levenshtein 0.04. The gate therefore has three outcomes, not two — *clean* → text layer,
*repairable* → deterministic glyph repair, *lossy or unusable* → vision re-extraction, with
the document flagged as vision-derived in its provenance so downstream findings can say so.
