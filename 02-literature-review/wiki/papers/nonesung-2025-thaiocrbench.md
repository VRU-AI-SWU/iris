---
type: paper
authors: [Nonesung S., Jaknamon T., Chaiophat S., Nitarach N., Wittayasakpan C., Sirichotedumrong W., Na-Thalang A., Pipatanakul K.]
year: 2025
title: "ThaiOCRBench: A Task-Diverse Benchmark for Vision-Language Understanding in Thai"
venue: IJCNLP-AACL 2025 (Main Conference)
doi: 10.48550/arXiv.2511.04479
relevance: medium
questions: [q-thai-nlp]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](nonesung-2025-thaiocrbench.th.md)

## Research Question
How well do current vision-language models actually understand **Thai text-rich documents**,
and where specifically do they fail?

## Limitations of Existing Methods
Document-understanding benchmarks "predominantly focus on high-resource languages, leaving
Thai underrepresented". Without a Thai benchmark there was no way to choose a model for
Thai document work, or to know which stages of a document pipeline were unsafe.

## Contribution
The first comprehensive Thai benchmark for text-rich visual understanding, with a
task-level error analysis that names the failure modes rather than reporting a single
score.

## Proposed Method
- **2,808 human-verified samples** across **13 task categories** and 30+ domains
  (government, finance, education, legal, retail, transport)
- Four capability areas: OCR/text recognition · structural understanding (table, chart,
  document parsing) · key-information extraction · multimodal reasoning
- Content includes Thai numerals, mixed scripts (Pali/Sanskrit inside Thai), forms,
  tables, charts, infographics, handwriting
- Zero-shot evaluation of proprietary and open-source VLMs

## Key Findings
- **Gemini 2.5 Pro ranked highest overall**; Qwen2.5-VL 72B was the strongest open-source
  model; a "significant performance gap" separates proprietary from open systems
- **Fine-grained text recognition is the hardest task**, with the steepest drops among
  open-source models, followed by handwritten content extraction
- Three named failure modes: **language bias** (drifting into English), **structural
  mismatch** (misaligned tables and forms), and **hallucinated content**
- Thai-specific penalties come from "Thai diacritics, small fonts, headless Thai scripts,
  and visually similar Thai–English characters", with **hallucinated or missing diacritics**
  called out explicitly

## Limitations of This Paper
Zero-shot only, so it measures models as shipped rather than their ceiling after
fine-tuning — a caveat borne out by [[nonesung-2026-typhoon-ocr]], where a Thai-tuned 3B
model beats far larger general ones. Public per-model numeric scores are limited in the
released summary.

## Concepts
[[thai-pdf-text-integrity]] · [[thai-nlp]]

## Questions Addressed
[[q-thai-nlp]]

## Notes for the Project
Independent, benchmark-scale confirmation of what
[`data-feasibility.md`](../../../03-solution-design/data-feasibility.md) measured on two
documents: **Thai diacritics are where Thai document processing breaks.** Iris found tone
marks and karan destroyed in a PDF text layer; this benchmark finds "hallucinated or
missing diacritics" as a systematic failure of vision models on Thai. The same
vulnerability, reached by two different routes.

That convergence is worth stating in the paper, because it establishes that Iris's
integrity gate is not defensive over-engineering for one bad file — diacritic loss is a
recognised, benchmarked property of Thai document processing, and **any** extraction
route can produce it. The gate must therefore run **after** the vision fallback too, not
only on the text-layer path.

Two operational consequences:

- **"Language bias" — drifting into English — is a real risk for the vision fallback.** A
  มคอ.2 is bilingual by design, so a model that silently switches language could produce
  fluent, wrong output. The diacritic-rate diagnostic will not catch that; a Thai-character
  proportion check will.
- **"Structural mismatch" in tables** bears directly on the curriculum mapping table. Iris
  extracts its ● / ○ marks from PDF glyph coordinates, which sidesteps this failure
  entirely — a reason to prefer the positional route over asking a VLM to read the table,
  even where the vision fallback is used for prose.

Model-selection note: this benchmark ranks general VLMs, and its own follow-up work shows a
3B Thai-tuned model beating them on structured Thai documents. Iris should not read
"Gemini 2.5 Pro ranked highest" as a recommendation — it evaluates a class of model Iris
has ruled out on privacy and cost grounds.
