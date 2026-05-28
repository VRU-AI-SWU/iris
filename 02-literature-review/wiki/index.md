# Literature Review Wiki — Index · Iris (Skill Gap Analysis)

Knowledge graph for the Iris project: a skill-gap analysis system comparing skill
distributions from Thai TQF (มคอ.2) curricula against Thai labour-market job
postings, using NLP and agentic AI.

This wiki follows the lab literature-review methodology (`../.claude/instruction.md`).
Components: **papers/** (per-paper notes), **concepts/** (semantic nodes),
**questions/** (13 research-question notes → design decisions), and
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

## Questions (13)

| File | Status | Working answer |
|------|--------|----------------|
| [q-skill-taxonomy](questions/q-skill-taxonomy.md) | partial | Emergent vocabulary at extraction, post-hoc map to ESCO; evolve zero-shot → RAG as vocabulary grows. |
| [q-thai-ontology](questions/q-thai-ontology.md) | **answered** | No Thai skill ontology exists at needed granularity — a confirmed gap; justifies emergent vocabulary + ESCO mapping. |
| [q-thai-nlp](questions/q-thai-nlp.md) | partial | PyThaiNLP for preprocessing; multilingual LLM for extraction; USE for matching; avoid WangchanBERTa for fine-grained terms. |
| [q-implied-skills](questions/q-implied-skills.md) | partial | Few-shot LLM + RAG most promising; no benchmark for implied-skill extraction — define eval in Phase 4. |
| [q-sample-size](questions/q-sample-size.md) | partial | No published threshold; target ~1,000–2,000 postings/career path (vs tipsena ~4,900/segment); run convergence analysis. |
| [q-job-posting-sources](questions/q-job-posting-sources.md) | partial | JobThai, JobsDB, Indeed TH, JOBBKK, JOBTOPGUN confirmed in research; PDPA applies; LinkedIn supplementary only. |
| [q-temporal-drift](questions/q-temporal-drift.md) | partial | 12-month window; technical skills volatile, soft skills stable; sliding-window weighting for future live system. |
| [q-gap-direction](questions/q-gap-direction.md) | partial | Hybrid: KL divergence (market‖programme, asymmetric) for score + set-based gap for readable report. |
| [q-visualisation](questions/q-visualisation.md) | partial | Course×skill heatmap primary; narrative headline first; multi-level output; RCA-weighted ranking. |
| [q-segment-taxonomy](questions/q-segment-taxonomy.md) | partial | Adopt tipsena-2025 5-segment DEPA framework; career paths sit within segments. |
| [q-credit-weighting](questions/q-credit-weighting.md) | open | Deferred to Phase 4 empirical validation (no literature yet). |
| [q-segment-inference](questions/q-segment-inference.md) | open | Deferred to Phase 4 empirical validation (no literature yet). |
| [q-registry-lookup](questions/q-registry-lookup.md) | open | Deferred to Phase 4 empirical validation (no literature yet). |

---

## Concepts (8)

| File | Summary |
|------|---------|
| [curriculum-analytics](concepts/curriculum-analytics.md) | NLP/data analysis on programme documents to extract and compare delivered skills. |
| [esco-ontology](concepts/esco-ontology.md) | EU multilingual skills/occupations taxonomy (~13.9k skills); field-dominant reference, no Thai. |
| [kl-divergence](concepts/kl-divergence.md) | Asymmetric distributional distance; primary aggregate gap metric (market‖programme) and drift measure. |
| [rag-skill-extraction](concepts/rag-skill-extraction.md) | Retrieval-grounded LLM skill extraction; reduces hallucination vs zero-shot. |
| [skill-gap-quantification](concepts/skill-gap-quantification.md) | Measuring supply vs demand skill distributions (set diff, cosine, KL, chi-square). |
| [thai-nlp](concepts/thai-nlp.md) | Thai-language NLP challenges: no word boundaries, tonal, code-switching, low-resource. |
| [tpqi-framework](concepts/tpqi-framework.md) | Thailand's occupational-standards/competency system; coarser than a skill ontology. |
| [wangchanberta](concepts/wangchanberta.md) | SOTA Thai RoBERTa; strong on Thai tasks but conflates closely related fine-grained terms. |

---

## Key Cross-Cutting Findings for Design Decisions

1. **Extraction stack (Q3):** WangchanBERTa conflates closely related Thai terms (97.21% similarity Physician/Dentist; lertmethaphat-2025) — use PyThaiNLP for preprocessing, a multilingual LLM (gemma-4-31b-it) for extraction, and USE for embedding/matching; reserve WangchanBERTa away from fine-grained skill classification.
2. **Taxonomy (Q1, Q2):** No Thai skill ontology exists at the needed granularity — an emergent, data-driven vocabulary is validated; map post-hoc to ESCO for international comparability; evolve zero-shot extraction toward RAG as the vocabulary grows.
3. **Gap metric (Q10):** KL divergence (market‖programme) is the asymmetric aggregate score; set-based gap is the interpretable stakeholder output.
4. **Skill weighting:** RCA (revealed comparative advantage) surfaces career-path-specific skills better than raw frequency (ahadi-2022).
5. **Visualisation (Q9):** Course×skill heatmap + narrative headline + multi-level drill-down is the validated stakeholder format (ahadi-2022; hilliger-2022).
6. **Data (Q5, Q6, Q7):** JobThai/JobsDB/Indeed-TH/JOBBKK/JOBTOPGUN are research-confirmed sources; target ~1,000–2,000 postings/career path; 12-month window (technical skills go stale fast; macedo-2022).
7. **Segments (Q11):** Adopt the tipsena-2025 five-segment DEPA digital taxonomy; the chaiaroon-2025 20-role list refines career paths within it.
8. **Deferred to Phase 4 (Q8, Q12, Q13):** credit weighting, LLM segment inference reliability, and Thai registry (DBD/SET) lookups have no literature and are empirical-validation tasks.
