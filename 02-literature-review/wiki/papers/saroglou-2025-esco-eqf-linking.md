---
type: paper
authors: [Saroglou S., Diamantaras K., Preta F., Delianidi M., Benisis A., Meyer C.J.]
year: 2025
title: "Enhancing Job Matching: Occupation, Skill and Qualification Linking with the ESCO and EQF taxonomies"
venue: arXiv (cs.CL) 2512.03195
doi: 10.48550/arXiv.2512.03195
relevance: high
questions: [q-skill-taxonomy, q-implied-skills, q-prevalence-metrics]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](saroglou-2025-esco-eqf-linking.th.md)

## Research Question
Should job-vacancy text be linked to ESCO/EQF by **Sentence Linking** (classify a whole
sentence to a taxonomy entry) or by **Entity Linking** (recognise a span first, then link
it)? And can generative LLMs improve either?

## Limitations of Existing Methods
Prior work stops at "surface-level skill extraction" and does not analyse how *occupations*
and *qualifications* — not just skills — are expressed in postings. The two linking
paradigms had not been compared under the same conditions.

## Contribution
A head-to-head comparison of Sentence Linking and Entity Linking, two new annotated
datasets for occupation and qualification representation, and an open-source tool
implementing both.

## Proposed Method
- **Taxonomies:** ESCO (skills, occupations) and EQF (qualification levels)
- **Pipeline:** entity recognition (for EL) → embedding similarity → top-k ranked
  taxonomy candidates
- **Embeddings:** fine-tuned `all-mpnet-base-v2`; entity-level vs full-sentence embeddings
  compared
- **Evaluation:** Accuracy@1 for linking; strict F1 for the recognition stage

## Key Findings
- **Entity Linking Accuracy@1: 0.2881**
- Sentence Linking reached **0.5387** accuracy on the Occupations task and
  **outperformed Entity Linking overall**, attributed to its ability to use sentence
  context that a bare span discards
- Entity recognition strict F1: **54.3 ± 2.6** (best) and 53.6 ± 2.5
- **Entity-level embeddings outperformed full-sentence embeddings** for the similarity
  module itself
- Supervised approaches "substantially outperform decoder-only models" on classification
  accuracy — a generative LLM alone was not the best tool for the ranking step

## Limitations of This Paper
European taxonomies and European/Ethiopian job data; no low-resource or non-Latin-script
evaluation. The Sentence-vs-Entity comparison is confounded by task (occupations vs
skills), and the authors note their qualitative analysis "does not reveal a clear
advantage for either method" in general.

## Concepts
[[skill-entity-linking]] · [[esco-ontology]] · [[proficiency-levels]] · [[rag-skill-extraction]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-implied-skills]] · [[q-prevalence-metrics]]

## Notes for the Project
The **third independent confirmation** that strict top-1 linking accuracy against a large
occupational taxonomy sits near 0.25–0.30 (0.2881 here, 23.55% in
[[zhang-2024-job-market-entity-linking]], 0.56 end-to-end in
[[arslan-2026-turkish-skill-extraction]]). Three different taxonomies, languages, and
research groups converging is strong enough to plan against.

Their central finding argues directly for one of Iris's design choices: **context helps.**
Sentence Linking beat Entity Linking because the full sentence carries disambiguating
information a bare span loses. Iris links at the level of a whole **course description** —
several sentences of coherent context, richer than either setting here — which supports
the choice not to first extract short skill spans and link those in isolation.

EQF is also worth noting as precedent: this is a linking pipeline that targets a
**qualification *level*** as well as an entity, which is structurally what Iris does with
the national standard's three proficiency levels. EQF levels are declared in the posting
text, whereas Iris must infer level from evidence — a harder problem, and one reason
[[q-level-inference]] remains open.

Caution to carry forward: supervised models beat decoder-only LLMs on their ranking step.
Iris should not assume an LLM adjudicator is automatically the best component, and the
Sprint 4 ablation should include a non-LLM ranking baseline.
