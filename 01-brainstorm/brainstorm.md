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

| Question | Owner | Status |
|---|---|---|
| What skill taxonomy/ontology should we use? (O*NET, ESCO, SFIA, or Thai-specific custom?) | Researcher + Domain Expert | **Resolved** — Emergent vocabulary; no fixed taxonomy at extraction time; optional post-hoc ESCO mapping for comparability |
| Does a Thai skill ontology exist that maps well to TQF content? | Researcher | **Resolved** — No Thai skill ontology exists (confirmed research gap); TPQI occupational standards are not machine-readable |
| How do we handle Thai-language skill extraction — translate first or extract in Thai? | AI Engineer + Data Scientist | **Resolved** — Extract directly using gemma-4-31b-it (multilingual); PyThaiNLP for preprocessing only; USE for embedding/matching |
| How do we handle skills implied by course content but not explicitly stated? | AI Engineer + Data Scientist | **Deferred to Phase 4** — RAG-enhanced extraction (xu-2025) earmarked for v2; v1 uses zero-shot LLM |
| What is the minimum job posting sample size for a stable career path distribution? | Data Scientist | **Resolved** — 1,000–2,000 postings per career path (tipsena-2025 benchmark for Thai digital sector) |
| Where can we obtain Thai job posting datasets ethically? (JobThai, LinkedIn TH, etc.) | Data Engineer | **Resolved** — 4 confirmed Thai academic platforms: Jobthai, Jobsdb, JOBBKK, JOBTOPGUN (chaiaroon-2025); LinkedIn excluded |
| How do we handle temporal drift in job postings? | Data Engineer + Data Scientist | **Resolved** — 12-month bounded collection window for v1 (macedo-2022); sliding window weighted averages earmarked for v2 (seif-2024) |
| Should course credit hours weight the skill contribution? | Data Scientist + Domain Expert | **Deferred to Phase 4** — Principle adopted (major courses weighted higher); exact weighting function to be determined empirically |
| What visualisation format is most actionable for academic administrators? | UX/UI Designer + Domain Expert | **Resolved** — Heatmap (courses × skills) + narrative summary for administrators; course drill-down for curriculum designers (ahadi-2022, hilliger-2022) |
| Should the gap be symmetric or directional? (A lacks X vs B has excess Y) | Data Scientist + Product Manager | **Resolved** — Directional; KL divergence in market‖programme direction (sabet-2024); penalises what graduates lack |
| What is the best practical segment taxonomy for Thai industry context? | Domain Expert + Researcher | **Resolved** — chaiaroon-2025 20-role Thai digital taxonomy for career paths; industry sector (Finance, Healthcare, etc.) is secondary enrichment only |
| How reliable is LLM-based segment inference from job description text alone? | AI Engineer + Data Scientist | **Deferred to Phase 4** — No literature benchmark for Thai context; validate empirically during implementation |
| Can Thai company registries (DBD, SET) provide reliable industry segment lookups? | Data Engineer | **Deferred to Phase 4** — No literature evidence; assess during data pipeline implementation |

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
| 1 | **NLP pipeline**: WangchanBERTa fails to discriminate closely related Thai terms (97.21% similarity between Physician/Dentist — lertmethaphat-2025). USE + XGBoost achieves ~90% accuracy on Thai job titles. **Skill taxonomy**: No Thai skill ontology exists (q-thai-ontology answered). Emergent vocabulary is the only viable approach; RAG > zero-shot for curriculum extraction (xu-2025). **Gap metric**: KL divergence (market‖programme direction) is the validated asymmetric aggregate metric (sabet-2024). **Job posting sources**: 4 Thai platforms confirmed for academic use: Jobthai, Jobsdb, JOBBKK, JOBTOPGUN (chaiaroon-2025). LinkedIn excluded (anti-scraping). Indeed Thailand replaced by confirmed Thai-specific platforms. **Data scale**: 1,000–2,000 postings per career path is realistic for Thai digital sector (tipsena-2025 benchmark). **Temporal drift**: credible signal horizon is 12 months (macedo-2022); collect postings from a bounded 12-month window. **Segment taxonomy**: chaiaroon-2025 provides a validated 20-role Thai digital taxonomy (.Net-dev, Back-end-dev, Business-analyst, Cloud, Data-analyst, Data-engineer, Database-admin, DevOps, Front-end-dev, Full-stack-dev, Information-security, IT-support, Java-dev, Mobile-dev, Network-engineer, Project-manager, Software-engineer, Tester, UX/UI-designer, Web-developer) — more specific than our original 10-15 sector list. **Visualisation**: heatmap (courses × skills) validated as primary view for non-technical academic stakeholders (ahadi-2022, hilliger-2022); multi-level output (programme summary + course drill-down) required. | (1) WangchanBERTa removed from extraction pipeline; replaced by LLM (gemma-4-31b-it) + USE. (2) KL divergence formally adopted as primary gap metric with market‖programme direction. (3) Job posting platform list updated to 4 confirmed Thai academic sources. (4) 12-month data window added as explicit constraint. (5) "Segment" concept clarified: career paths = role-level (20 categories from chaiaroon-2025); industry sectors = secondary enrichment layer. (6) Heatmap adopted as primary output visualisation with narrative summary. (7) RAG flagged for v2 extraction (zero-shot for v1). | 2026-04-29 |

---

## Go Decision

