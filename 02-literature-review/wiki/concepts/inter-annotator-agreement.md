---
type: concept
---

## Definition
**Inter-annotator agreement (IAA)** measures how consistently independent human annotators
apply an annotation scheme. It is the evidence that a gold standard is a property of the
task rather than of one person's judgement — and therefore the precondition for any model
result measured against it. If two experts cannot agree, a model's score against either of
them means nothing.

Coefficients correct raw agreement for chance:

| Coefficient | Handles |
|---|---|
| Cohen's κ | two annotators, single categorical label |
| Fleiss' κ | many annotators, single categorical label |
| **Krippendorff's α** | any number of annotators, missing data, **any distance function δ** |

The choice that matters for structured annotation is not the coefficient but the
**distance function**. For single-label tasks δ is binary (0 if equal, 1 otherwise). For
**set-valued** tasks — where each annotator assigns a *set* — binary δ scores `{A, B}`
against `{A, B, C}` as total disagreement, identical to `{A, B}` against `{X, Y}`.
[[passonneau-2006-masi-set-agreement]] introduced the **MASI** distance (Jaccard ×
monotonicity) to capture partial agreement, and it is the standard choice for set-valued
annotation inside Krippendorff's α.

## Papers That Discuss This
- [[passonneau-2006-masi-set-agreement]] — ⭐ MASI; the monotonicity term separates
  "one annotator was more generous" (M = 2/3) from genuine conflict (M = 1/3 or 0)
- [[zhang-2024-job-market-entity-linking]] — evaluates against a *single* gold ESCO title
  per mention and notes this understates performance where several links are valid
- [[kumar-2025-bloom-taxonomy-classification]] — ⚠️ reports 94% classifier accuracy on
  Bloom levels with **no inter-annotator agreement** for the gold labels
- [[zaki-2023-clo-plo-mapping-automation]] — ⚠️ reports 83–88% precision against "domain
  experts" with **no inter-expert agreement**, so it is unknown how much of the 12–17%
  gap is model error rather than legitimate ambiguity

## Related Concepts
[[skill-entity-linking]] · [[nil-entity-linking]] · [[proficiency-levels]] ·
[[curriculum-analytics]]

## Relevance to Iris
The Sprint 4 gate rests on this. Iris commits to two independent annotators over a
stratified ~50-course sample and to reporting agreement — and, following
[[zhang-2024-job-market-entity-linking]], to permitting **multiple correct links per
course**. That makes the task **set-valued**, so:

**Krippendorff's α with the MASI distance**, not Cohen's or Fleiss' κ. Plain κ would treat
a strict annotator's `{SQL, Data Modeling}` and a generous one's
`{SQL, Data Modeling, Database Design}` as complete disagreement — and since that subset
pattern is the *expected* form of disagreement here, κ would systematically understate
agreement and discredit a sound evaluation.

Two of the closest papers to Iris's evaluation — [[kumar-2025-bloom-taxonomy-classification]]
and [[zaki-2023-clo-plo-mapping-automation]] — report model accuracy against expert labels
without reporting agreement between the experts. Iris reporting it properly is a small,
genuine methodological improvement on both, and it is cheap: the second annotator is
already in the plan.

Known limitation to state: MASI has no semantic distance, so agreement on a fine-grained
vocabulary where annotators pick near-synonyms
(`การสร้างแบบจำลองข้อมูลเชิงสัมพันธ์` vs `...เชิงตรรกะ`) is measured conservatively.
