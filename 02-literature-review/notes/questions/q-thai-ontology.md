---
type: question
owner: Researcher
status: open
---

## Question
Does a Thai skill ontology exist that maps well to TQF content?

## Why This Matters for Iris
If a Thai skill ontology exists and aligns with the TQF course structure, we could use or adapt it rather than building from scratch. If none exists, this is both a research gap and a contribution opportunity.

## Initial Hypothesis
None. This is an open empirical question — the answer determines whether we build on existing Thai ontology work or pioneer a new one.

## Papers Addressing This
- [[weerasombat-2025-thai-employer-skill-priorities]] — confirms skill mismatch exists in Thailand but uses broad categories, not a granular skill ontology
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — analyses Thai skill demand from job portals but uses keyword matching, not a formal ontology
- [[chaiaroon-2025-thai-digital-workforce-matching]] — defines 20 digital job categories for Thai market but no underlying skill ontology

## Current Working Answer
status: answered

**No Thai skill ontology exists** at the granularity needed for Iris. Thailand has:
- **TQF (มคอ.2)**: defines 5 broad learning outcome domains — not a skill ontology
- **TPQI framework**: occupational standards and competency levels — coarser than skill-level taxonomy; not machine-readable as an ontology
- **ICDL/ECDL** (adopted by TPQI for ICT): covers digital literacy but not CS/software engineering skills

This is both a confirmed research gap and a justification for our emergent vocabulary approach. Post-hoc mapping to ESCO remains the best option for international comparability, accepting that ESCO coverage of Thai-context skills will be incomplete.

## Remaining Uncertainty
Whether TPQI occupational standards for ICT could be used as a partial validation layer (not extraction target) for our skill clusters. Requires manual inspection of TPQI-Net standards.