- [x] Problem statement is stable and evidence-grounded
- [x] Key hypotheses are validated or consciously accepted as risks
- [x] Gaps and opportunities from the literature are understood
- [x] Team is aligned on scope and direction

**Go decision made by:** Research Team  **Date:** 2026-04-29

**Summary of final idea (post-iteration):**

Iris is a skill gap analysis system that compares Thai academic programme skill profiles against market demand distributions and against each other.

**Data sources:** Programme skill profiles are extracted from TQF (มคอ.2) course descriptions using `gemma-4-31b-it` (multilingual LLM, zero-shot) with PyThaiNLP for Thai preprocessing. Market demand distributions are aggregated from 1,000–2,000 job postings per career path collected within a 12-month bounded window from four confirmed Thai platforms: Jobthai, Jobsdb, JOBBKK, and JOBTOPGUN.

**Skill representation:** Data-driven emergent vocabulary — skills are extracted bottom-up from the data, clustered using `text-embedding-embeddinggemma-300m` to handle semantic variation ("machine learning" ≈ "predictive modelling"), and optionally mapped post-hoc to ESCO for cross-context comparability. No fixed taxonomy is imposed at extraction time. Skill weights in gap reports use RCA (Revealed Comparative Advantage) to surface career-discriminating skills over generic common skills.

**Gap metrics:** Primary aggregate metric is KL divergence in the market‖programme direction (penalises skills the market demands that graduates lack). Programme-to-programme comparison uses set-based decomposition into common skills, A-unique, and B-unique skill sets.

**Career path taxonomy:** chaiaroon-2025 20-role Thai digital taxonomy (.Net-dev, Back-end-dev, Business-analyst, Cloud, Data-analyst, Data-engineer, Database-admin, DevOps, Front-end-dev, Full-stack-dev, Information-security, IT-support, Java-dev, Mobile-dev, Network-engineer, Project-manager, Software-engineer, Tester, UX/UI-designer, Web-developer). Industry sector (Finance, Healthcare, etc.) is a secondary enrichment layer only.

**Outputs:** Multi-level curriculum analytics report — programme-level heatmap (courses × skills) with narrative summary for academic administrators; course-level drill-down for curriculum designers. Free electives are handled via a scenario system (Core / Core + Electives / Hypothetical) enabling what-if curriculum planning.

**Known limitations accepted for v1:** Soft skills excluded (hard to extract reliably); free elective courses student-variable; temporal drift handled by static snapshot only (sliding window earmarked for v2); RAG-enhanced extraction earmarked for v2; segment inference reliability unvalidated (empirical resolution in Phase 4).

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
| WangchanBERTa removed from NLP pipeline; replaced by gemma-4-31b-it (extraction) + USE (embedding) | lertmethaphat-2025: WangchanBERTa produces 97.21% cosine similarity between Physician and Dentist — catastrophically fails to discriminate closely related domain terms, which is exactly what skill extraction requires | 2026-04-29 |
| KL divergence (market‖programme direction) adopted as primary aggregate gap metric | sabet-2024 validates asymmetric KL for curriculum gap; market‖programme direction penalises skills the market demands that graduates lack — the actionable direction for curriculum review | 2026-04-29 |
| RCA (Revealed Comparative Advantage) adopted for skill weighting in gap reports | ahadi-2022: RCA captures career-path specificity of a skill, not raw frequency — penalises common skills shared across all paths, rewards skills that discriminate one career path from another | 2026-04-29 |
| Job posting sources narrowed to 4 confirmed Thai platforms: Jobthai, Jobsdb, JOBBKK, JOBTOPGUN | chaiaroon-2025: top 5 platforms by Google Trends 2021; all 4 confirmed in Thai academic research; LinkedIn excluded (ToS / anti-scraping enforcement) | 2026-04-29 |
| 12-month bounded data collection window adopted as explicit constraint | macedo-2022: credible skill demand forecast horizon ≈ 12 months; technical skills volatile beyond this (cloud NRMSE 0.42 vs 24-month); v1 = static snapshot with documented collection date | 2026-04-29 |
| Career path taxonomy replaced by chaiaroon-2025 20-role Thai digital taxonomy | Empirically validated on 11,365 Thai job postings; replaces original 10–15 sector list; industry sectors (Finance, Healthcare, etc.) are secondary enrichment, not the primary comparison dimension | 2026-04-29 |
| Heatmap (courses × skills) + narrative summary adopted as primary output format | ahadi-2022: heatmap surfaces unexpected pathway alignments; hilliger-2022: administrators rated multi-level CA tool 76/100, faculty 85/100; narrative summary required for non-technical stakeholders who will not interpret raw matrices | 2026-04-29 |
| Multi-level output required: programme summary for administrators + course drill-down for curriculum designers | hilliger-2022: single-level output is insufficient — administrators need the aggregated programme view first before drilling into course-level detail; two levels serve both audiences with one tool | 2026-04-29 |
| RAG-based curriculum extraction earmarked for v2; zero-shot LLM (gemma-4-31b-it) for v1 | xu-2025: RAG outperforms zero-shot for curriculum extraction but requires a retrieval corpus; v1 uses zero-shot to reduce pipeline complexity; RAG is a validated upgrade path | 2026-04-29 |
| "Segment" concept split: career path (role-level, 20 chaiaroon categories) is primary; industry sector is secondary enrichment | Literature review revealed these are distinct dimensions — a Data Engineer role exists across Finance, Healthcare, and Manufacturing; role-level taxonomy is the primary curriculum gap dimension | 2026-04-29 |
