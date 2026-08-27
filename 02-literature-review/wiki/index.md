# Literature Review Wiki — Index · Iris (Curriculum Skill Alignment)

Knowledge graph for the Iris project: expressing a Thai TQF (มคอ.2) curriculum in the
vocabulary of the **national Thailand Skill Mapping standard** (สป.อว. / KMITL), and
measuring level-aware alignment against the skill demand that standard publishes.

> ⚠️ **Pivot 2026-08-27.** This review was conducted for a design that built its own
> skill vocabulary by clustering, and measured demand by scraping Thai job boards. A
> national skill standard published in July 2025 supersedes both. Papers are unchanged and
> mostly *more* relevant; **question nodes carry status banners** — five are closed or
> superseded, five revised, three new. Start with [[thailand-skill-mapping]] and
> [[q-thai-ontology]], whose answer reversed.

This wiki follows the lab literature-review methodology (`../.claude/instruction.md`).
Components: **papers/** (per-paper notes), **concepts/** (semantic nodes),
**questions/** (research-question notes → design decisions), and
**[literature_review/](literature_review/literature-review.md)** (the narrative
academic review with citations). Source provenance is in `../raw/manifest.md`.

---

## Papers (23)

### Skill Extraction, Taxonomy & Ontology (7)

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [sabet-2024-course-skill-atlas](papers/sabet-2024-course-skill-atlas.md) | Sabet et al. | 2024 | Nature Sci Data | High | National longitudinal Course-Skill Atlas from 3M+ US syllabi; O*NET DWA taxonomy; KL divergence for curriculum↔market drift. |
| [senger-2024-dl-skill-extraction-survey](papers/senger-2024-dl-skill-extraction-survey.md) | Senger et al. | 2024 | NLP4HR @ EACL | High | Survey of DL skill extraction/classification; ESCO dominant; terminology inconsistency a known field problem. |
| [kavargyris-2025-escox-skill-extraction](papers/kavargyris-2025-escox-skill-extraction.md) | Kavargyris et al. | 2025 | Software Impacts | High | ESCOX: LLM + ESCO-embedding skill/occupation extraction; top SE skills Java/SQL/DevOps/Python/Agile. |
| [luyen-2025-skill-decomposition-ontology](papers/luyen-2025-skill-decomposition-ontology.md) | Luyen & Abel | 2025 | arXiv | Medium | LLM skill decomposition aligned to expert ontologies; few-shot prompting closes the granularity gap. |
| [xu-2025-llm-curricular-analytics](papers/xu-2025-llm-curricular-analytics.md) | Xu et al. | 2025 | arXiv (cs.CY) | High | Evaluates LLMs for course→skill extraction; RAG grounded in a skill base beats zero-shot; handles brief/abstract docs. |
| [dixon-2023-occupational-models-42m](papers/dixon-2023-occupational-models-42m.md) | Dixon et al. | 2023 | Patterns | High | Occupational models from 42M postings; a bounded 775-skill vocabulary suffices at US national scale. |
| [vo-2022-nlp-curriculum-learning-path](papers/vo-2022-nlp-curriculum-learning-path.md) | Vo et al. | 2022 | Computers & Education: AI | High | CSIT-NER: domain-specific BERT fine-tuning beats general BERT for CS/IT skill NER in curriculum text. |

### Thai NLP & Language Models (2)

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [lowphansirikul-2021-wangchanberta](papers/lowphansirikul-2021-wangchanberta.md) | Lowphansirikul et al. | 2021 | arXiv (cs.CL) | High | WangchanBERTa: SOTA Thai RoBERTa; beats mBERT/XLM-R on Thai tasks. |
| [phatthiyaphaibun-2023-pythainlp](papers/phatthiyaphaibun-2023-pythainlp.md) | Phatthiyaphaibun et al. | 2023 | NLP-OSS @ EMNLP | Medium | PyThaiNLP: standard Thai toolkit for tokenisation/segmentation/preprocessing. |

### Thai Labour Market & Digital Workforce (6)

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [phaphuangwittayakul-2018-thai-skill-demand-jobthai](papers/phaphuangwittayakul-2018-thai-skill-demand-jobthai.md) | Phaphuangwittayakul et al. | 2018 | JCSSE (IEEE) | High | Thai skill-demand analysis from JobThai/JobsDB via scraping + keyword matching. |
| [lertmethaphat-2025-thai-job-market-nlp](papers/lertmethaphat-2025-thai-job-market-nlp.md) | Lertmethaphat et al. | 2025 | PIER DP 228 | High | WangchanBERTa fails on closely related Thai job titles (97% sim Physician/Dentist); USE+XGBoost (~90%) wins. |
| [chaiaroon-2025-thai-digital-workforce-matching](papers/chaiaroon-2025-thai-digital-workforce-matching.md) | Chaiaroon et al. | 2025 | JCST | High | ML skill-based job classification; 20-category Thai digital job taxonomy. |
| [tipsena-2025-predicting-thai-digital-workforce](papers/tipsena-2025-predicting-thai-digital-workforce.md) | Tipsena et al. | 2025 | JISTaP | High | 24,494 Thai digital positions from 10 platforms (2023–24); 5-segment DEPA taxonomy. |
| [siddoo-2019-thai-digital-workforce-competency](papers/siddoo-2019-thai-digital-workforce-competency.md) | Siddoo et al. | 2019 | Heliyon | High | EFA-derived 3-category Thai digital competency taxonomy. |
| [weerasombat-2025-thai-employer-skill-priorities](papers/weerasombat-2025-thai-employer-skill-priorities.md) | Weerasombat & Pumipatyothin | 2025 | Cogent Education | Medium | Confirms a Thai skill mismatch using broad employer-priority categories. |

### Curriculum Analytics & Skill Gap (5)

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [ahadi-2022-skills-taught-vs-sought](papers/ahadi-2022-skills-taught-vs-sought.md) | Ahadi et al. | 2022 | EDM | High | Course×occupation heatmap with RCA weighting validated for academic stakeholders. |
| [hilliger-2022-curriculum-analytics-tool](papers/hilliger-2022-curriculum-analytics-tool.md) | Hilliger et al. | 2022 | J. Computing in HE | High | Multi-level CA reporting (student/course/program); administrators hardest to design for. |
| [aljohani-2022-curriculum-skill-gap-bibliometric](papers/aljohani-2022-curriculum-skill-gap-bibliometric.md) | Aljohani et al. | 2022 | J. Innovation & Knowledge | Medium | Data-driven bibliometric framing of the curriculum↔job-market skill gap. |
| [januzaj-2022-cosine-similarity-he-job-market](papers/januzaj-2022-cosine-similarity-he-job-market.md) | Januzaj & Luma | 2022 | iJET | Low | Cosine similarity on common words to match HE programmes to job-market demand. |
| [rikala-2024-skill-gaps-industry40-review](papers/rikala-2024-skill-gaps-industry40-review.md) | Rikala et al. | 2024 | Tech. Forecasting & Social Change | Medium | Review of how Industry 4.0 skill gaps are defined and measured. |

### Temporal Skill Demand (3)

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [macedo-2022-skills-demand-forecasting-temporal](papers/macedo-2022-skills-demand-forecasting-temporal.md) | Garcia de Macedo et al. | 2022 | arXiv | High | LSTM/GRU skill-demand forecasting; credible horizon ≈ 12 months. |
| [fettach-2025-skill-demand-temporal-kg](papers/fettach-2025-skill-demand-temporal-kg.md) | Fettach et al. | 2025 | arXiv | Medium | Temporal KG embeddings; soft skills stable, technical skills volatile. |
| [seif-2024-dynamic-jobs-skills-kg](papers/seif-2024-dynamic-jobs-skills-kg.md) | Seif et al. | 2024 | RecSys in HR | High | Singapore dynamic jobs-skills KG; sliding-window weighted averages. |

---

## Questions (16)

Status key: **answered** · **open** (live) · **revised** (answer changed by the pivot) ·
**superseded** / **closed** (no longer applicable — retained for provenance).

### Live

| File | Status | Working answer |
|------|--------|----------------|
| [q-skill-taxonomy](questions/q-skill-taxonomy.md) | **answered** | Adopt the national standard as a controlled vocabulary; the task becomes entity linking, not extraction + clustering. |
| [q-thai-ontology](questions/q-thai-ontology.md) | **answered** ⚠️ reversed | A Thai skill vocabulary at the needed granularity **does** now exist — Thailand Skill Mapping, 4,376 skills with graded levels. |
| [q-level-inference](questions/q-level-inference.md) | open 🆕 | No literature grades curriculum depth against a competency scale. Combine CLOs, the ● ○ curriculum map, and curriculum position; report disagreement. |
| [q-out-of-vocabulary](questions/q-out-of-vocabulary.md) | open 🆕 | Record skills outside the standard separately, never score them; the residue becomes coverage feedback upstream. |
| [q-prevalence-metrics](questions/q-prevalence-metrics.md) | open 🆕 | Demand is prevalence, not a distribution. Primary metric: level-aware coverage gap, RCA-weighted. KL only after explicit renormalisation. |
| [q-implied-skills](questions/q-implied-skills.md) | revised | Now measurable as **recall in skill entity linking** — the central quantity of the Sprint 4 evaluation gate. |
| [q-thai-nlp](questions/q-thai-nlp.md) | revised | Answer holds, but a **text-layer integrity gate must run first** — real มคอ.2 text layers are silently corrupted. |
| [q-gap-direction](questions/q-gap-direction.md) | revised | Directional argument survives; the distributional assumption does not. Superseded on metrics by q-prevalence-metrics. |
| [q-temporal-drift](questions/q-temporal-drift.md) | revised | Drift becomes a *signal*: the standard publishes per-skill growth rates per career. |
| [q-visualisation](questions/q-visualisation.md) | revised | Heatmap still primary, now level-shaded; truncation must never render as a confirmed zero. |
| [q-credit-weighting](questions/q-credit-weighting.md) | open | Still empirical; now interacts with level inference. |

### Closed by the pivot

| File | Status | Why |
|------|--------|-----|
| [q-job-posting-sources](questions/q-job-posting-sources.md) | closed | Iris no longer collects job postings. |
| [q-sample-size](questions/q-sample-size.md) | closed | Sample size is not ours to choose; small-`N` careers are now a data-quality filter. |
| [q-segment-taxonomy](questions/q-segment-taxonomy.md) | superseded | Replaced by the standard's 5 industries → 371 careers. |
| [q-segment-inference](questions/q-segment-inference.md) | closed | Careers arrive pre-classified. |
| [q-registry-lookup](questions/q-registry-lookup.md) | closed | No employers are processed. |

---

## Concepts (12)

| File | Summary |
|------|---------|
| [thailand-skill-mapping](concepts/thailand-skill-mapping.md) 🆕 | ⭐ The national standard — 4,376 skills, 3 graded levels each, 371 careers, open API. The foundation the project now stands on. |
| [skill-entity-linking](concepts/skill-entity-linking.md) 🆕 | Mapping free text to IDs in a fixed vocabulary. Iris's core research task after the pivot. |
| [proficiency-levels](concepts/proficiency-levels.md) 🆕 | Graded skill depth; the standard's criteria meet TQF's own ● ○ depth declarations. The novel contribution. |
| [thai-pdf-text-integrity](concepts/thai-pdf-text-integrity.md) 🆕 | Silent corruption of Thai marks in institutional PDFs, its diagnostic, and its repair. Unaddressed in the literature. |
| [curriculum-analytics](concepts/curriculum-analytics.md) | NLP/data analysis on programme documents to extract and compare delivered skills. |
| [rag-skill-extraction](concepts/rag-skill-extraction.md) | Retrieval-grounded LLM extraction; the standard's definitions now supply the corpus this needs. |
| [kl-divergence](concepts/kl-divergence.md) | Asymmetric distributional distance; demoted to a secondary metric — see q-prevalence-metrics. |
| [skill-gap-quantification](concepts/skill-gap-quantification.md) | Measuring supply vs demand skill distributions (set diff, cosine, KL, chi-square). |
| [thai-nlp](concepts/thai-nlp.md) | Thai NLP challenges: no word boundaries, tonal, code-switching, low-resource. |
| [esco-ontology](concepts/esco-ontology.md) | EU multilingual taxonomy (~13.9k skills); the field's reference, no Thai. Post-hoc mapping dropped. |
| [tpqi-framework](concepts/tpqi-framework.md) | Thailand's occupational-standards system; coarser than a skill ontology. |
| [wangchanberta](concepts/wangchanberta.md) | SOTA Thai RoBERTa; conflates closely related fine-grained terms. |

---

## Key Cross-Cutting Findings for Design Decisions

*Rewritten 2026-08-27 for the pivot. Findings 1, 4, 5 survive unchanged from the original
review; the rest were replaced by the adoption of the national standard.*

1. **Extraction stack (Q3):** WangchanBERTa conflates closely related Thai terms (97.21 %
   similarity Physician/Dentist; lertmethaphat-2025) — use PyThaiNLP for preprocessing and
   a multilingual LLM for adjudication; keep WangchanBERTa away from fine-grained skill
   work. *Unchanged.*
2. **Vocabulary (Q1, Q2):** ⚠️ **Reversed.** A Thai national skill vocabulary now exists
   (thailand-skill-mapping, 4,376 skills with graded levels). Emergent vocabulary,
   clustering, and post-hoc ESCO mapping are all dropped. The task is entity linking.
3. **Method:** RAG over the standard's 4,376 definitions and 6,058 level criteria —
   the corpus xu-2025 showed beats zero-shot, and which the earlier design lacked.
4. **Skill weighting:** RCA surfaces career-specific skills better than raw frequency
   (ahadi-2022). *Unchanged, but must be redefined on prevalence.*
5. **Visualisation (Q9):** Heatmap + narrative headline + multi-level drill-down is the
   validated stakeholder format (ahadi-2022; hilliger-2022). *Unchanged*, now level-shaded.
6. **Metrics (Q10):** ⚠️ Demand is **prevalence**, not a distribution, and is truncated at
   ~100 skills per career. Primary metric is a level-aware coverage gap; KL is secondary
   and only after explicit renormalisation.
7. **Data (Q5, Q6, Q7):** ⛔ No longer applicable — demand is published, not collected.
8. **Segments (Q11):** ⛔ Superseded by the standard's 5 industries → 371 careers.
9. **Level-awareness:** 🆕 No reviewed work grades curriculum skill depth against a
   competency scale — all are binary presence. This is the project's novel contribution.
10. **Thai PDF integrity:** 🆕 Real มคอ.2 text layers are silently corrupted, and the
    literature does not address it. A diagnostic gate is mandatory before any NLP.
11. **Method gap for the lab:** 🆕 A literature search did not surface a government
    open-data standard that had existed for nine months. Infrastructure questions need
    ministry and open-data portals searched directly, not only journals.
