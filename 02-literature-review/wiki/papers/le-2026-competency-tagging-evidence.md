---
type: paper
authors: [Le N.L., Abel M.-H., Laforge B.]
year: 2026
title: "From Learning Resources to Competencies: LLM-Based Tagging with Evidence and Graph Constraints"
venue: arXiv (cs.AI, cs.IR) 2605.28483
doi: 10.48550/arXiv.2605.28483
relevance: high
questions: [q-level-inference, q-implied-skills, q-out-of-vocabulary, q-visualisation]
---

## Research Question
How can learning resources be aligned to a competency framework **automatically but
auditably** — so that a human can see why each competency was assigned?

## Limitations of Existing Methods
Manual tagging of learning resources against competency frameworks is labour-intensive and
inconsistent, while fully automated approaches "often lack transparency" and cannot
justify an assignment. Course resources are heterogeneous and frequently revised, so any
alignment decays unless it can be re-derived and re-checked cheaply.

## Contribution
An end-to-end pipeline that uses the LLM as a **"constrained, evidence-producing tagger"**:
it must select competencies from a supplied candidate set *and* return the text span that
justifies each selection, with a competency graph used to suppress structurally
inconsistent assignments.

## Proposed Method
1. **Segmentation** — resources split into pedagogical fragments
2. **Retrieval** — candidate competencies via BM25 plus graph-enriched competency profiles
3. **LLM selection** — the model chooses relevant competencies from candidates and
   identifies the **evidence span** in the source text for each
4. **Refinement** — competency-graph structure filters predictions; fragment-level results
   aggregate to resource level

- **Dataset:** 22 competencies over Computer Science teaching materials (UTC)
- **Baselines:** zero-shot and few-shot LLM variants, retrieval-only baselines, supervised
  classifiers

## Key Findings

| Metric | Score |
|---|---|
| Micro-F1 (fragment level) | **0.57** |
| Macro-F1 (fragment level) | 0.50 |
| Macro-F1 (resource level) | 0.51 |
| MRR | **0.82** |

- The evidence-and-constraints pipeline **outperformed zero-shot/few-shot LLM variants,
  retrieval-only baselines, and supervised classifiers**
- MRR 0.82 against micro-F1 0.57: the right competency is usually ranked near the top even
  when the binary decision is wrong
- Graph constraints measurably reduce spurious tags
- Evidence spans provide "mechanical traceability for human auditing"

## Limitations of This Paper
Only **22 competencies** — two orders of magnitude smaller than the taxonomies in
[[zhang-2024-job-market-entity-linking]] or the Thai national standard, so the candidate
space is far easier. Single institution, single discipline, French/European context. The
authors do not report inter-annotator agreement for the gold labels.

## Concepts
[[skill-entity-linking]] · [[curriculum-analytics]] · [[proficiency-levels]] · [[rag-skill-extraction]]

## Questions Addressed
[[q-level-inference]] · [[q-implied-skills]] · [[q-out-of-vocabulary]] · [[q-visualisation]]

## Notes for the Project
**The closest published system to Iris's architecture**, from the same group as
[[luyen-2025-skill-decomposition-ontology]]. It independently arrives at the design Iris
specified — retrieve candidates, have the LLM select from them, require an evidence span —
and shows it beats every baseline they tried.

The evidence-span requirement is the important convergence. Iris's skill-link review screen
was justified from stakeholder reasoning: a curriculum committee will challenge specific
assignments and the tool must answer immediately. This paper gives the same design an
empirical justification — evidence spans make the output auditable, and the constrained
formulation *outperforms* unconstrained prompting rather than merely explaining it.

Two calibration points, read carefully:

- **Micro-F1 0.57 over 22 competencies** is the optimistic bound, not a target Iris should
  expect. Iris faces 4,376 candidates. Reporting these numbers as comparable would be
  wrong, and the Sprint 4 write-up must say so.
- **MRR 0.82 with F1 0.57** repeats the pattern in
  [[zhang-2024-job-market-entity-linking]] (Acc@32 double Acc@1): ranking is good,
  thresholding is the weak step. This is the strongest cross-paper argument for ordering
  the review screen by confidence and letting a human make the marginal calls.

Their graph constraints have no direct Iris analogue — the national vocabulary is flat,
with no parent/child relations to exploit. Iris's substitutes are the `hard-skill` /
`soft-skill` / `tools` typing, the industry–career–skill structure, and the prerequisite
graph of the curriculum itself. Whether those constrain usefully is worth testing.
