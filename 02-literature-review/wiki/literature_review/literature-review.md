# Literature Review — Iris: Skill Gap Analysis for Thai Curricula

> Narrative synthesis of the 23 papers in `wiki/papers/`, organised around the
> project's 13 research questions (`wiki/questions/`). Inline citations are
> `(Author Year)` hyperlinked to their paper note; full entries are in the
> References. This document is regenerated as papers are added.

---

## 1. Introduction

Iris quantifies the gap between the skills a Thai academic programme teaches —
extracted from TQF (มคอ.2) curriculum documents — and the skills the Thai labour
market demands, read from job postings. Realising this requires settling four
clusters of questions the literature can inform: how to extract skills from
Thai-language text, what vocabulary to express them in, how to measure the gap
and present it to academic stakeholders, and how to source and time-bound the
labour-market data. This review synthesises the evidence behind each decision and
marks where the literature runs out and Phase 4 empirical work must take over.

---

## 2. Skill Extraction and the Thai NLP Stack

The extraction stack is the project's highest-risk technical choice, and the
single most consequential finding is a negative one. ([Lertmethaphat 2025](../papers/lertmethaphat-2025-thai-job-market-nlp.md))
shows that WangchanBERTa — the state-of-the-art Thai transformer of
([Lowphansirikul 2021](../papers/lowphansirikul-2021-wangchanberta.md)) — fails to
discriminate closely related Thai job titles, reporting 97.21% similarity between
"Physician" and "Dentist", while a Universal Sentence Encoder with XGBoost reaches
~90% classification accuracy. Because skill terms such as "data analysis", "data
engineering", and "data science" are exactly this kind of near-neighbour, the
review concludes WangchanBERTa should not be the standalone classifier for
fine-grained skills. The resulting pipeline uses PyThaiNLP
([Phatthiyaphaibun 2023](../papers/phatthiyaphaibun-2023-pythainlp.md)) for
preprocessing (tokenisation and segmentation — non-trivial in a language without
word boundaries), a multilingual LLM for extraction, and USE-style sentence
embeddings for matching.

For extraction quality, the curriculum-analytics literature favours grounded,
exemplar-driven prompting over zero-shot. ([Xu 2025](../papers/xu-2025-llm-curricular-analytics.md))
evaluates LLMs on course-to-skill extraction and finds retrieval-augmented
generation, grounded in a skill knowledge base, outperforms zero-shot while
handling brief and abstract course descriptions well; ([Luyen 2025](../papers/luyen-2025-skill-decomposition-ontology.md))
shows few-shot prompting lets an LLM decompose high-level skills to a consistent
granularity and infer sub-skills. These bear directly on the "implied skills"
problem (a "Database Systems" course implies SQL and normalisation without naming
them): few-shot LLM extraction plus RAG over a growing vocabulary is the most
promising route, though ([Senger 2024](../papers/senger-2024-dl-skill-extraction-survey.md))
notes the field lacks consensus on what even counts as an implied versus explicit
skill, so an evaluation rubric must be defined before extraction quality can be
measured. For CS/IT specifically, ([Vo 2022](../papers/vo-2022-nlp-curriculum-learning-path.md))
demonstrates that domain-specific NER fine-tuning beats general models — a useful
fallback if LLM extraction proves unreliable on formal Thai.

---

## 3. Skill Taxonomy and the Thai Ontology Gap

What vocabulary should the extracted skills live in? The field's default is ESCO,
dominant across the survey of ([Senger 2024](../papers/senger-2024-dl-skill-extraction-survey.md))
and operationalised by ([Kavargyris 2025](../papers/kavargyris-2025-escox-skill-extraction.md)),
whose ESCOX pipeline pairs an LLM with ESCO embeddings and provides a useful
cross-check (its top extracted software-engineering skills are Java, SQL, DevOps,
Python, Agile). But fixed taxonomies miss emerging and context-specific skills —
a limitation ([Sabet 2024](../papers/sabet-2024-course-skill-atlas.md)) flags even
while using O*NET DWAs at national scale, and ([Dixon 2023](../papers/dixon-2023-occupational-models-42m.md))
shows a bounded vocabulary (775 skills) is nonetheless sufficient to model 42
million US postings. Iris's emergent-vocabulary approach is thus well supported:
let skills surface from the data, then map post-hoc to ESCO for international
comparability, evolving extraction from zero-shot toward RAG as the vocabulary
grows.

