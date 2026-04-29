# Brainstorm — Iris (Skill Gap Analysis)

> **This is a living document.** Phases 1 (Brainstorm) and 2 (Literature Review) are iterative.
> Each pass through the literature may refine or redirect the ideas here. Update this document
> after each iteration. Proceed to Phase 3 only after a formal go decision.

---

## Context

**Primary context:** Thai undergraduate academic programmes, using the official TQF document (มคอ.2 / Thai Qualifications Framework) as the data source.
**Extension scope:** English-taught programmes in Thailand (same TQF format). Overseas programmes excluded in v1 due to different regulatory frameworks.

---

## Problem Statement

Academic programmes are designed with intended learning outcomes, but two critical misalignments persist:

1. **Programme-to-Programme Gap** — Different academic programmes produce graduates with different skill profiles. These differences are rarely made explicit or quantified, making cross-programme comparison difficult for institutions, accreditation bodies, and students choosing between programmes.

2. **Programme-to-Market Gap** — Academic programmes evolve slowly while job market requirements shift rapidly. Graduates often enter the workforce with skill profiles misaligned with what employers need for a given career path. Institutions lack a systematic, data-driven mechanism to detect and respond to this drift.

**Who experiences it:** Academic administrators, curriculum designers, students, career advisors, accreditation bodies, employers.

**Cost of not solving it:** Graduates are underprepared for specific career paths; institutions waste resources on outdated skills; students make uninformed programme and career choices.

---

## Target Users / Stakeholders

| User / Stakeholder | Role | Key Need |
|---|---|---|
| Academic administrator | Curriculum review decision-maker | Evidence of which skills are over/under-represented vs market demands |
| Curriculum designer | Builds and updates programme content | Specific, actionable skill gaps to address in course design |
| Student | Chooses programme or plans career | Understand their programme's coverage relative to a target career path |
| Career advisor | Guides students on career planning | Data-driven comparison tool to use in advising sessions |
| Accreditation body | Validates programme quality | Benchmark programmes against industry standards |
| Employer / HR | Hires graduates | Transparency into what skill profile a programme produces |

---

## Goals & Success Criteria

| Goal | How We Measure Success |
|---|---|
| Quantify gap between two programmes | Ranked list of skill differences with magnitude scores |
| Quantify gap between a programme and a career path | Deficit/surplus report mapped to job posting requirements |
| Make gaps actionable | Each gap is traceable to specific courses or job postings |
| Accessible outputs | Non-technical stakeholders can interpret reports without data science knowledge |
| Reproducible analysis | Same inputs produce same outputs; methodology is peer-reviewable |

---

## Scope

**In scope:**
- Skill extraction from academic programme documents (syllabi, course descriptions, learning outcomes)
- Skill extraction from job postings for a specified career path
- Skill distribution construction and comparison (programme vs programme; programme vs market)
- Gap quantification and summary reporting
- Web interface or report output for non-technical users

**Out of scope (v1):**
- Real-time job posting scraping (start with a static snapshot dataset)
- Individual student skill assessment (programme-level analysis only)
- Soft skills and personality traits (focus on technical and domain skills)
- Automated curriculum redesign recommendations (gap identification only, not prescription)

---

## Key Hypotheses

1. **Skills can be reliably extracted from free text** — NLP models can extract meaningful skills from syllabi and job postings with sufficient accuracy for comparative analysis.
2. **Skill embeddings capture semantic similarity** — Differently-worded skills (e.g., "machine learning" vs "predictive modelling") can be matched meaningfully using embedding-based similarity.
3. **Job postings are a valid proxy for market demand** — Aggregating skills from a large sample of job postings for a career path produces a stable, representative skill distribution.
4. **Programme skill distributions are stable** — A programme's skill profile derived from its current syllabi reasonably represents what graduates know.
5. **Gap magnitude correlates with curriculum action priority** — Larger gaps indicate higher-priority areas for curriculum review.

---

## TQF Document Structure (Key Finding from SWU & KU Documents)

Both SWU (มศว) and KU (เกษตรศาสตร์) CS programmes follow identical TQF (มคอ.2) structure. A unified parser can work across all Thai universities.

**Useful sections for skill extraction:**

| Section | Thai Name | Content | Skill Signal |
|---|---|---|---|
| Course list | รายวิชา | All courses with category classification | Course inventory |
| Study plan | แผนการศึกษา | Which year/semester each course is taught | Temporal progression |
| Course descriptions | คำอธิบายรายวิชา | Topics covered per course (richest signal) | **Primary skill source** |
| Programme Learning Outcomes | ผลลัพธ์การเรียนรู้ระดับหลักสูตร (ELOs) | High-level expected outcomes at graduation | High-level skill validation |

