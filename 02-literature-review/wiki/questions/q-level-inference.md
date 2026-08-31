---
type: question
owner: Researcher + AI Engineer + Domain Expert
status: open
---

<!-- lang-switch -->
**English** · [ภาษาไทย](q-level-inference.th.md)

## Question
How should a course's **proficiency level** for a linked skill be inferred from a TQF
(มคอ.2) document, and how reliable is each available signal?

## Why This Matters for Iris
The national standard grades every skill into three levels with explicit criteria
([[proficiency-levels]]). Using them turns Iris's output from "this programme does not
cover skill X" into "this programme develops X only to foundational level while the
career requires intermediate" — a materially more useful finding for a curriculum
committee, and the project's novel contribution.

Getting it wrong is worse than not attempting it: a confidently wrong level claim is
harder to detect than a missing skill, and would be discovered in a revision meeting.

## Candidate Signals
Measured as present in the SWU document:

1. **Course learning outcomes (CLOs)** — written per course in the OBE `ชุดรายวิชา`
   format; matched against the skill's own level criteria
2. **Curriculum mapping table** — ● *ความรับผิดชอบหลัก* vs ○ *ความรับผิดชอบรอง* per
   course × learning outcome; the programme's own regulated declaration of centrality
3. **Curriculum position** — year of study from the course code; prerequisite chain depth
4. *(baseline)* LLM judgement from the course description alone

## Papers Addressing This
- [[xu-2025-llm-curricular-analytics]] — LLMs on course documents; brief descriptions are
  the hard case, which is exactly where level inference will be weakest
- [[luyen-2025-skill-decomposition-ontology]] — aligning LLM output to expert-defined
  granularity; the analogous problem one level up
- [[sabet-2024-course-skill-atlas]] — national-scale course→skill mapping, but **binary
  presence only**; no depth grading, confirming the gap
- [[ahadi-2022-skills-taught-vs-sought]] — course×occupation heatmaps, also binary
- [[hilliger-2022-curriculum-analytics-tool]] — multi-level reporting for administrators;
  relevant to how a level claim should be *presented*, not how it is derived
- **[[kumar-2025-bloom-taxonomy-classification]]** — ⭐ **added 2026-08-28.** On six-way
  Bloom classification, **zero-shot LLMs reach only 0.72–0.73 accuracy** while SVM with
  augmentation reaches 94%; RNNs and BERT overfit badly on 600 sentences. A direct measure
  of the naive approach Iris might have taken
- **[[zaki-2023-clo-plo-mapping-automation]]** — ⭐ automating the CLO→PLO matrix reaches
  **83.1% / 88.1%** precision against domain experts, varying by 5 points between two
  programmes at one institution
- [[le-2026-competency-tagging-evidence]] — constrained, evidence-producing competency
  tagging; micro-F1 0.57, MRR 0.82. Evidence spans give "mechanical traceability for human
  auditing"
- [[saroglou-2025-esco-eqf-linking]] — links EQF qualification *levels* as well as
  entities; precedent for level as a linking target, though EQF levels are stated in the
  text rather than inferred

## Current Working Answer
status: open — *empirical, but the 2026-08-28 round rules out one approach and warns about another*

No literature grades curriculum skill depth against a published competency scale; the
reviewed curriculum-analytics work is uniformly binary. The approach remains ours to define
and evaluate. Two findings now shape it:

**1. Do not ask an LLM to judge level holistically.**
[[kumar-2025-bloom-taxonomy-classification]] measures that approach at **0.72–0.73
zero-shot** on a six-way problem, more than 20 points behind a classical classifier with
augmentation on the same data. Bloom's cognitive *verbs* are the feature that classifier
exploits — and Thai TQF CLOs use the same verb conventions (`อธิบาย` explain → lower;
`ออกแบบ` design → higher). This strengthens the plan to derive level from the document's own
declared signals, and adds a requirement: **the Sprint 4 ablation must include a non-LLM
verb-feature baseline over CLO text.** It may win, and that should be discovered before an
LLM-only path is built.

**2. The ● / ○ matrix is evidence, not ground truth.**
[[zaki-2023-clo-plo-mapping-automation]] reconstructs this matrix at 83.1–88.1% precision
against expert judgement, and the two programmes differ by 5 points purely on how outcomes
are written. The matrix in a มคอ.2 is hand-authored for accreditation, with its own noise
and incentives. This is the citation for why the design **records disagreement between the
level sources rather than resolving it silently** — and why cross-institution comparison
must carry a caveat about TQF authoring style.

Plan unchanged in shape: combine all four signals, record disagreement, report per-source
reliability against expert annotation. Disagreement rate is itself a publishable finding.

## Remaining Uncertainty
- Which signal is most reliable, and how often do they conflict?
- Are CLOs written specifically enough to discriminate three levels, or do they cluster?
- Does ● / ○ correlate with skill depth at all, or only with assessment weighting?
- Do documents without CLOs and without a curriculum map (like the KU excerpt) admit any
  level inference beyond curriculum position?

- The Thai standard's three levels are coarser than Bloom's six, which should make the
  problem easier — but its criteria are written as *observable capabilities*, not cognitive
  verbs, so the CLO-verb → standard-level mapping is itself an empirical question
- Neither [[kumar-2025-bloom-taxonomy-classification]] nor
  [[zaki-2023-clo-plo-mapping-automation]] reports inter-annotator agreement. Iris's
  protocol must, because if two experts cannot agree on a level, no model number means
  anything

**Blocked on:** the full KU มคอ.2. The file on hand is an excerpt with no curriculum
mapping table, so this is currently evaluable on one programme only.
