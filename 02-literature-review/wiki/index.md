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
>
> 🔄 **Second round 2026-08-28.** The review was re-run against the *new* questions.
> **11 papers added** across four themes the original round never searched: skill entity
> linking, out-of-KB (NIL) handling, proficiency-level inference, and Thai document
> extraction. See [Post-Pivot Round](#post-pivot-round-2026-08-28) at the end.

This wiki follows the lab literature-review methodology (`../.claude/instruction.md`).
Components: **papers/** (per-paper notes), **concepts/** (semantic nodes),
**questions/** (research-question notes → design decisions), and
**[literature_review/](literature_review/literature-review.md)** (the narrative
academic review with citations). Source provenance is in `../raw/manifest.md`.

---

## Papers (36)

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

### Skill Entity Linking (5) 🆕 *added 2026-08-28*

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [zhang-2024-job-market-entity-linking](papers/zhang-2024-job-market-entity-linking.md) | Zhang et al. | 2024 | Findings of EACL | High | First span-level skill EL to ESCO; **BLINK Acc@1 23.55%, Acc@32 48.98%** over 13,890 skills. The field's calibration point. |
| [arslan-2026-turkish-skill-extraction](papers/arslan-2026-turkish-skill-extraction.md) | Arslan İltüzer et al. | 2026 | arXiv | High | Low-resource, morphologically complex language; **0.56 end-to-end**; native-language extraction beats translation. Closest analogue to Thai. |
| [saroglou-2025-esco-eqf-linking](papers/saroglou-2025-esco-eqf-linking.md) | Saroglou et al. | 2025 | arXiv | High | Sentence vs Entity Linking to ESCO/EQF; EL Acc@1 **0.2881**; context helps; supervised beats decoder-only on ranking. |
| [dong-2023-out-of-kb-mention-discovery](papers/dong-2023-out-of-kb-mention-discovery.md) | Dong et al. | 2023 | CIKM | High | BLINKout: explicit NIL target beats thresholding; KB Versioning generates out-of-KB test data free. |
| [herandi-2024-skill-llm](papers/herandi-2024-skill-llm.md) | Herandi et al. | 2024 | arXiv | Low | Fine-tuned LLM for skill *extraction*; no linking, no accessible numbers. Not adopted. |

### Proficiency Level & Curriculum Mapping (3) 🆕 *added 2026-08-28*

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [kumar-2025-bloom-taxonomy-classification](papers/kumar-2025-bloom-taxonomy-classification.md) | Kumar et al. | 2025 | arXiv | High | ⚠️ **Zero-shot LLMs 0.72–0.73 vs SVM+augmentation 94%** on six-way Bloom classification. Argues against holistic LLM level judgement. |
| [zaki-2023-clo-plo-mapping-automation](papers/zaki-2023-clo-plo-mapping-automation.md) | Zaki et al. | 2023 | Educ. Inf. Technol. | High | Automating the CLO→PLO matrix: **83.1% / 88.1%** vs domain experts. The ● ○ matrix Iris reads is itself noisy. |
| [le-2026-competency-tagging-evidence](papers/le-2026-competency-tagging-evidence.md) | Le et al. | 2026 | arXiv | High | LLM as *constrained, evidence-producing tagger*; micro-F1 0.57, MRR 0.82. Closest published system to Iris's architecture. |

### Thai Document Extraction (2) 🆕 *added 2026-08-28*

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [nonesung-2026-typhoon-ocr](papers/nonesung-2026-typhoon-ocr.md) | Nonesung et al. | 2026 | arXiv | High | Thai-tuned 3B VLM: **Levenshtein 0.04 on Thai government forms** (GPT-4o 0.57). The fallback for lossy text layers. |
| [nonesung-2025-thaiocrbench](papers/nonesung-2025-thaiocrbench.md) | Nonesung et al. | 2025 | IJCNLP-AACL | Medium | 2,808 samples, 13 tasks; names hallucinated/missing diacritics, language bias, structural mismatch as Thai VLM failure modes. |

### Structure-Aware Retrieval (1) 🆕 *added 2026-08-28*

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [sarthi-2024-raptor](papers/sarthi-2024-raptor.md) | Sarthi et al. | 2024 | ICLR | Medium | Recursive clustering + summarisation tree; +20% on QuALITY. *Inferred* hierarchy — the contrast that justifies PageIndex's *declared* one. |

### Evaluation Method & Human Review (2) 🆕 *added 2026-08-28 by the process audit*

| File | Authors | Year | Venue | Relevance | Summary |
|------|---------|------|-------|-----------|---------|
| [passonneau-2006-masi-set-agreement](papers/passonneau-2006-masi-set-agreement.md) | Passonneau | 2006 | LREC | High | ⭐ MASI = Jaccard × monotonicity, as the distance inside Krippendorff's α. **Corrects the Sprint 4 IAA statistic** — the task is set-valued, so κ is wrong. |
| [chen-2025-interface-design-high-stakes](papers/chen-2025-interface-design-high-stakes.md) | Chen et al. | 2025 | arXiv (cs.HC) | High | 108 participants; **human+AI can underperform AI alone** under automation bias. Confidence/explanations help; forcing functions *hurt* performance. |

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

## Concepts (37)

| File | Summary |
|------|---------|
| [thailand-skill-mapping](concepts/thailand-skill-mapping.md) 🆕 | ⭐ The national standard — 4,376 skills, 3 graded levels each, 371 careers, open API. The foundation the project now stands on. |
| [skill-entity-linking](concepts/skill-entity-linking.md) 🆕 | Mapping free text to IDs in a fixed vocabulary. Iris's core research task after the pivot. |
| [proficiency-levels](concepts/proficiency-levels.md) 🆕 | Graded skill depth; the standard's criteria meet TQF's own ● ○ depth declarations. The novel contribution. |
| [thai-pdf-text-integrity](concepts/thai-pdf-text-integrity.md) 🆕 | Silent corruption of Thai marks in institutional PDFs, its diagnostic, and its repair. Text-layer corruption still unaddressed in the literature; vision-side diacritic loss now corroborated. |
| [nil-entity-linking](concepts/nil-entity-linking.md) 🆕 | Mentions with no correct entry in the vocabulary. Explicit NIL target beats thresholding. |
| [structure-aware-retrieval](concepts/structure-aware-retrieval.md) 🆕 | Indexing a long document by its structure. Inferred (RAPTOR) vs declared (PageIndex) hierarchies. |
| [curriculum-analytics](concepts/curriculum-analytics.md) | NLP/data analysis on programme documents to extract and compare delivered skills. |
| [rag-skill-extraction](concepts/rag-skill-extraction.md) | Retrieval-grounded LLM extraction; the standard's definitions now supply the corpus this needs. |
| [kl-divergence](concepts/kl-divergence.md) | Asymmetric distributional distance; demoted to a secondary metric — see q-prevalence-metrics. |
| [skill-gap-quantification](concepts/skill-gap-quantification.md) | Measuring supply vs demand skill distributions (set diff, cosine, KL, chi-square). |
| [thai-nlp](concepts/thai-nlp.md) | Thai NLP challenges: no word boundaries, tonal, code-switching, low-resource. |
| [esco-ontology](concepts/esco-ontology.md) | EU multilingual taxonomy (~13.9k skills); the field's reference, no Thai. Post-hoc mapping dropped. |
| [tpqi-framework](concepts/tpqi-framework.md) | Thailand's occupational-standards system; coarser than a skill ontology. |
| [wangchanberta](concepts/wangchanberta.md) | SOTA Thai RoBERTa; conflates closely related fine-grained terms. |

### Backlog cleared 2026-08-28 (21 nodes)

Concepts that papers referenced but which had never been created — 65 dangling wikilinks.
Each is written with its post-pivot status stated, so the graph records what the design
kept and what it dropped.

| File | Summary | Post-pivot status |
|------|---------|-------------------|
| [skill-taxonomy](concepts/skill-taxonomy.md) | Enumerated skill sets with stable IDs; ESCO 13,890 · O*NET ~2,000 · Thai standard 4,376. Dixon: 775 suffices at national scale. | **live** |
| [skill-ontology](concepts/skill-ontology.md) | A taxonomy plus relations. ⚠️ The Thai standard is flat — no parent/child, so graph constraints have no analogue. | **live (gap)** |
| [onet-taxonomy](concepts/onet-taxonomy.md) | US Detailed Work Activities; the taxonomy behind sabet-2024's 3M-syllabus atlas. | considered, not used |
| [skill-normalisation](concepts/skill-normalisation.md) | Collapsing surface forms to a canonical entry — what linking makes unnecessary. | subsumed |
| [skill-decomposition](concepts/skill-decomposition.md) | Resolving granularity mismatch between text and taxonomy. | handled by retrieval breadth |
| [skill-extraction](concepts/skill-extraction.md) | Open-vocabulary skill strings from text. | ⛔ **was the core task; replaced by linking** |
| [llm-skill-extraction](concepts/llm-skill-extraction.md) | Prompted LLMs for skill work; the more constrained, the better it performs. | **live** |
| [zero-shot-prompting](concepts/zero-shot-prompting.md) | ⚠️ Loses every controlled comparison in the corpus. Bloom: 0.72–0.73 vs SVM 94%. | ⛔ **reversed; ablation baseline only** |
| [few-shot-prompting](concepts/few-shot-prompting.md) | Dynamic few-shot is the best Turkish configuration; needs a labelled pool. | post-gate option |
| [deep-learning-ner](concepts/deep-learning-ner.md) | Supervised sequence labelling; needs thousands of Thai labels that do not exist. | not viable |
| [job-posting-analysis](concepts/job-posting-analysis.md) | Postings as a demand corpus. ⚠️ Iris now inherits these biases second-hand without controlling them. | ⛔ **closed; biases still apply** |
| [thai-job-market](concepts/thai-job-market.md) | Thai role taxonomies, platforms, and the confirmed skill mismatch. | motivates; superseded as data |
| [temporal-drift](concepts/temporal-drift.md) | Demand decay; 12-month horizon, technical skills volatile. | **threat → signal** (`growth`) |
| [cosine-similarity](concepts/cosine-similarity.md) | Angle between vectors; retrieval scoring. | retrieval only, **not** a gap metric |
| [sentence-embedding](concepts/sentence-embedding.md) | Dense text vectors; discrimination matters more than benchmark rank. | **live** |
| [thai-bert](concepts/thai-bert.md) | ⚠️ 97.21% similarity Physician/Dentist — cannot separate near-identical Thai terms. | ⛔ **excluded from retrieval** |
| [roberta-architecture](concepts/roberta-architecture.md) | The pretraining recipe behind WangchanBERTa; overfits on small sets. | background |
| [sentence-piece-tokenization](concepts/sentence-piece-tokenization.md) | Subword vocabulary without word boundaries; suggests a second corruption diagnostic. | inherited |
| [thai-tokenization](concepts/thai-tokenization.md) | No spaces between Thai words; segmentation is ambiguous and runs *after* the integrity gate. | **live** |
| [pythainlp](concepts/pythainlp.md) | The Thai toolkit — used for `ำ` restoration and lexical retrieval, not as stage one. | **live** |
| [bibliometric-analysis](concepts/bibliometric-analysis.md) | Quantitative mapping of a research field; cannot surface unpublished government standards. | framing |

### Added by the process audit (2 nodes)

| File | Summary | Post-pivot status |
|------|---------|-------------------|
| [inter-annotator-agreement](concepts/inter-annotator-agreement.md) 🆕 | The precondition for any gold standard. For set-valued tasks the **distance function**, not the coefficient, is what matters. | **live — corrects Sprint 4** |
| [automation-bias](concepts/automation-bias.md) 🆕 | Accepting model output without scrutiny; why "add a human" is a design problem, not a solution. | **live — governs the review screen** |

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
12. **Expected linking accuracy:** 🆕 *(2026-08-28)* Three independent studies put strict
    top-1 skill linking at **0.23–0.29** and end-to-end pipelines near **0.56**. All report
    ranking far ahead of selection (Acc@32 ≈ 2× Acc@1; MRR 0.82 vs F1 0.57). **The human
    review screen is required, not optional.**
13. **Level inference method:** 🆕 *(2026-08-28)* Zero-shot LLM Bloom classification scores
    0.72–0.73 against 94% for SVM+augmentation — derive level from the document's declared
    signals, and include a non-LLM verb-feature baseline in the ablation.
14. **Thai OCR fallback exists:** 🆕 *(2026-08-28)* A self-hostable 3B Thai VLM reaches
    Levenshtein 0.04 on Thai government forms. The "no OCR needed" conclusion holds only for
    *substitution* damage; lossy documents get a vision path, flagged in provenance.

---

## Post-Pivot Round (2026-08-28)

The first review round (April 2026) answered the questions of a design that no longer
exists. This round targeted the questions the pivot created.

**Searched, and new to the corpus:**

| Theme | Why it was never searched before | Papers added |
|---|---|---|
| Skill entity linking | The old design had no fixed vocabulary to link *to* | 5 |
| Proficiency level & curriculum mapping | The old design was binary presence/absence | 3 |
| Thai document extraction | The old design assumed PDF text extraction just works | 2 |
| Structure-aware retrieval | The old design used regex over flat text | 1 |

**Deliberately not re-searched:** job-posting sources, sample size, industry segmentation,
company-registry lookup — all closed by the pivot (see the *Closed by the pivot* table).

**Confirmed gaps — nothing found, and the absence is itself a finding:**

- **No NLP work on Thai TQF (มคอ.) documents.** Searching for it returns TQF policy
  documents and framework descriptions, not computational work. Iris appears to be first.
- **No paper on PDF text-layer corruption in Thai.** The vision-side literature documents
  diacritic loss; nothing addresses a text layer that extracts cleanly and is silently wrong.
- **No work grading curriculum skill depth against a published competency scale.** Confirmed
  a second time, now against the 2025–26 literature.

**What changed as a result:** [[q-out-of-vocabulary]] method settled (explicit NIL target,
not thresholding); [[q-level-inference]] gained a ruled-out approach and a required
baseline; [[q-thai-nlp]] gained a controlled result on native-language extraction and a
vision fallback; [[q-implied-skills]] gained the numbers that justify the review screen.
The `thai-pdf-text-integrity` policy changed from two outcomes to three.


---

## Traceability Audit (2026-08-28)

The first two rounds asked *"what does the literature say?"*. This one asked
**"does every design element have evidence behind it?"** — tracing each method component in
`03-solution-design/` back to a paper, and flagging what has none.

### Design element → evidence

| Design element | Evidence | Status |
|---|---|---|
| Fixed national vocabulary as the linking target | dixon-2023 (775 skills suffice), senger-2024 | ✅ supported |
| Retrieve-then-adjudicate | zhang-2024, arslan-2026, le-2026, xu-2025 | ✅ strong |
| Evidence spans on every link | le-2026 (also *outperforms* unconstrained prompting) | ✅ supported |
| Out-of-vocabulary as an explicit target | dong-2023 (BLINKout) | ✅ supported |
| Level from CLO verbs, not LLM judgement | kumar-2025 (0.72–0.73 vs 94%) | ✅ supported |
| ● ○ matrix treated as noisy evidence | zaki-2023 (83–88% vs experts) | ✅ supported |
| Vision fallback for lossy text layers | nonesung-2026, nonesung-2025 | ✅ supported |
| Declared- over inferred-structure indexing | sarthi-2024 (by contrast) | ✅ supported |
| No vector database at 4,376 entries | — *(engineering, not a research claim)* | ➖ n/a |
| **Review screen as a method requirement** | zhang-2024 et al. establish it is *necessary* | ⚠️ **was one-sided** → chen-2025 shows it is not *sufficient* |
| **IAA on a set-valued annotation task** | none — κ would have been used by default | 🔴 **error** → passonneau-2006 (MASI) |
| **RCA denominator** | ahadi-2022 uses RCA; never stated which denominator | 🔴 **underspecified** → measured: top-15 overlap 8/15 |
| **Seniority gradient** | none found | 🆕 **no precedent — a contribution claim** |
| Thai PDF integrity gate | none found (2nd round) | 🆕 confirmed novelty |
| Level grading of curricula | none found (2nd round) | 🆕 confirmed novelty |
| NLP on Thai TQF documents | none found (2nd round) | 🆕 confirmed novelty |

### What the audit found

**Two design errors that the literature corrects.**

1. **The Sprint 4 agreement statistic was wrong.** The plan permits multiple correct links
   per course, which makes annotation **set-valued**; the default choice would have been
   Cohen's or Fleiss' κ, which scores `{A,B}` against `{A,B,C}` as total disagreement.
   Since that subset pattern is the *expected* disagreement between a strict and a generous
   annotator, κ would have systematically understated agreement and discredited a sound
   evaluation. → Krippendorff's α with the MASI distance
   ([[passonneau-2006-masi-set-agreement]]).

2. **The review screen was justified one-sidedly.** Measured linking accuracy establishes
   that review is *necessary*; nothing established that it *works*.
   [[chen-2025-interface-design-high-stakes]] shows human+AI pairs can underperform the AI
   alone under [[automation-bias]], that confidence displays and text explanations help,
   and that **cognitive forcing functions reduced performance** — which is what
   confidence-first sorting and disagreement display resemble. Kept, for different stated
   reasons, and now instrumented.

**One underspecification measured rather than argued.** "RCA weighting" never said which
global denominator. Career-equal and count-weighted give median |ΔRCA| = 3.02, max 23.86,
and a **top-15 ranking overlap of 8/15** — on the very list a curriculum committee is shown.
Career-equal adopted, because count-weighting inherits the unresolved meaning of `N`.

**A fourth confirmed novelty.** Searches for empirical work measuring skill-demand shifts
across seniority rungs returned industry guidance and CV self-presentation studies
(Azamnouri et al. 2026: *"seniority nearly triples the odds of articulating leadership"* —
about candidates describing themselves, not about demand). **No precedent was found for the
seniority gradient**, which makes it a contribution rather than an application.

**Eighteen broken graph edges.** Papers were added to question nodes without the reverse
link, so `questions:` frontmatter was wrong for 18 pairs and the graph was unusable from
the paper side. Repaired; one orphan paper (januzaj-2022) also linked. **0 one-way edges,
0 orphans, 0 dangling wikilinks.**

### Process rules added to the methodology

- **Verify bidirectional links.** Adding a paper to a question is not done until the paper
  declares the question (§9 step 4). A one-way edge is a silent graph defect.
- **Audit design → evidence, not only question → paper.** A question node can look
  well-supported while a *design decision* derived from it has no evidence at all — which
  is how both errors above survived two review rounds.
- **Search for every new method element before building it.** The seniority gradient and
  the MASI issue both entered the design *after* the review rounds, and neither would have
  been checked without an explicit pass.