**SWU ELOs (5 outcomes):**
1. Communicate using CS knowledge in collaborative work
2. Apply CS knowledge to solve problems
3. Analyze, design, and develop CS systems ethically
4. Evaluate information system performance and infrastructure
5. Public consciousness, teamwork, and project management

**Key structural observations:**
- SWU organizes courses into **bundles** (ชุดวิชา) — useful intermediate level between course and programme
- KU provides **bilingual descriptions** (Thai + English) — easier for skill extraction
- Both have ~124–126 credit hours, split across General Ed, Major-specific, and Free elective categories
- **Major-specific courses** (หมวดวิชาเฉพาะ) should be weighted higher than General Education in skill extraction
- Free elective courses (หมวดวิชาเลือกเสรี) vary per student — treat as optional/secondary signal

**Credit weighting approach:**
- หมวดวิชาเฉพาะ (Major): primary weight
- หมวดวิชาศึกษาทั่วไป (General Ed): secondary weight
- หมวดวิชาเลือกเสรี (Free Elective): excluded from v1 (student-variable)

---

## Constraints

- TQF documents are in Thai — skill extraction must handle Thai text (and bilingual where available)
- Course descriptions vary in richness — some are brief; skill extraction must be robust to sparse text
- Job posting data must be ethically sourced and legally usable
- Analysis must be explainable to non-technical academic stakeholders — black-box results will not be trusted or acted on
- Must produce outputs suitable for academic publication (rigorous and reproducible methodology)
- v1 scope: Thai-language TQF documents; bilingual documents are a bonus

---

## Open Questions

| Question | Owner | Due |
|---|---|---|
| What skill taxonomy/ontology should we use? (O*NET, ESCO, SFIA, or Thai-specific custom?) | Researcher + Domain Expert | Literature review |
| Does a Thai skill ontology exist that maps well to TQF content? | Researcher | Literature review |
| How do we handle Thai-language skill extraction — translate first or extract in Thai? | AI Engineer + Data Scientist | Literature review |
| How do we handle skills implied by course content but not explicitly stated? | AI Engineer + Data Scientist | Literature review |
| What is the minimum job posting sample size for a stable career path distribution? | Data Scientist | Literature review |
| Where can we obtain Thai job posting datasets ethically? (JobThai, LinkedIn TH, etc.) | Data Engineer | Literature review |
| How do we handle temporal drift in job postings? | Data Engineer + Data Scientist | Literature review |
| Should course credit hours weight the skill contribution? | Data Scientist + Domain Expert | Solution Design |
| What visualisation format is most actionable for academic administrators? | UX/UI Designer + Domain Expert | Solution Design |
| Should the gap be symmetric or directional? (A lacks X vs B has excess Y) | Data Scientist + Product Manager | Solution Design |
| What is the best practical segment taxonomy for Thai industry context? | Domain Expert + Researcher | Literature review |
| How reliable is LLM-based segment inference from job description text alone? | AI Engineer + Data Scientist | Literature review |
| Can Thai company registries (DBD, SET) provide reliable industry segment lookups? | Data Engineer | Literature review |

---

## Initial Ideas

**Skill extraction approach — data-driven emergent vocabulary:**
- Extract raw skills from TQF course descriptions using LLM (`gemma-4-31b-it`)
- Do NOT force a fixed taxonomy at extraction time — let skills emerge from the data
- Cluster semantically similar skills using `text-embedding-embeddinggemma-300m` (e.g., "machine learning" ≈ "predictive modelling")
- Build a shared skill vocabulary from the union of all programmes being compared
- Optionally: map skill clusters to a reference taxonomy (O*NET, ESCO) for cross-context comparability
- Decompose into **common skills** (shared across programmes) and **unique skills** (distinguishing each programme)

**Common vs unique skill structure:**
```
Programme A skills ──┐
                      ├── Common skills (shared baseline)
Programme B skills ──┘
                      ── A-unique skills (what A has that B doesn't)
                      ── B-unique skills (what B has that A doesn't)
```
This naturally handles programmes of varying closeness — CS vs DS will have large common set; CS vs EE will have small common set.

**Skill distribution representation:**
- Frequency-weighted vector over the emergent skill vocabulary
- Credit-hour weighted (major-specific courses weighted higher than general education)
- Embedding centroid per programme for high-level similarity comparison

**Gap quantification approaches:**
- Set-based gap: skills present in B but absent in A (and vice versa) — most interpretable
- Cosine distance between skill distribution vectors — overall similarity score
- KL divergence between frequency distributions — asymmetric gap measurement
- Hybrid: set-based for report, cosine/KL for aggregate score