The decisive Thai-context finding is that **no Thai skill ontology exists at the
needed granularity**. The TQF defines five broad learning-outcome domains, not
skills; the TPQI occupational-standards framework is coarser than a skill
taxonomy and not machine-readable as an ontology; and ICDL (adopted by TPQI for
ICT) covers digital literacy, not software engineering. The Thai studies confirm
this indirectly: ([Weerasombat 2025](../papers/weerasombat-2025-thai-employer-skill-priorities.md))
establishes a Thai skill mismatch but only in broad categories,
([Phaphuangwittayakul 2018](../papers/phaphuangwittayakul-2018-thai-skill-demand-jobthai.md))
uses keyword matching rather than an ontology, and ([Chaiaroon 2025](../papers/chaiaroon-2025-thai-digital-workforce-matching.md))
defines 20 digital job categories with no underlying skill ontology. This gap is
both a justification for the emergent approach and a publishable contribution; the
TPQI ICT standards may later serve as a partial validation layer, not an
extraction target.

---

## 4. Quantifying and Weighting the Gap

For the aggregate gap score, KL divergence is the validated choice.
([Sabet 2024](../papers/sabet-2024-course-skill-atlas.md)) uses it to measure both
the curriculum-to-market gap and temporal drift between snapshots, and its
asymmetry is exactly right for Iris: KL(market‖programme) ≠ KL(programme‖market),
and the market is the reference distribution, consistent with the directional
framing ([Senger 2024](../papers/senger-2024-dl-skill-extraction-survey.md)) notes
is standard in the field. The recommendation is a hybrid: KL divergence for the
single-number score and a set-based gap (which in-demand skills are absent from
the programme) for the human-readable report, since non-technical stakeholders
need the interpretable form. An open refinement is partial matching — "machine
learning" in a programme versus "deep learning" in the market — which a set-based
gap misses but embedding cosine similarity would capture. On weighting,
([Ahadi 2022](../papers/ahadi-2022-skills-taught-vs-sought.md)) shows revealed
comparative advantage (RCA) surfaces career-path-specific skills better than raw
frequency, which over-represents generic skills — so gap rankings should be
RCA-weighted.

---

## 5. Curriculum Analytics and Stakeholder Visualisation

