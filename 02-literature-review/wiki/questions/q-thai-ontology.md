---
type: question
owner: Researcher + Domain Expert
status: answered
---

> ⚠️ **Answer reversed 2026-08-27.** This question was previously marked *answered* with
> the conclusion "no Thai skill ontology exists at the needed granularity — a confirmed
> gap". **That conclusion is now false.** It was correct when the literature review was
> conducted, and was overtaken by events rather than by an error in the review.

## Question
Does a Thai-language skill ontology or taxonomy exist at the granularity Iris needs?

## Why This Matters for Iris
The answer determined the entire design. Under the previous answer — no such ontology —
the only defensible approach was an emergent, data-driven vocabulary built by clustering
extracted terms, with post-hoc mapping to ESCO for comparability. That drove the choice
of embedding models, a clustering sidecar, and a vector database.

## Papers and Sources Addressing This
- [[tpqi-framework]] — Thailand Professional Qualification Institute: occupational
  standards and competency certification, but coarser than a skill ontology and not
  machine-readable at skill granularity. **Still true.**
- [[esco-ontology]] — 27 languages, none of them Thai. **Still true.**
- [[siddoo-2019-thai-digital-workforce-competency]] — EFA-derived three-category Thai
  digital competency taxonomy; too coarse
- [[chaiaroon-2025-thai-digital-workforce-matching]] — 20-category Thai digital *job*
  taxonomy; roles, not skills
- [[tipsena-2025-predicting-thai-digital-workforce]] — five-segment DEPA framework;
  segments, not skills
- **[[thailand-skill-mapping]]** — ⭐ **the answer.** Published July 2025 by สป.อว.
  (OPS MHESI), developed by KMITL: 4,376 Thai skills with definitions and three graded
  proficiency levels each, mapped to 371 careers across five industries, served over an
  open API

## Current Working Answer
status: **answered — a Thai national skill vocabulary now exists**

The gap this question identified was real and is now closed. Thailand Skill Mapping
provides Thai-language skills at exactly the granularity Iris needs (`ภาษาไพธอน`,
`การจัดเก็บข้อมูลในคลังข้อมูล`, `สกัดข้อมูล แปลงข้อมูล และโหลดข้อมูล (ETL)`), with
official standing, bilingual labels, machine-readable access, and graded proficiency
criteria that ESCO itself does not offer.

Every design consequence of the old answer is therefore void: emergent vocabulary
construction, clustering, the vector database, and post-hoc ESCO mapping. See
[[q-skill-taxonomy]].

## Why the review did not find it
The review was conducted in April 2026 against **academic literature**. The standard was
published as **government open data** in July 2025 and, as of this writing, has no
accompanying peer-reviewed paper describing the database itself. Searching journals for a
Thai skill ontology would not have surfaced it.

**Methodological note for the lab:** for infrastructure questions — does a dataset, an
ontology, a registry exist? — a literature search is insufficient. Government open-data
portals and ministry publications must be searched directly. Worth adding to the
literature-review methodology.

## Remaining Uncertainty
- What corpus underlies the demand figures, and is it Thai? *(external: สป.อว. / KMITL)*
- Is there a peer-reviewed publication describing the database, needed for citation?
  *(the KMUTT EV skill-mapping paper is a different artefact — see below)*
- How is the vocabulary maintained, and on what cadence?
- Coverage of academic-CS content that job postings do not describe — see
  [[q-out-of-vocabulary]]

## ⚠️ Citation hazard
`Anmanatarkul et al. (2025), "Development of Learning Modules and Skills Mapping to
Prepare Workforce Competencies for the Electric Vehicle Industry"` (FTE Journal) is a
**KMUTT** paper describing a Delphi expert-consensus skill map with seven skill groups
for the EV industry. It is a legitimate methodological precedent for linking curricula to
careers via skill mapping, **but it is not the KMITL/สป.อว. database** and must not be
cited as if it were.
