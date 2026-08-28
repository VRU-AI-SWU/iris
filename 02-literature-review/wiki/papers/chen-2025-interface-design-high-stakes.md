---
type: paper
authors: [Chen Z., Luo Y., Sra M.]
year: 2025
title: "Engaging with AI: How Interface Design Shapes Human-AI Collaboration in High-Stakes Decision-Making"
venue: arXiv (cs.HC) 2501.16627
doi: 10.48550/arXiv.2501.16627
relevance: high
questions: [q-visualisation, q-implied-skills, q-level-inference]
---

## Research Question
Which interface mechanisms — explanations and cognitive forcing functions — actually
improve expert decision quality and trust calibration when a person reviews AI
recommendations in a high-stakes domain?

## Limitations of Existing Methods
**Human-AI teams frequently underperform the AI alone.** Reviewers exhibit *automation
bias*: they accept incorrect recommendations without scrutiny. Text-based explanations
(XAI) often fail because users engage System 1 intuitive processing rather than
deliberative reasoning, so an explanation is read as a reassurance rather than as
evidence to check.

## Contribution
A controlled comparison of six decision-support mechanisms across two families, isolating
which help, which are neutral, and which actively harm.

## Proposed Method
- **108 participants**, controlled experiment
- **Domain:** diabetes management decisions (high-stakes, expert-judgement)
- **Mechanisms tested:** AI confidence display · text explanations · performance
  visualisations · human feedback prompts · AI-driven questions · visual explanations
- **Outcomes:** engagement, trust calibration, collaborative task performance

## Key Findings

| Mechanism | Effect |
|---|---|
| **AI confidence** | ✅ improved performance and calibrated trust |
| **Text explanations** | ✅ improved performance and calibrated trust |
| **Performance visualisations** | ✅ improved performance and calibrated trust |
| Human feedback prompts | ⚠️ deepened reflection but **reduced task performance** — cognitive load, and trust suffered |
| AI-driven questions | ⚠️ same pattern — reflection up, performance down |
| Simple visual explanations | ➖ negligible effect on trust calibration |

The headline is the asymmetry: mechanisms that *inform* helped; mechanisms that *interrogate
the reviewer* raised cognitive load enough to make decisions worse, and then damaged trust.

## Limitations of This Paper
A single medical task with lay-ish participants rather than domain experts in their own
workflow; a laboratory session rather than sustained professional use. Six mechanisms
tested in isolation, so interaction effects between them are unknown — and a review screen
necessarily combines several.

## Concepts
[[automation-bias]] · [[curriculum-analytics]] · [[skill-entity-linking]] ·
[[proficiency-levels]]

## Questions Addressed
[[q-visualisation]] · [[q-implied-skills]] · [[q-level-inference]]

## Notes for the Project
Iris's design concluded that the **skill-link review screen is a requirement of the
method**, because measured linking accuracy (Acc@1 0.23–0.29) makes an unreviewed mapping
unusable as evidence. That conclusion stands — but it was reached without any evidence
about whether human review *works*, and this paper supplies the missing half: **human
review is not automatically an improvement.** Under automation bias, a badly designed
review surface can leave the pair performing worse than the model alone.

Three consequences for the review screen as currently specified.

**What the design already gets right.** The screen shows per-link confidence, the skill's
official definition, and the evidence span — that is *AI confidence* plus *text
explanation*, the two mechanisms with the strongest positive effect here. The level-source
agreement display is a form of performance visualisation. No change needed.

**Where the design carries risk.** Sorting lowest-confidence-first and surfacing
level-source disagreement are, in this paper's terms, close to *cognitive forcing
functions* — and the forcing mechanisms tested here **reduced performance**. The
justification for keeping them is different from the justification for the others: they
exist to direct scarce attention and to avoid hiding uncertainty, not to provoke
reflection. They should be measured against the product-design target (a 78-course
programme reviewed in one sitting), and if review completion degrades, confidence sorting
is the first thing to make optional.

**What to add.** Automation bias predicts that bulk-accept on high-confidence links will
be used indiscriminately — it is the single most bias-prone affordance on the screen.
Instrumenting the correction rate (already a stated success measure) is how that gets
caught: a correction rate far below the Sprint 4 error rate means reviewers are rubber-
stamping, not reviewing, and the report is not the evidence it claims to be.
