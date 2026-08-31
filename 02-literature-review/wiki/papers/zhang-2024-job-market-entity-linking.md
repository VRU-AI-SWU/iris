---
type: paper
authors: [Zhang M., van der Goot R., Plank B.]
year: 2024
title: "Entity Linking in the Job Market Domain"
venue: Findings of EACL 2024
doi: 10.48550/arXiv.2401.17979
relevance: high
questions: [q-implied-skills, q-out-of-vocabulary, q-prevalence-metrics, q-skill-taxonomy]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](zhang-2024-job-market-entity-linking.th.md)

## Research Question
Can fine-grained, span-level skill mentions in job-market text be linked to a standardised
occupational taxonomy (ESCO), rather than classifying whole sentences?

## Limitations of Existing Methods
Prior work linked **coarse-grained full sentences** to ESCO skills. Nothing addressed
span-level mentions, so systems could not say *which words* justified a skill assignment —
and could not be evaluated at the granularity a downstream application needs.

## Contribution
The first entity-linking study in the job-market domain: span-level skill mentions mapped
to ESCO, with a synthetic training corpus and a human-annotated benchmark released for the
task.

## Proposed Method
- **Target taxonomy:** ESCO, 13,890 skills
- **Training data:** 123,619 synthetic mention–skill pairs covering 12,984 unique ESCO
  titles, generated with GPT-3.5
- **Evaluation data:** real job advertisements, manually annotated — dev 480 instances
  (149 unique titles), test 1,824 instances (455 unique titles)
- **Models:** BLINK (bi-encoder, `bert-large`) and GENRE (autoregressive, `bart-large`),
  both with Wiki + ESCO continued pre-training

## Key Findings

| Model | Acc@1 | Acc@4 | Acc@8 | Acc@16 | Acc@32 |
|---|---|---|---|---|---|
| BLINK (bi-encoder) | **23.55%** | 32.63% | 37.38% | 43.25% | 48.98% |
| GENRE (autoregressive) | 11.48% | 21.26% | 27.40% | 37.21% | 49.78% |

- The bi-encoder wins decisively under strict top-1 evaluation; the autoregressive model
  catches up only when many candidates are allowed
- **Top-1 accuracy is low in absolute terms (23.55%) while Acc@32 more than doubles it** —
  the correct skill is usually *retrievable*, but selecting it is the hard part
- Both models could link **implicit** skill mentions, where the surface text does not name
  the taxonomy entry

## Limitations of This Paper
Stated by the authors: English only, with no evidence of generalisation to other
languages; training on GPT-3.5 synthetic data may not capture real-document variation; and
critically, **evaluation assumes exactly one gold ESCO title per mention**, which
underestimates performance when several links are legitimately valid.

## Concepts
[[skill-entity-linking]] · [[esco-ontology]] · [[rag-skill-extraction]] · [[skill-gap-quantification]]

## Questions Addressed
[[q-implied-skills]] · [[q-out-of-vocabulary]] · [[q-prevalence-metrics]] · [[q-skill-taxonomy]]

## Notes for the Project
The most direct precedent for Iris's core task, and the single most important calibration
point for the Sprint 4 evaluation gate: **state-of-the-art skill entity linking achieves
Acc@1 of 23.55% against a 13,890-entry taxonomy.** Any expectation that Iris will link
Thai course descriptions to the national vocabulary at high top-1 accuracy is
unsupported by the literature.

Three consequences for the design:

1. **The human review screen is not polish, it is required.** At these accuracy levels an
   unreviewed automated mapping cannot be presented to a curriculum committee as evidence.
2. **The retrieve-then-adjudicate architecture is validated.** Acc@32 (48.98%) being twice
   Acc@1 says recall is far cheaper than precision — exactly the gap an LLM adjudication
   stage exists to close, and a reason to keep `k` generous.
3. **Iris's setting is easier in two respects worth stating in the paper.** The national
   vocabulary is 4,376 entries against ESCO's 13,890 — a 3× smaller candidate space — and
   a course description is a richer, more contextual input than a job-posting span. Iris
   should not report its numbers as directly comparable, but has grounds to expect better.

Their evaluation caveat is also ours: a course legitimately develops several related
skills, so single-gold-label scoring would understate performance. Iris's annotation
protocol must allow multiple correct links per span.
