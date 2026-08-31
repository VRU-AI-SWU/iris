---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](automation-bias.th.md)

## Definition
**Automation bias** is the tendency to accept an automated system's output without the
scrutiny one would apply to the same claim from another source. Its practical consequence
is that a human-plus-AI pair can perform **worse than the AI alone**: the model's errors
pass through unchallenged while the human's independent judgement is suppressed.

It is the reason "put a human in the loop" is a design *problem* rather than a design
*solution*. [[chen-2025-interface-design-high-stakes]] measures which interface mechanisms
mitigate it and finds the answer counter-intuitive — mechanisms that *inform* the reviewer
(confidence, text explanations, performance visualisations) improved decisions and
calibrated trust, while mechanisms that *interrogate* the reviewer (feedback prompts,
AI-generated questions) increased cognitive load, **reduced task performance**, and then
damaged trust.

The related failure is **miscalibrated trust** in either direction: over-trust yields
rubber-stamping, under-trust yields wholesale rejection and abandonment. The design target
is calibration, not maximal trust.

## Papers That Discuss This
- [[chen-2025-interface-design-high-stakes]] — ⭐ 108 participants, high-stakes medical
  decisions; six mechanisms compared, with the inform-versus-interrogate asymmetry as the
  headline
- [[le-2026-competency-tagging-evidence]] — evidence spans for "mechanical traceability
  for human auditing"; the constrained, evidence-producing formulation also *outperformed*
  unconstrained prompting
- [[hilliger-2022-curriculum-analytics-tool]] — administrators are the hardest stakeholder
  to design curriculum analytics for
- [[zhang-2024-job-market-entity-linking]] — the accuracy level (Acc@1 23.55%) that makes
  review necessary in the first place

## Related Concepts
[[skill-entity-linking]] · [[curriculum-analytics]] · [[inter-annotator-agreement]] ·
[[proficiency-levels]]

## Relevance to Iris
Iris's design concluded that the skill-link review screen is **a requirement of the
method**, because measured linking accuracy makes an unreviewed mapping unusable as
evidence. That reasoning is sound but was one-sided: it established that review is
*necessary* without establishing that review is *sufficient*. This concept supplies the
missing half — review can fail, and a badly designed surface can make the pair worse than
the model.

Three implications, recorded in the product design:

1. **The screen's informational elements are the right ones.** Per-link confidence, the
   official skill definition, and the evidence span map onto the three mechanisms that
   measurably helped.
2. **Confidence-first sorting and disagreement display carry risk.** They resemble the
   forcing functions that *hurt* performance here. They are kept for a different reason —
   directing scarce attention, and refusing to hide uncertainty — but they are the first
   things to make optional if review completion degrades in usability testing.
3. **Bulk-accept is the most bias-prone affordance on the screen.** The instrumented
   **correction rate** is the detector: if it falls far below the Sprint 4 measured error
   rate, reviewers are rubber-stamping and the published report is not the evidence it
   claims to be. That check belongs in the analysis of every reviewed programme, not only
   in usability sessions.
