---
type: paper
authors: [Zaki N., Turaev S., Shuaib K., Krishnan A., Mohamed E.]
year: 2023
title: "Automating the mapping of course learning outcomes to program learning outcomes using natural language processing for accurate educational program evaluation"
venue: "Education and Information Technologies 28(12), 16723–16742"
doi: 10.1007/s10639-023-11877-4
relevance: high
questions: [q-level-inference, q-credit-weighting, q-visualisation]
---

## Research Question
Can the mapping of course learning outcomes (CLOs) to programme learning outcomes (PLOs) —
the matrix every outcome-based curriculum must publish for accreditation — be automated and
validated with NLP?

## Limitations of Existing Methods
CLO→PLO mapping is done by hand. It is slow, inconsistent between mappers, and prone to
bias, yet it is the artefact accreditation bodies inspect. Because it is authored rather
than derived, nobody knows how accurate any given published mapping is.

## Contribution
An NLP system that produces the CLO→PLO mapping automatically, validated against the
mapping domain experts produced for the same programmes, delivered as a web tool for
teachers and administrators.

## Proposed Method
- NLP similarity between CLO text and PLO text, automating construction of the mapping matrix
- Evaluated on **two real educational programmes'** complete outcome sets
- Compared against the mapping produced by **domain experts** for the same programmes
- Packaged as a web-based tool intended for routine use by faculty

## Key Findings

| Programme | Precision vs domain experts |
|---|---|
| Programme 1 | **83.1%** |
| Programme 2 | **88.1%** |

- Automated mapping reaches the mid-to-high 80s against expert judgement, i.e. useful as a
  **draft for review** rather than as a replacement for the expert
- The gap between the two programmes shows sensitivity to how outcomes are written, not
  only to the method

## Limitations of This Paper
Two programmes at one institution, English only. Precision is reported against expert
mapping treated as ground truth, but **no inter-expert agreement is reported**, so it is
unknown how much of the 12–17% disagreement is model error rather than legitimate
ambiguity. It maps outcome text to outcome text; it does not assign a *level* or connect
either side to labour-market demand.

## Concepts
[[curriculum-analytics]] · [[proficiency-levels]] · [[skill-entity-linking]]

## Questions Addressed
[[q-level-inference]] · [[q-credit-weighting]] · [[q-visualisation]]

## Notes for the Project
Iris reads the CLO→PLO artefact this paper generates. In Thai TQF documents it is
**แผนที่แสดงการกระจายความรับผิดชอบ (Curriculum Mapping)**, with ● ความรับผิดชอบหลัก and
○ ความรับผิดชอบรอง marking each course × outcome pair — and it is a required, regulated
part of every มคอ.2. Iris treats it as evidence for [[q-level-inference]] rather than
something to generate.

That difference in direction carries a warning this paper supplies and no other source in
the corpus does. **The ● / ○ matrix is itself authored by hand, at roughly 83–88% agreement
with expert judgement when reconstructed.** Iris is inferring proficiency level partly from
a signal that is not gold — it is a curriculum committee's declaration, made for
accreditation, with its own noise and its own incentives. The design's decision to combine
it with CLO text and curriculum position, and to **record disagreement between sources
rather than resolve it**, is the right response to that; this paper is the citation for why
that caution is necessary.

Two further points:

- Precision varies by 5 points between two programmes at one institution purely on how
  outcomes are written. Iris compares programmes *across* universities, so cross-institution
  variance in TQF authoring style is a real threat to comparability and belongs in the
  limitations of any comparison result.
- The absence of reported inter-expert agreement is the same gap flagged in
  [[kumar-2025-bloom-taxonomy-classification]]. Two of the closest papers to Iris's
  evaluation both omit it. Iris's Sprint 4 protocol reports it, which is a small but real
  methodological improvement to claim.
