---
type: question
owner: Researcher + AI Engineer + Domain Expert
status: open
---

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

## Current Working Answer
status: open

No literature grades curriculum skill depth against a published competency scale — the
reviewed curriculum-analytics work is uniformly binary. The approach is therefore ours to
define and evaluate.

Planned: combine all four signals, **record disagreement rather than resolving it
silently**, and report per-source reliability against expert annotation. Disagreement rate
is itself a finding worth publishing.

## Remaining Uncertainty
- Which signal is most reliable, and how often do they conflict?
- Are CLOs written specifically enough to discriminate three levels, or do they cluster?
- Does ● / ○ correlate with skill depth at all, or only with assessment weighting?
- Do documents without CLOs and without a curriculum map (like the KU excerpt) admit any
  level inference beyond curriculum position?

**Blocked on:** the full KU มคอ.2. The file on hand is an excerpt with no curriculum
mapping table, so this is currently evaluable on one programme only.