**Job posting sources (Thailand):**
- **Primary:** JobThai.com (largest Thai portal, scraping-friendly), JobsDB Thailand, Indeed Thailand
- **Secondary:** LinkedIn Thailand (strong anti-scraping defense — treat as supplementary)
- **Architecture:** unified job posting schema (title, description, requirements, company, date) with a thin adapter per source; LLM handles within-source format variation

**Curriculum scenario system (free elective toggle):**
Rather than binary include/exclude, implement named scenarios:
- **Scenario: Core** — required courses only (หมวดวิชาเฉพาะ บังคับ) — stable baseline
- **Scenario: Core + Electives** — include user-specified free electives
- **Scenario: Hypothetical** — proposed future curriculum (add/remove any courses)
This turns Iris into a planning tool: *"what would our skill distribution look like if we added these electives?"*

**Industry segment breakdown:**
Academic institutions want to know not just *what skills are missing* but *which industry segments their programme fits or misses*. Example insight: *"Your CS programme aligns well with Finance and Insurance segments but has a significant gap for Manufacturing."*

Segment information is not always available in job postings:
- **Direct**: some postings include company name and/or industry field → extract directly
- **Indirect**: company name visible but segment unknown → web search agent looks up company profile (LinkedIn, Thai company registry, etc.)
- **Hidden**: agency postings that intentionally obscure employer identity → LLM classifier infers segment from job description vocabulary (fintech, manufacturing, healthcare each have distinctive language patterns)

Segment taxonomy: use a practical flat list of ~10–15 segments meaningful for Thai academic context (e.g., Finance/Banking, Insurance, Manufacturing, Technology/Software, Healthcare, Retail/E-commerce, Government/Public Sector, Energy/Utilities, Telecommunications, Logistics/Supply Chain) rather than full TSIC for v1. Map TSIC optionally for formal reporting.

**Output formats:**
- Gap summary report (PDF / markdown) with common/unique skill decomposition
- Interactive web dashboard with radar charts and ranked gap tables
- Per-skill breakdown showing which courses contribute each skill
- Scenario comparison view (side-by-side skill distributions across scenarios)
- **Industry segment view**: heatmap of programme fit score per industry segment

---

## Iteration Log

_Record each pass through the Brainstorm ↔ Literature Review loop._

| Iteration | What the Literature Revealed | How the Idea Changed | Date |
|---|---|---|---|
| 1 | _(pending literature review)_ | | |

---

## Go Decision

- [ ] Problem statement is stable and evidence-grounded
- [ ] Key hypotheses are validated or consciously accepted as risks
- [ ] Gaps and opportunities from the literature are understood
- [ ] Team is aligned on scope and direction

**Go decision made by:** _______________  **Date:** _______________

**Summary of final idea (post-iteration):**

---

## Decisions Made

| Decision | Rationale | Date |
|---|---|---|
| Primary context is Thai academic programmes using TQF (มคอ.2) | TQF is the official structured standard across all Thai universities — consistent format enables unified parser | 2026-04-28 |
| Start with static job posting dataset | Reduces v1 complexity; live scraping can be added in v2 | 2026-04-28 |
| Exclude soft skills from v1 | Hard to extract reliably; technical skills are more actionable for curriculum design | 2026-04-28 |
| Free elective courses handled via scenario system, not excluded | Binary exclusion loses information; scenario toggle supports "what-if" analysis for planning | 2026-04-28 |
| Weight major-specific courses (หมวดวิชาเฉพาะ) higher than general education | Major courses define the programme's technical identity | 2026-04-28 |
| Use course descriptions (คำอธิบายรายวิชา) as primary skill extraction source | Richest and most consistent signal across all TQF documents | 2026-04-28 |
| Data-driven emergent skill vocabulary, not fixed taxonomy | No gold standard exists for programme skills; bottom-up extraction then optional taxonomy mapping is more honest and flexible | 2026-04-28 |
| Multi-source job posting scraping with unified schema + per-source adapters | Handles format variety without tight coupling; LLM fills gaps within sources | 2026-04-28 |
| Industry segment enrichment via 3-tier pipeline (direct → search agent → LLM classifier) | Agency postings hide employer info; need fallback inference from job description content | 2026-04-28 |
| Use practical 10–15 segment taxonomy for v1, TSIC mapping optional | TSIC is too granular for actionable institutional insight; custom segments are more interpretable | 2026-04-28 |
| Literature review conducted as Obsidian knowledge graph (atomic notes + wikilinks) | Bidirectional linking between question, paper, and concept nodes makes research gaps visually identifiable; aligns with Karpathy LLMwiki approach | 2026-04-29 |
| LLM-assisted paper ingestion via structured prompt template | Researchers always extract the same things from a paper (research question, limitations of existing methods, contribution, proposed method, findings, limitations); a fixed prompt enforces consistency and speeds up ingestion | 2026-04-29 |