A gap analysis is only useful if administrators act on it, and two curriculum-
analytics studies converge on the format. Both ([Ahadi 2022](../papers/ahadi-2022-skills-taught-vs-sought.md))
and ([Hilliger 2022](../papers/hilliger-2022-curriculum-analytics-tool.md)) center
on a course×skill heatmap, which shows the multi-course, multi-skill gap landscape
at a glance. ([Hilliger 2022](../papers/hilliger-2022-curriculum-analytics-tool.md))
adds two lessons from deploying a real tool: multi-level reporting (programme
summary for administrators, course drill-down for faculty) is what turns a
curiosity into decision support, and administrators are harder to design for than
faculty — so reports should lead with a plain-language headline ("your programme
is missing 3 of the top 10 Data Science skills") before any chart. The broader
framing that a measurable curriculum-to-market gap exists and matters is
established by ([Aljohani 2022](../papers/aljohani-2022-curriculum-skill-gap-bibliometric.md))
and the Industry 4.0 review of ([Rikala 2024](../papers/rikala-2024-skill-gaps-industry40-review.md));
([Januzaj 2022](../papers/januzaj-2022-cosine-similarity-he-job-market.md)) offers a
simple cosine-on-common-words baseline that Iris should be able to beat.

---

## 6. Thai Labour-Market Data: Sources, Sample Size, and Temporal Drift

The market side of the gap depends on sourcing Thai postings ethically. Academic
precedent confirms several platforms: ([Phaphuangwittayakul 2018](../papers/phaphuangwittayakul-2018-thai-skill-demand-jobthai.md))
scrapes JobThai and JobsDB; ([Chaiaroon 2025](../papers/chaiaroon-2025-thai-digital-workforce-matching.md))
adds JOBBKK and JOBTOPGUN; ([Tipsena 2025](../papers/tipsena-2025-predicting-thai-digital-workforce.md))
draws 24,494 positions from ten platforms over 2023–2024. Thailand's PDPA applies,
but company names and job requirements are generally not personal data; LinkedIn
is treated as supplementary given its anti-scraping stance. On sample size, the
literature gives no published convergence threshold: US national scale implies
~48K postings per occupation code ([Dixon 2023](../papers/dixon-2023-occupational-models-42m.md)),
which is not transferable, while the most realistic Thai benchmark is
([Tipsena 2025](../papers/tipsena-2025-predicting-thai-digital-workforce.md))'s
~4,900 postings per segment — leading to a working target of ~1,000–2,000 postings
per career path, to be validated by a Phase 4 convergence analysis (a genuine
methodological gap for small labour markets).

Time-bounding matters because demand shifts. ([Macedo 2022](../papers/macedo-2022-skills-demand-forecasting-temporal.md))
establishes a credible forecast horizon of roughly 12 months, beyond which error
grows sharply, and ([Fettach 2025](../papers/fettach-2025-skill-demand-temporal-kg.md))
shows soft skills are temporally stable while technical skills are volatile.
Iris v1 therefore collects a bounded 12-month snapshot, reports its date
explicitly, and flags technical-skill gaps as higher-urgency. A future live
system should adopt the sliding-window weighted average of
([Seif 2024](../papers/seif-2024-dynamic-jobs-skills-kg.md))'s dynamic jobs-skills
knowledge graph, which downweights older signals on a 6–12 month rolling window.

---

## 7. Industry Segmentation

To break demand down by sector, the strongest Thai precedent is
([Tipsena 2025](../papers/tipsena-2025-predicting-thai-digital-workforce.md))'s
five-segment digital-economy taxonomy (hardware/smart devices, software/software
services, digital services, digital content, telecommunications), drawn from
Thailand's DEPA policy framework — coarse enough for sufficient data per segment.
([Chaiaroon 2025](../papers/chaiaroon-2025-thai-digital-workforce-matching.md))'s
20 digital job categories refine career paths *within* those segments, and
([Siddoo 2019](../papers/siddoo-2019-thai-digital-workforce-competency.md))'s
three functional competency categories serve as a skill-level validation layer
rather than a segment scheme. The reliability of LLM-based segment inference from
job-description text (needed for agency postings that hide the employer) and of
Thai company-registry lookups (DBD, SET) for the enrichment pipeline have **no
supporting literature** and are deferred to Phase 4 empirical validation, as is
the question of whether course credit hours should weight skill contribution.

---

## 8. Synthesis

The literature settles most of Iris's design. Skills are extracted with PyThaiNLP
preprocessing, a multilingual LLM, and USE-style matching — explicitly avoiding
WangchanBERTa for fine-grained terms ([Lertmethaphat 2025](../papers/lertmethaphat-2025-thai-job-market-nlp.md))
— with RAG and few-shot prompting to capture implied skills ([Xu 2025](../papers/xu-2025-llm-curricular-analytics.md); [Luyen 2025](../papers/luyen-2025-skill-decomposition-ontology.md)).
Because no Thai skill ontology exists, the vocabulary is emergent and mapped
post-hoc to ESCO ([Senger 2024](../papers/senger-2024-dl-skill-extraction-survey.md); [Kavargyris 2025](../papers/kavargyris-2025-escox-skill-extraction.md)).
The gap is scored with asymmetric KL divergence and reported as an RCA-weighted
set-based gap ([Sabet 2024](../papers/sabet-2024-course-skill-atlas.md); [Ahadi 2022](../papers/ahadi-2022-skills-taught-vs-sought.md)),
presented as a course×skill heatmap with a narrative headline and multi-level
drill-down ([Hilliger 2022](../papers/hilliger-2022-curriculum-analytics-tool.md)).
Market data comes from research-confirmed Thai platforms over a 12-month window
([Tipsena 2025](../papers/tipsena-2025-predicting-thai-digital-workforce.md); [Macedo 2022](../papers/macedo-2022-skills-demand-forecasting-temporal.md)),
segmented by the DEPA five-segment scheme. Three questions — credit weighting,
LLM segment-inference reliability, and Thai registry lookups — have no literature
and are carried into Phase 4 as empirical-validation tasks. Each conclusion is
recorded in its `wiki/questions/` note and feeds the Phase 3 design and Phase 4
implementation.

---

## References

Author-date citations above resolve to this list; the full author list and
detailed findings live in each `wiki/papers/` note.

1. Ahadi A. et al. (2022). *Skills Taught vs Skills Sought: Using Skills Analytics to Identify the Gaps between Curriculum and Job Markets.* EDM 2022 (poster). — [note](../papers/ahadi-2022-skills-taught-vs-sought.md)
2. Aljohani N.R. et al. (2022). *Bridging the skill gap between the acquired university curriculum and the requirements of the job market.* Journal of Innovation & Knowledge. https://doi.org/10.1016/j.jik.2022.100190 — [note](../papers/aljohani-2022-curriculum-skill-gap-bibliometric.md)
3. Chaiaroon P. et al. (2025). *Digital Workforce Matching: A Machine Learning Approach for Skill-Based Job Classification and Recommendation.* J. Current Science and Technology. https://doi.org/10.59796/jcst.V15N4.2025.137 — [note](../papers/chaiaroon-2025-thai-digital-workforce-matching.md)
4. Dixon N. et al. (2023). *Occupational models from 42 million unstructured job postings.* Patterns. https://doi.org/10.1016/j.patter.2023.100757 — [note](../papers/dixon-2023-occupational-models-42m.md)
5. Fettach Y. et al. (2025). *Skill Demand Forecasting Using Temporal Knowledge Graph Embeddings.* arXiv:2504.07233. https://arxiv.org/abs/2504.07233 — [note](../papers/fettach-2025-skill-demand-temporal-kg.md)
6. Hilliger I. et al. (2022). *Lessons learned from designing a curriculum analytics tool for improving student learning and program quality.* Journal of Computing in Higher Education. https://doi.org/10.1007/s12528-021-09284-2 — [note](../papers/hilliger-2022-curriculum-analytics-tool.md)
7. Januzaj Y. & Luma A. (2022). *Cosine Similarity – A Computing Approach to Match Similarity Between Higher Education Programs and Job Market Demands.* iJET 17(12). https://doi.org/10.3991/ijet.v17i12.30375 — [note](../papers/januzaj-2022-cosine-similarity-he-job-market.md)
8. Kavargyris D.C. et al. (2025). *ESCOX: A tool for skill and occupation extraction using LLMs from unstructured text.* Software Impacts. https://doi.org/10.1016/j.simpa.2025.100772 — [note](../papers/kavargyris-2025-escox-skill-extraction.md)
9. Lertmethaphat N.N. et al. (2025). *Exploring the Thai Job Market Through the Lens of Natural Language Processing and Machine Learning.* PIER Discussion Paper 228. https://www.pier.or.th/dp/228/ — [note](../papers/lertmethaphat-2025-thai-job-market-nlp.md)
10. Lowphansirikul L. et al. (2021). *WangchanBERTa: Pretraining transformer-based Thai Language Models.* arXiv:2101.09635. https://doi.org/10.48550/arXiv.2101.09635 — [note](../papers/lowphansirikul-2021-wangchanberta.md)
11. Luyen L.N. & Abel M.-H. (2025). *Automated Skill Decomposition Meets Expert Ontologies: Bridging the Granularity Gap with LLMs.* arXiv:2510.11313. https://doi.org/10.48550/arXiv.2510.11313 — [note](../papers/luyen-2025-skill-decomposition-ontology.md)
12. Macedo M.M.G. de et al. (2022). *Practical Skills Demand Forecasting via Representation Learning of Temporal Dynamics.* arXiv:2205.09508. https://arxiv.org/abs/2205.09508 — [note](../papers/macedo-2022-skills-demand-forecasting-temporal.md)
13. Phaphuangwittayakul A. et al. (2018). *Analysis of Skill Demand in Thai Labor Market from Online Jobs Recruitment Websites.* JCSSE 2018 (IEEE). https://doi.org/10.1109/JCSSE.2018.8457393 — [note](../papers/phaphuangwittayakul-2018-thai-skill-demand-jobthai.md)
14. Phatthiyaphaibun W. et al. (2023). *PyThaiNLP: Thai Natural Language Processing in Python.* NLP-OSS @ EMNLP. https://arxiv.org/abs/2312.04649 — [note](../papers/phatthiyaphaibun-2023-pythainlp.md)
15. Rikala P. et al. (2024). *Understanding and measuring skill gaps in Industry 4.0 — A review.* Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2024.123206 — [note](../papers/rikala-2024-skill-gaps-industry40-review.md)
16. Sabet A.J. et al. (2024). *Course-Skill Atlas: A national longitudinal dataset of skills taught in U.S. higher education curricula.* Nature Scientific Data. https://doi.org/10.1038/s41597-024-03931-8 — [note](../papers/sabet-2024-course-skill-atlas.md)
17. Seif A. et al. (2024). *A Dynamic Jobs-Skills Knowledge Graph.* RecSys in HR 2024 (CEUR Vol-3788). — [note](../papers/seif-2024-dynamic-jobs-skills-kg.md)
18. Senger E. et al. (2024). *Deep Learning-based Computational Job Market Analysis: A Survey on Skill Extraction and Classification from Job Postings.* NLP4HR @ EACL. https://doi.org/10.48550/arXiv.2402.05617 — [note](../papers/senger-2024-dl-skill-extraction-survey.md)
19. Siddoo V. et al. (2019). *An exploratory study of digital workforce competency in Thailand.* Heliyon. https://doi.org/10.1016/j.heliyon.2019.e01723 — [note](../papers/siddoo-2019-thai-digital-workforce-competency.md)
20. Tipsena R. et al. (2025). *Predicting Workforce Needs in Thailand's Digital Industry: A Machine Learning Approach (2023-2024).* JISTaP 13(3). https://doi.org/10.1633/JISTaP.2025.13.3.1 — [note](../papers/tipsena-2025-predicting-thai-digital-workforce.md)
21. Vo N.N.Y. et al. (2022). *Domain-specific NLP system to support learning path and curriculum design at tech universities.* Computers and Education: Artificial Intelligence. https://doi.org/10.1016/j.caeai.2021.100042 — [note](../papers/vo-2022-nlp-curriculum-learning-path.md)
22. Weerasombat T. & Pumipatyothin P. (2025). *Employers' priority on work skills and the skill gaps: a case of Thailand.* Cogent Education. https://doi.org/10.1080/2331186X.2024.2441656 — [note](../papers/weerasombat-2025-thai-employer-skill-priorities.md)
23. Xu Z. et al. (2025). *From Course to Skill: Evaluating LLM Performance in Curricular Analytics.* arXiv:2505.02324. https://doi.org/10.48550/arXiv.2505.02324 — [note](../papers/xu-2025-llm-curricular-analytics.md)
