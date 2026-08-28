---
type: paper
authors: [Nonesung S., Nitarach N., Jaknamon T., Taveekitworachai P., Pipatanakul K.]
year: 2026
title: "Typhoon OCR: Open Vision-Language Model For Thai Document Extraction"
venue: arXiv (cs.CL) 2601.14722
doi: 10.48550/arXiv.2601.14722
relevance: high
questions: [q-thai-nlp]
---

## Research Question
Can an open, lightweight vision-language model extract text and structure from **real Thai
documents** as well as far larger proprietary models?

## Limitations of Existing Methods
VLMs are built for high-resource languages. Thai poses "script complexity from non-latin
letters, the absence of explicit word boundaries", and real Thai documents are largely
unstructured, so general-purpose open models perform poorly. Traditional OCR loses layout;
frontier proprietary VLMs are costly and cannot be self-hosted.

## Contribution
Typhoon OCR V1.5 — an open 3B/7B VLM for Thai and English document extraction that matches
or beats frontier proprietary models on structured Thai documents at a fraction of the
compute.

## Proposed Method
- **Training corpus:** 53.7% retained from the Typhoon OCR V1 corpus, 37.6% synthetic
  documents from a generation pipeline, remainder curated; built from traditional OCR
  output restructured by a VLM
- **Two supervision modes:** *Default Mode* for loosely structured documents (receipts,
  handwritten notes) and *Structure Mode* for complex layouts (financial reports,
  government forms)
- **Input standardisation:** images resized to a fixed width of 1,800 px — variable sizing
  destabilised optimisation and reduced accuracy
- **Metrics:** BLEU, ROUGE-L, and Levenshtein distance for lexical accuracy, plus
  sequence-level structural similarity

## Key Findings

**Thai Government Forms** — the document class closest to มคอ.2:

| Model | BLEU ↑ | ROUGE-L ↑ | Levenshtein ↓ |
|---|---|---|---|
| GPT-4o (2024-11-20) | 0.25 | 0.45 | 0.57 |
| Gemini 2.5 Flash (2025-04-17) | 0.74 | 0.87 | 0.15 |
| **Typhoon OCR 3B (image)** | **0.93** | **0.96** | **0.04** |
| Typhoon OCR 7B (PDF) | 0.89 | 0.94 | 0.08 |

**Thai Financial Reports:** Typhoon OCR 3B/7B reach BLEU 0.90–0.91 and Levenshtein
0.07–0.08, against GPT-4o at 0.25 / 0.56.

- The 3B model matches or beats the 7B on several categories — capability here comes from
  Thai-specific training data, not scale
- The model quantises well, "with only limited impact on accuracy"

## Limitations of This Paper
Evaluation is on the authors' own document categories; no comparison against a *correct*
PDF text layer, only against other VLMs. No reported breakdown by Thai diacritic or tone
mark specifically, which is the failure mode Iris cares most about. Structure Mode output
is a layout serialisation, not a semantic table parse.

## Concepts
[[thai-pdf-text-integrity]] · [[thai-nlp]] · [[curriculum-analytics]]

## Questions Addressed
[[q-thai-nlp]]

## Notes for the Project
This changes one of Iris's design conclusions and should be reflected in the solution
proposal.

The [`data-feasibility.md`](../../../03-solution-design/data-feasibility.md) study found
two failure modes in real มคอ.2 files. The SWU case — tone marks and karan substituted by
ASCII through WinAnsi font encoding — is deterministically reversible, and a repair table
remains the right answer there: auditable, free, reproducible. **That conclusion stands.**

The KU case does not. Every `ำ` in that document has collapsed to `า`, and nothing in the
text layer distinguishes them, so repair is genuinely lossy and needs a lexicon guess.
Iris's stated fallback was "request a better source file", which is not always possible.
**Typhoon OCR is the better fallback**, and the evidence is directly on point: Thai
government forms at Levenshtein 0.04 from a 3B model that fits alongside the adjudication
model on `linux-gpu-server`, self-hosted, no API cost, consistent with the project's
local-inference premise.

Revised ingestion policy for the integrity gate:

| Class | Action |
|---|---|
| clean | use the text layer |
| repairable (substitution damage) | deterministic glyph repair — auditable, preferred |
| **lossy (e.g. `ำ` collapse) or unusable** | **re-extract with Typhoon OCR, flag the document as vision-derived in provenance** |

The provenance flag matters: a vision-derived extraction is a *model output*, not a
faithful reading of the document, and any finding traced back to it should say so.

Their fixed-width-1,800 finding is a concrete implementation detail worth reusing if Iris
renders pages for this path.
