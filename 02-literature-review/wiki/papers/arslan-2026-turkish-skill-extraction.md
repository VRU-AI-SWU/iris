---
type: paper
authors: [Arslan İltüzer E., Özlü Ö.A., Farajijobehdar V., Eryiğit G.]
year: 2026
title: "Leveraging LLMs for Turkish Skill Extraction"
venue: arXiv (cs.CL) 2601.22885
doi: 10.48550/arXiv.2601.22885
relevance: high
questions: [q-thai-nlp, q-skill-taxonomy, q-implied-skills]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](arslan-2026-turkish-skill-extraction.th.md)

## Research Question
How should skill extraction be done for a **morphologically complex, low-resource
language** that has neither a skill taxonomy nor an annotated dataset — and does extraction
work better in the native language or after translation to English?

## Limitations of Existing Methods
Skill extraction research is overwhelmingly English. Turkish had no skill taxonomy and no
skill-extraction dataset, so supervised sequence-labelling approaches had nothing to train
on and no benchmark to report against.

## Contribution
The first Turkish skill-extraction dataset, and a systematic comparison of LLM pipelines
against supervised sequence labelling for a low-resource language, aligned to ESCO.

## Proposed Method
- **Dataset:** 4,819 manually annotated skill spans from 327 job postings across
  occupational categories
- **Taxonomy:** ESCO, used as the standardisation target
- **Best pipeline:** Claude Sonnet 3.7 with **dynamic few-shot prompting** for skill
  identification, then **embedding-based retrieval**, then **LLM-based re-ranking** for
  linking
- **Key comparison:** native-language processing vs translate-to-English-first

## Key Findings
- The LLM-based end-to-end pipeline **outperformed supervised sequence labelling**
- Best end-to-end score: **0.56**
- **Native-language extraction beat translation-based alternatives** — translating to
  English first lost information
- Results are comparable to equivalent studies in other languages, i.e. a low-resource
  language is not inherently penalised when the pipeline is built this way

## Limitations of This Paper
No explicit limitations section in the abstract. The dataset is modest (327 postings), and
the strongest configuration depends on a proprietary frontier model, which raises cost and
reproducibility questions for a locally-hosted deployment.

## Concepts
[[skill-entity-linking]] · [[thai-nlp]] · [[esco-ontology]] · [[rag-skill-extraction]]

## Questions Addressed
[[q-thai-nlp]] · [[q-skill-taxonomy]] · [[q-implied-skills]]

## Notes for the Project
**The closest methodological analogue to Iris available in the literature** — a
morphologically complex, low-resource, non-Latin-adjacent language with no native skill
taxonomy, tackled with exactly the architecture Iris has chosen: retrieve candidates by
embedding, then have an LLM re-rank and select.

Two findings transfer directly:

1. **Extract in Thai, do not translate first.** This is independent confirmation of the
   position [[q-thai-nlp]] already held, now with a controlled comparison behind it rather
   than an argument from first principles. Iris's bilingual channel is a *cross-check*
   where an English course description exists, never a substitute for the Thai one.
2. **0.56 end-to-end is a realistic target**, consistent with
   [[zhang-2024-job-market-entity-linking]] and [[saroglou-2025-esco-eqf-linking]].

Iris starts from a better position than this work in one important respect: Turkish had to
borrow ESCO, an imported European taxonomy, whereas Thai now has a native national
vocabulary with Thai-language definitions. The translation-loss problem that motivated
their native-language finding does not apply on the taxonomy side for Iris at all.

The dependence on Claude Sonnet 3.7 is the finding that does *not* transfer cleanly —
Iris runs locally by design. Their result sets an upper reference point; the Sprint 4
ablation over model size is where Iris establishes its own.
