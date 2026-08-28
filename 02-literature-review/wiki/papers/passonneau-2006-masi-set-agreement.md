---
type: paper
authors: [Passonneau R.]
year: 2006
title: "Measuring Agreement on Set-valued Items (MASI) for Semantic and Pragmatic Annotation"
venue: LREC 2006
doi: null
relevance: high
questions: [q-implied-skills, q-level-inference, q-out-of-vocabulary]
---

## Research Question
How should inter-annotator agreement be measured when each annotator assigns a **set** of
labels to an item, rather than choosing one category from a fixed list?

## Limitations of Existing Methods
Conventional reliability metrics — Cohen's κ, Fleiss' κ, Scott's π — assume each unit gets
exactly one categorical value. Applied to set-valued annotation they compare sets for
**exact identity**, so `{A, B}` versus `{A, B, C}` scores as complete disagreement, the
same as `{A, B}` versus `{X, Y}`. Partial agreement, which is the normal case in semantic
annotation, is invisible. Annotation projects on complex semantic or pragmatic phenomena
therefore could not report meaningful reliability at all.

## Contribution
**MASI**, a distance metric for set comparison that captures partial agreement, usable as
the distance function δ inside any weighted agreement coefficient — Krippendorff's α or
Artstein & Poesio's β. It is independent of how expected agreement is computed.

## Proposed Method

**MASI = J × M**

- **J** — the Jaccard (1908) coefficient, `|Q ∩ P| / |Q ∪ P|`, weighting the difference in
  set size independently of set relationship
- **M** — a **monotonicity** term penalising conflicting sets more than nested ones:

| Relationship between sets Q and P | M |
|---|---|
| identical | **1** |
| one a subset of the other | **2/3** |
| intersection and both differences non-null | **1/3** |
| disjoint | **0** |

Used as δ in Krippendorff's α, over *m* coders and *r* units:

```
α = 1 − ( (rm−1) Σᵢ Σ_b Σ_{c>b} n_b^i n_c^i δ_bc ) / ( m Σ_b Σ_c n_b n_c δ_bc )
```

## Key Findings
- The monotonicity term separates cases conventional metrics conflate. On the worked
  example, an annotation matrix with a monotonic (subset) relationship scores mean MASI
  **10/27 = 0.37**, while one with symmetric differences scores **6/27 = 0.22** — a
  distinction that exact-match agreement cannot express at all
- MASI is independent of the expected-agreement calculation, so it composes with any
  weighted coefficient rather than requiring a new one
- Artstein and Poesio (2005) find quantitative differences between metric families are
  generally small — the choice that matters here is the **distance function**, not the
  coefficient

## Limitations of This Paper
Demonstrated on co-reference and summarisation-pyramid annotation, not on entity linking
to a large controlled vocabulary. MASI has no notion of *semantic* distance between
labels — `{SQL}` versus `{MySQL}` is as distant as `{SQL}` versus `{Ethics}`, which
understates agreement when annotators pick near-synonymous entries from a fine-grained
taxonomy.

## Concepts
[[inter-annotator-agreement]] · [[skill-entity-linking]] · [[nil-entity-linking]]

## Questions Addressed
[[q-implied-skills]] · [[q-level-inference]] · [[q-out-of-vocabulary]]

## Notes for the Project
**This corrects an error in the Sprint 4 evaluation plan that would have produced the
wrong number.**

The plan commits to two annotators and to reporting inter-annotator agreement, and — on
[[zhang-2024-job-market-entity-linking]]'s advice — to permitting **multiple correct links
per course**. That makes Iris's annotation task set-valued by construction: each annotator
assigns a *set* of national skill IDs to each course. Nothing in the plan said which
agreement statistic to use, and the default choice would have been Cohen's or Fleiss' κ.

On this task those are simply wrong. Two annotators returning `{SQL, Data Modeling}` and
`{SQL, Data Modeling, Database Design}` for CP242 have agreed substantially; exact-match
κ scores it as total disagreement. Since subset relationships are the *expected* form of
disagreement between a strict and a generous annotator, κ would systematically understate
agreement — and a low reported IAA would then discredit an evaluation that is actually
sound.

**Adopted for the skill-set annotation:** Krippendorff's α with the MASI distance. The
monotonicity term is the property that matters — it distinguishes *"one annotator was more
generous"* (M = 2/3) from *"the annotators disagree about what this course teaches"*
(M = 1/3 or 0), which is exactly the distinction the annotation guideline must be tuned
against.

⚠️ **Not for the level assignment.** Level is a single **ordinal** value per
(course, skill) pair — `พื้นฐาน < ปานกลาง < สูง` — not a set. MASI would score
*foundational vs intermediate* as exactly as distant as *foundational vs advanced*,
discarding the ordering that is the whole content of a level. Level agreement uses
Krippendorff's α with an **ordinal** distance, so adjacent-level disagreement counts as
partial agreement. Choosing δ by data type is the general lesson; MASI is the right answer
only for the set-valued half.

The stated limitation is live for Iris and should be reported: MASI treats
`การสร้างแบบจำลองข้อมูลเชิงสัมพันธ์` and `การสร้างแบบจำลองข้อมูลเชิงตรรกะ` as fully
distinct, so agreement on a fine-grained vocabulary is measured conservatively. A
semantically-weighted variant is out of scope for v1 but worth naming in the limitations.
