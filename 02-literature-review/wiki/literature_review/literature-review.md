# Literature Review — Iris: Skill Gap Analysis for Thai Curricula

<!-- lang-switch -->
**English** · [ภาษาไทย](literature-review.th.md)

> Narrative synthesis of the 23 papers in `wiki/papers/`, organised around the
> project's 13 research questions (`wiki/questions/`). Inline citations are
> `(Author Year)` hyperlinked to their paper note; full entries are in the
> References. This document is regenerated as papers are added.

> ## ⚠️ Addendum — the 2026-08-27 pivot
>
> This review was written in April 2026 and its synthesis (§8) drove the Phase 3 design.
> On 2026-08-27 the project pivoted to align with the **Thailand Skill Mapping** national
> standard (สป.อว. / KMITL, published July 2025), which supersedes two of the four
> question clusters named in §1.
>
> **The evidence in §§2–7 is unchanged and remains correct.** What changed is the world it
> describes: §3 concludes that no Thai skill ontology exists at the needed granularity —
> true when written, false now. §6 and §7 concern sourcing labour-market data, which the
> project no longer does.
>
> Read §§2–7 as the record of how the design was reasoned to, then
> **[§9](#9-addendum-realignment-to-the-national-standard-2026-08-27)** for what the
> standard changes and which papers become *more* load-bearing as a result, then
> **[§10](#10-second-round-evidence-for-the-new-questions-2026-08-28)** for the eleven
> papers added in the second review round, which supply the performance expectations the
> project must plan against, and
> **[§11](#11-process-audit--evidence-for-the-methods-own-machinery-2026-08-28)** for the
> audit that traced each design element back to its evidence and found two errors in the
> project's own evaluation machinery.

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

---

## 9. Addendum — realignment to the national standard (2026-08-27)

### 9.1 What was published, and why the review missed it

In July 2025 the Office of the Permanent Secretary, MHESI (สป.อว.) published **Thailand
Skill Mapping**, developed by KMITL: 4,376 Thai skills, each with a Thai definition and
three graded proficiency levels with written criteria, mapped to 371 careers across five
industries, served over an open API. It is national reference data, not an academic
artefact.

§3 of this review concluded — correctly on the evidence available — that no Thai skill
ontology existed at the granularity Iris needs, and that conclusion justified the emergent
vocabulary approach. The standard had existed for nine months when this review was
written. It was missed because the search was conducted over **peer-reviewed literature**,
and the standard has no accompanying paper describing the database. Ministry publications
and government open-data portals were not searched.

That is a methodological lesson worth carrying into the lab's review procedure: for
questions of the form *does this dataset, ontology, or registry exist?*, a literature
search is structurally incapable of returning the answer.

⚠️ **A citation hazard for anyone writing this up.** The paper most easily found when
searching for Thai skill mapping — Anmanatarkul et al. (2025), on learning modules and
skills mapping for the electric-vehicle industry — is from **KMUTT**, and describes a
Delphi expert-consensus skill map with seven skill groups. It is a legitimate precedent
for linking curricula to careers through skill mapping, but it is **not** the
KMITL/สป.อว. database and must not be cited as if it were.

### 9.2 The task changes from extraction to entity linking

§2 and §3 framed the problem as extracting skill terms from Thai text and organising them
into a vocabulary. With a fixed vocabulary the problem becomes **skill entity linking**:
mapping course-description text to IDs in a controlled set.

This is a better-posed research task. Open extraction produces surface strings that must
be normalised before they can be scored, and the normalisation is itself contested;
linking against a fixed vocabulary makes precision and recall directly computable against
expert annotation, and makes results reproducible across runs and across research groups.

The papers this review already collected become the direct methodological template rather
than a loose analogy. [ESCOX](../papers/kavargyris-2025-escox-skill-extraction.md)
(Kavargyris et al. 2025) is the closest published system — an LLM combined with taxonomy
embeddings, linking text to ESCO — and Iris is structurally the same pipeline against the
Thai standard. [Senger et al. (2024)](../papers/senger-2024-dl-skill-extraction-survey.md)
document that ESCO-linked approaches dominate the field precisely because open extraction
suffers terminology inconsistency. [Dixon et al. (2023)](../papers/dixon-2023-occupational-models-42m.md)
show a bounded 775-skill vocabulary suffices at US national scale, which makes 4,376 a
comfortable size rather than a constraint.

Most consequentially, [Xu et al. (2025)](../papers/xu-2025-llm-curricular-analytics.md)
found RAG grounded in a skill knowledge base outperforms zero-shot extraction for
course→skill work, especially on brief or abstract course descriptions. The Phase 3 design
acknowledged this and chose zero-shot anyway, on the explicit grounds that RAG "requires a
retrieval corpus not yet available". **That corpus now exists**: 4,376 skill definitions
and 6,058 level criteria. The approach the literature recommended is available on the
evidence that recommended it.

### 9.3 Level-awareness: where the literature runs out

Every curriculum-analytics system reviewed here treats a skill as **present or absent** in
a course. [Sabet et al. (2024)](../papers/sabet-2024-course-skill-atlas.md) build a
national Course-Skill Atlas from three million syllabi as a binary course × O*NET-DWA
matrix. [Ahadi et al. (2022)](../papers/ahadi-2022-skills-taught-vs-sought.md) present
course × occupation heatmaps with RCA weighting — again binary occupancy, weighted by
market specificity rather than by depth. None grades how deeply a course develops a skill.

The standard makes grading possible from one side: every skill carries `ระดับพื้นฐาน`,
`ระดับปานกลาง`, and `ระดับสูง` with explicit criteria. The Thai TQF format supplies the
other side, and does so under regulation — programmes must publish a
**แผนที่แสดงการกระจายความรับผิดชอบ** marking each course × learning-outcome pair as
● *ความรับผิดชอบหลัก* or ○ *ความรับผิดชอบรอง*, and newer outcome-based documents state
course learning outcomes per course. Both were verified present in the SWU มคอ.2.

Joining them turns the research question from *does this programme teach X?* into *to what
level, and is that the level the career requires?* No reviewed work asks it, and the
combination that permits it — a national standard publishing graded criteria alongside a
national curriculum format requiring depth declarations — appears specific to the Thai
context. This is the project's novel contribution, and its open problems are recorded in
[q-level-inference](../questions/q-level-inference.md).

### 9.4 Metrics: prevalence is not a distribution

§4 adopted KL divergence in the market‖programme direction, following
[Sabet et al. (2024)](../papers/sabet-2024-course-skill-atlas.md). That paper computes it
over syllabus-derived skill *distributions*. The national standard does not publish a
distribution: within a career, `count / percentage` is constant, so `percentage` is the
share of that career's postings mentioning a skill — a prevalence. Percentages across a
career sum to between roughly 45 % and 3,596 %.

KL divergence is therefore not directly applicable. It remains available after
renormalising counts into shares, but then measures "share of all skill mentions", which
is not the quantity a curriculum committee needs and not what §4 argued for.

A second constraint compounds this: the published demand vector is **truncated at
approximately 100 skills per career**. Any divergence computed over it is taken across an
incomplete support, and — more importantly for the writing — **absence from the vector
means below the cut-off, never not demanded**.

The directional argument of §4 survives entirely: administrators need to know what
graduates lack, not what they have in excess. What changes is the vehicle. The primary
metric becomes a level-aware coverage gap computed on prevalence and weighted by RCA
[(Ahadi et al. 2022)](../papers/ahadi-2022-skills-taught-vs-sought.md), with KL retained as
a secondary aggregate reported only alongside its changed interpretation. See
[q-prevalence-metrics](../questions/q-prevalence-metrics.md).

One capability is gained rather than lost. §6 treated temporal drift as a threat to
validity, since a single scrape goes stale —
[Garcia de Macedo et al. (2022)](../papers/macedo-2022-skills-demand-forecasting-temporal.md)
put the credible horizon at about twelve months, and
[Fettach et al. (2025)](../papers/fettach-2025-skill-demand-temporal-kg.md) show technical
skills are the volatile ones. The standard publishes a per-skill **growth rate** per
career. Drift becomes a measurable signal, and the review's finding about which skills
move tells us how to read it.

### 9.5 What the literature does not cover at all

Neither the Thai NLP literature nor the PDF-mining literature addresses a problem that
blocks the pipeline outright: **Thai text extracted from institutional PDFs is silently
corrupted**.

Measured on two real มคอ.2 documents, one retains 1 % of its karan (`์`) and 14 % of its
mai tho (`้`), the marks having been substituted by ASCII glyphs through a WinAnsi font
encoding; the other has lost every `ำ` in the document. Both extract without error and
return plausible-looking Thai. PyMuPDF and poppler produce identical output, so this is a
property of the documents, not the tooling.

Thai NLP papers, including [PyThaiNLP](../papers/phatthiyaphaibun-2023-pythainlp.md)
(Phatthiyaphaibun et al. 2023), assume correct input text. PDF-extraction work does not
address Thai mark stacking. Since a missing karan turns `คอมพิวเตอร์` into `คอมพิวเตอร`
and degrades every downstream match against a correctly-spelled vocabulary, and since the
corruption is invisible, a pipeline without a detection stage would produce confident
wrong results.

The diagnostic developed for Iris — Thai combining-mark rate per 1,000 Thai characters,
compared per-mark against a clean-document baseline — and the deterministic repair that
follows from the damage being substitution rather than deletion, are therefore a small
methodological contribution in their own right, reusable by anyone mining Thai
institutional documents. See [thai-pdf-text-integrity](../concepts/thai-pdf-text-integrity.md).

### 9.6 Revised synthesis

| §8 conclusion | After the pivot |
|---|---|
| Emergent vocabulary; post-hoc ESCO mapping | ⛔ National standard as controlled vocabulary; ESCO dropped |
| Zero-shot extraction (RAG deferred — no corpus) | ✅ RAG, on the corpus the standard provides |
| KL divergence (market‖programme) primary | ⚠️ Level-aware coverage gap on prevalence; KL secondary, renormalised |
| RCA weighting | ✅ Retained, redefined on prevalence |
| Heatmap + narrative + drill-down | ✅ Retained, level-shaded |
| Four Thai job platforms, 12-month window | ⛔ No collection; demand is published |
| chaiaroon-2025 20-role taxonomy | ⛔ Standard's 138 digital careers |
| PyThaiNLP preprocessing | ✅ Retained — preceded by an integrity gate |
| *(not considered)* | 🆕 Proficiency-level inference from TQF's own ● ○ and CLO declarations |
| *(not considered)* | 🆕 Thai PDF text-layer integrity |

Three questions the literature cannot answer now sit at the centre of Phase 4: how
reliably a proficiency level can be inferred from a TQF document
([q-level-inference](../questions/q-level-inference.md)); what proportion of an academic
curriculum falls outside a labour-market-derived vocabulary, and what to do with it
([q-out-of-vocabulary](../questions/q-out-of-vocabulary.md)); and which alignment metrics
are valid on truncated prevalence data
([q-prevalence-metrics](../questions/q-prevalence-metrics.md)).

Two further questions are not empirical but institutional, and block the methods section
until สป.อว./KMITL answer them: what corpus underlies the demand counts — per-career
posting totals range from 203 to 6,291,725, which is not plausible for Thailand alone —
and whether the ~100-skill cap is a display limit or a data limit.

---

---

## 10. Second round — evidence for the new questions (2026-08-28)

The April 2026 round answered the questions of a design that no longer exists. This round
searched four themes the original never touched, because the original had no reason to:
skill entity linking, out-of-knowledge-base handling, proficiency-level inference, and Thai
document extraction. Eleven papers were added. Three findings matter more than the rest.

### 10.1 What accuracy to expect, and what follows from it

The single most useful result of this round is a number the project did not have.

[Zhang et al. (2024)](../papers/zhang-2024-job-market-entity-linking.md) conducted the first
span-level skill entity-linking study, mapping mentions in job advertisements to ESCO's
13,890 skills. Training on 123,619 synthetic mention–skill pairs and evaluating on 1,824
human-annotated instances, their bi-encoder reached **Acc@1 of 23.55%**, rising to 48.98% at
Acc@32; the autoregressive alternative reached 11.48% at rank one.
[Saroglou et al. (2025)](../papers/saroglou-2025-esco-eqf-linking.md), working on ESCO and
EQF with different data and a different architecture, report Entity Linking
**Accuracy@1 of 0.2881**. [Arslan İltüzer et al. (2026)](../papers/arslan-2026-turkish-skill-extraction.md),
in Turkish, report a best **end-to-end score of 0.56**, and
[Le et al. (2026)](../papers/le-2026-competency-tagging-evidence.md), tagging learning
resources against a competency framework, report **micro-F1 0.57**.

Four studies, four languages, three taxonomies, four research groups, converging on the same
range. Strict top-1 linking against a large occupational vocabulary is a hard problem that
nobody solves well, and any expectation that Iris will do so is unsupported.

The second regularity is more actionable than the first. Every one of these papers reports
that **ranking is substantially better than selection**: Acc@32 roughly doubles Acc@1 in
Zhang et al.; Le et al. report MRR 0.82 against micro-F1 0.57. The correct answer is
usually retrieved and then discarded at the decision step. That is an argument for a
generous retrieval depth, and a much stronger argument for something the product design had
justified only from stakeholder reasoning: **a human review screen between the linker and
any published claim**. At these accuracy levels an unreviewed automated mapping is not
evidence, and the literature now says so in numbers.

Two qualifications keep this honest. Iris's candidate space is 4,376 entries against ESCO's
13,890, and its input is a whole course description rather than a job-posting span —
Saroglou et al. find precisely that sentence context helps, which is why their Sentence
Linking outperformed Entity Linking. There are grounds to expect better than 0.23–0.29. But
Iris's numbers will not be directly comparable to any of these, and the write-up must say so
rather than borrowing their difficulty as an excuse or their scale as a claim.

Zhang et al. also flag an evaluation trap Iris would otherwise have walked into: they score
against exactly one gold ESCO title per mention, which underestimates performance wherever
several links are legitimately valid. A course develops several related skills. Iris's
annotation protocol must permit multiple correct links per span.

### 10.2 How to infer a level, and how not to

[Kumar et al. (2025)](../papers/kumar-2025-bloom-taxonomy-classification.md) compared
classical models, RNNs, transformers and frontier LLMs on the same Bloom's-taxonomy
classification data — 600 learning outcomes across six cognitive levels. **SVM with data
augmentation reached 94% accuracy. Zero-shot LLMs reached 0.72–0.73.** RNNs and BERT
overfitted badly; RoBERTa degraded during training.

This measures the approach Iris might casually have taken — asking a language model what
level a course teaches a skill at — and finds it more than twenty points behind a classical
classifier. The feature the SVM exploits is Bloom's cognitive verbs, and Thai TQF course
learning outcomes follow the same convention: `อธิบาย` (explain) sits low, `ออกแบบ` (design)
sits high. The design's decision to derive level from the document's own declared signals is
therefore not merely more traceable, it is likely more accurate — and the Sprint 4 ablation
must include a non-LLM verb-feature baseline, because on this evidence it may win.

[Zaki et al. (2023)](../papers/zaki-2023-clo-plo-mapping-automation.md) supply a caution no
other source in the corpus does. They automate construction of the CLO→PLO matrix and
validate against domain experts, reaching **83.1% and 88.1% precision** on two programmes —
differing by five points purely on how the outcomes were written. Iris reads that matrix
rather than generating it: in Thai TQF it is **แผนที่แสดงการกระจายความรับผิดชอบ**, with
● ความรับผิดชอบหลัก and ○ ความรับผิดชอบรอง marking each course × outcome pair. It is a
required, regulated artefact — and it is hand-authored for accreditation, with its own noise
and its own incentives. Iris is inferring level partly from a signal that is not gold. The
design's decision to combine it with CLO text and curriculum position, and to **record
disagreement between sources rather than resolve it**, is the correct response; this is the
citation for why it is necessary. The five-point swing between two programmes at one
institution is also a warning about cross-institution comparability that belongs in the
limitations of any comparison result.

Both papers omit inter-annotator agreement on their gold labels. For a judgement as
contested as cognitive level, that omission is serious, and Iris's protocol reporting it is a
small methodological improvement worth claiming.

### 10.3 The architecture, independently arrived at

[Le et al. (2026)](../papers/le-2026-competency-tagging-evidence.md) — from the same group as
[Luyen and Abel (2025)](../papers/luyen-2025-skill-decomposition-ontology.md) — describe a
pipeline that segments learning resources, retrieves candidate competencies with BM25 and
graph-enriched profiles, has an LLM select from those candidates **and return the evidence
span justifying each selection**, then applies graph constraints to suppress inconsistent
tags. It outperforms zero-shot and few-shot LLM variants, retrieval-only baselines, and
supervised classifiers.

That is, component for component, the architecture Iris specified — including the evidence
span, which Iris had justified only on the grounds that a curriculum committee will
challenge specific assignments and the tool must answer immediately. Le et al. show the
constrained, evidence-producing formulation is not merely more auditable but *more
accurate* than unconstrained prompting. Their scores must be read carefully: micro-F1 0.57
over **22 competencies** is an optimistic bound, not a target for a system facing 4,376.

[Arslan İltüzer et al. (2026)](../papers/arslan-2026-turkish-skill-extraction.md) settle a
question §2 could only argue about. Facing a morphologically complex, low-resource language
with neither a skill taxonomy nor a dataset — Thai's position before the national standard —
they compare native-language extraction against translate-to-English-first and find
**native-language wins**. Their best pipeline is embedding retrieval followed by LLM
re-ranking, and it beats supervised sequence labelling. Iris's bilingual channel is
therefore a cross-check where an English course description exists, never a substitute for
the Thai one.

Where Iris departs is the fixed-vocabulary blind spot.
[Dong et al. (2023)](../papers/dong-2023-out-of-kb-mention-discovery.md) name it: mentions
with no correct entry in the knowledge base. Their BLINKout models this as an **explicit NIL
prediction target** rather than a similarity threshold, and beats threshold- and
feature-based methods across five datasets and three knowledge bases. This settles the
implementation question in [§9](#9-addendum-realignment-to-the-national-standard-2026-08-27)
and [q-out-of-vocabulary](../questions/q-out-of-vocabulary.md): a curriculum teaches theory
of computation, research method, and ethics that no job advertisement describes, and mapping
those to the nearest labour-market skill would be confidently wrong. Two of their techniques
transfer at no cost — synonym enhancement, since the standard ships a Thai title, an English
title and a Thai definition for every skill; and KB Versioning, which generates out-of-KB
test cases by holding out part of the vocabulary, adding an evaluation to Sprint 4 for the
price of a script.

### 10.4 A correction to the Thai-PDF conclusion

[§9.5](#95-what-the-literature-does-not-cover-at-all) concluded that no OCR was needed, on
the grounds that the damage measured in the SWU document is glyph substitution rather than
deletion. That holds for substitution damage and the repair table remains the right answer
there — deterministic, auditable, free.

It was wrong as a general rule. The KU document's collapse of every `ำ` into `า` is
genuinely lossy, and the stated fallback — request a better source file — is not always
available. [Nonesung et al. (2026)](../papers/nonesung-2026-typhoon-ocr.md) provide the
alternative: a Thai-tuned open vision-language model that reaches **BLEU 0.93 and Levenshtein
0.04 on Thai government forms**, against GPT-4o at 0.25 / 0.57 and Gemini 2.5 Flash at
0.74 / 0.15. It is 3B parameters, self-hostable alongside the adjudication model, and
consistent with the project's local-inference premise. Notably the 3B matches or beats their
own 7B on several categories — capability here comes from Thai-specific training data, not
scale.

The ingestion gate therefore has three outcomes rather than two: *clean* uses the text
layer, *repairable* applies the glyph repair table, and *lossy or unusable* re-extracts with
a vision model — with the document flagged as vision-derived, because a model output is not
a faithful reading and any finding traced to it should say so.

[Nonesung et al. (2025)](../papers/nonesung-2025-thaiocrbench.md) confirm at benchmark scale
what the two-document study found: across 2,808 samples and 13 tasks, Thai vision-language
performance is limited by "Thai diacritics, small fonts, headless Thai scripts", with
**hallucinated or missing diacritics** named as a systematic failure alongside language bias
and structural mismatch. Two independent routes to the same vulnerability. The practical
consequence is that the integrity gate must run **after** the vision path too, and that a
Thai-character-proportion check is needed to catch the language-bias failure that a
diacritic-rate diagnostic would miss. Their finding of structural mismatch in tables also
argues for extracting the ● / ○ curriculum-mapping marks from PDF glyph coordinates rather
than asking a vision model to read the table.

Finally, [Sarthi et al. (2024)](../papers/sarthi-2024-raptor.md) supply the reference point
for structure-aware retrieval, reporting a 20% absolute accuracy gain on QuALITY by building
a tree of recursively clustered and summarised chunks. The contrast is what matters for
Iris: RAPTOR *infers* a hierarchy by clustering, while a มคอ.2 already *declares* one under
regulation. An inferred hierarchy would be strictly worse and would not carry the page
ranges Iris uses for provenance — and RAPTOR's own limitation, that summarisation "can
discard fine-grained details", is disqualifying for a task that must recover every course
description. The deeper constraint applies to both and was already recorded: these systems
retrieve the *most relevant* node, whereas Iris needs exhaustive enumeration. Structure
indexing locates the section; extraction within it stays deterministic.

### 10.5 What was searched for and not found

Three gaps were confirmed rather than closed, and each is a claim the project can make.

**No computational work on Thai TQF documents.** Searching returns TQF policy documents and
framework descriptions, not NLP. Iris appears to be the first system to parse มคอ.2 at scale.

**No literature on PDF text-layer corruption in Thai.** The vision-side literature documents
diacritic failure; nothing addresses a text layer that extracts without error and is silently
wrong. The diagnostic in [thai-pdf-text-integrity](../concepts/thai-pdf-text-integrity.md)
remains an original contribution.

**No work grading curriculum skill depth against a published competency scale.** Confirmed a
second time against the 2025–26 literature. Every curriculum-analytics system reviewed —
including the three added this round — treats a skill as present or absent.


---

## 11. Process audit — evidence for the method's own machinery (2026-08-28)

The first two rounds asked what the literature says about the *problem*. This one asked
whether every element of the *solution* has evidence behind it — tracing each method
component back to a paper and flagging what had none. Two things turned out to be resting
on nothing, and both are corrected by literature that already existed.

### 11.1 The agreement statistic was wrong

The Sprint 4 gate commits to two independent annotators over a stratified course sample,
and — on [Zhang et al.'s (2024)](../papers/zhang-2024-job-market-entity-linking.md) warning
that single-gold scoring understates performance — to permitting **multiple correct links
per course**. That decision, taken to make the evaluation fairer, quietly changed the
annotation task from categorical to **set-valued**: each annotator returns a *set* of
national skill IDs per course.

Nothing in the plan said which agreement coefficient to use, and the default would have
been Cohen's or Fleiss' κ. On a set-valued task those compare sets for exact identity, so
one annotator's `{SQL, Data Modeling}` against another's
`{SQL, Data Modeling, Database Design}` counts as complete disagreement — indistinguishable
from `{SQL, Data Modeling}` against `{Ethics, Public Speaking}`. Since a subset relation is
precisely the disagreement one expects between a strict and a generous annotator, κ would
have understated agreement systematically, and a low reported reliability would then have
discredited an evaluation that was in fact sound.

[Passonneau (2006)](../papers/passonneau-2006-masi-set-agreement.md) solved this two
decades ago. **MASI = J × M** multiplies the Jaccard coefficient by a *monotonicity* term
that scores identical sets 1, a subset relation **2/3**, a partial overlap with non-null
differences **1/3**, and disjoint sets 0; used as the distance function δ inside
Krippendorff's α, it makes partial agreement measurable. On the paper's worked example an
annotation matrix in a subset relation scores 0.37 against 0.22 for one with symmetric
differences — a distinction exact-match agreement cannot express.

Iris adopts Krippendorff's α with MASI for both the skill-set annotation and the level
assignment. The monotonicity term is the load-bearing part: it separates *"one annotator
was more generous"* from *"the annotators disagree about what this course teaches"*, and
the annotation guideline should be tuned against exactly that distinction.

One limitation carries through and belongs in the write-up. MASI has no semantic distance,
so `การสร้างแบบจำลองข้อมูลเชิงสัมพันธ์` and `การสร้างแบบจำลองข้อมูลเชิงตรรกะ` are as far
apart as any two entries. On a fine-grained vocabulary this measures agreement
conservatively.

It is worth noting that the two papers closest to Iris's evaluation —
[Kumar et al. (2025)](../papers/kumar-2025-bloom-taxonomy-classification.md) and
[Zaki et al. (2023)](../papers/zaki-2023-clo-plo-mapping-automation.md) — both report model
performance against expert labels **without reporting agreement between the experts**. Zaki
et al.'s 83–88% precision "against domain experts" cannot be interpreted without knowing
how far the experts were from each other. Reporting it properly is a small but real
methodological improvement on the nearest prior work.

### 11.2 The review screen was justified one-sidedly

The design concluded that the skill-link review screen is a *requirement of the method*,
because measured linking accuracy (Acc@1 0.23–0.29, §10.1) makes an unreviewed mapping
unusable as evidence. That establishes review is **necessary**. Nothing in the corpus
established that it **works**.

[Chen et al. (2025)](../papers/chen-2025-interface-design-high-stakes.md) supply the
missing half, and the finding is uncomfortable: human–AI teams frequently **underperform
the AI alone**, because reviewers exhibit [automation bias](../concepts/automation-bias.md)
and accept incorrect recommendations without scrutiny. Across 108 participants on
high-stakes medical decisions, they compare six decision-support mechanisms and find a
clear asymmetry. Mechanisms that *inform* the reviewer — AI confidence, text explanations,
performance visualisations — improved collaborative performance and calibrated trust.
Mechanisms that *interrogate* the reviewer — feedback prompts, AI-generated questions —
deepened reflection but **reduced task performance** through cognitive load, and damaged
trust as a result. Simple visual explanations did nothing.

Read against Iris's specified screen, this validates part of it and puts the rest on
notice. Per-link confidence, the official skill definition and the highlighted evidence
span are precisely the informing mechanisms that helped. Confidence-first ordering and the
level-source disagreement display, however, sit close to the cognitive forcing functions
that *hurt* — they are retained for a different and stated reason, to direct scarce
attention and to refuse to hide uncertainty, but they are the first candidates to make
optional if usability testing shows review completion degrading.

The practical addition is a detector. Automation bias predicts that bulk-accept on
high-confidence links will be used indiscriminately, and that is the most bias-prone
affordance on the screen. The instrumented **correction rate** is how it gets caught: a
correction rate far below the Sprint 4 measured error rate means reviewers are
rubber-stamping, and the resulting report is not the evidence it claims to be. That check
belongs in the analysis of every reviewed programme, not only in usability sessions.

### 11.3 An underspecification, measured rather than argued

§4 and §10 both carry RCA weighting forward from
[Ahadi et al. (2022)](../papers/ahadi-2022-skills-taught-vs-sought.md) without ever stating
**which denominator**. RCA is a ratio of shares, and on this data the numerator is
unambiguous — within a career, the share computed from `count` and from `percentage` is
identical, because the per-career posting total cancels. The global denominator is not: one
may weight careers by posting volume, or treat each career as a single observation.

The difference is not academic. Measured on the Data Engineer demand vector, the two
constructions give a median absolute RCA difference of 3.02, a maximum of 23.86, and a
**top-15 ranking overlap of only 8 out of 15** — on the very list a curriculum committee is
handed as its priority order.

Iris adopts career-equal weighting, on the grounds that count-weighting inherits the
unresolved meaning of `N`: per-career posting totals span 203 to 6,291,725, and if that
range reflects a corpus artefact rather than real demand, count-weighting propagates the
artefact into every ranked list. The choice is stated in outputs and the alternative
reported as a sensitivity check.

### 11.4 A fourth confirmed gap

The seniority gradient — comparing a skill's prevalence between paired career rungs to see
which skills gain prominence with experience — entered the design after both review rounds
and had never been searched for. Searching found industry guidance on seniority
classification and one study of how candidates *describe* themselves
(Azamnouri et al. 2026: *"seniority nearly triples the odds of articulating leadership"*,
from 300 CVs), but **no empirical work measuring skill-demand shifts across seniority rungs
from a published occupational taxonomy**.

That makes it a fourth confirmed gap alongside the three recorded in §10.5 — NLP on Thai
TQF documents, Thai PDF text-layer corruption, and grading curriculum skill depth against a
competency scale — and it should be presented as a contribution rather than as an
application of existing method.

### 11.5 What the audit changed about the process

Both errors survived two full review rounds for the same structural reason: only the
question → paper direction was ever checked. A question node can look thoroughly supported
while a *design decision derived from it* rests on nothing, because the decision is not a
node in the graph at all. The audit therefore added a **design element → evidence**
traceability table to `index.md`, and three rules to the methodology: verify links are
bidirectional (the audit found 18 one-way edges), audit design against evidence rather than
only questions against papers, and **search for every new method element before it is
built** — both errors here entered the design after the reviews had finished.


### Non-peer-reviewed sources (added 2026-08-27)

These are government publications and platform documentation, not journal articles. They
are load-bearing for the design and must be cited as what they are.

- **สำนักงานปลัดกระทรวง อว. (OPS MHESI) / KMITL.** *Thailand Skill Mapping.* Public
  platform and open-data API. https://www.skillmapping.in.th/ ·
  https://skill-mapping.ops.go.th/ · https://skill.kmitl.ac.th/ · API
  https://api.skillmapping.in.th/docs (v0.8.1-beta-public). Snapshot used in this project:
  2026-08-27, `data/skillmapping/2026-08-27/`. — [concept note](../concepts/thailand-skill-mapping.md)
- **Khomfoi S.** *Skill Mapping: Empowering Thailand's Higher Education for the Future.*
  Invited talk abstract, Kasetsart University, 2568/2025.
  https://registrar.ku.ac.th/wp-content/uploads/eduserv/academic/training/2568/671112_SkillMapping/Skill_Mapping_Surin_Thailand.pdf
  — states the platform's framing of open data for curriculum redesign.
- **Anmanatarkul A., Chomsuwan K., Jiracheewanun S., Sooklamai M., Kirtphaiboon S. &
  Wiyaratn W.** (2025). *Development of Learning Modules and Skills Mapping to Prepare
  Workforce Competencies for the Electric Vehicle Industry.* FTE Journal.
  https://so10.tci-thaijo.org/index.php/FTEJournal/article/view/1351
  ⚠️ **KMUTT**, not KMITL — a Delphi expert-consensus skill map for the EV industry
  (seven skill groups). A methodological precedent for curriculum↔career skill mapping;
  **not** the national database.

---

## References

Author-date citations above resolve to this list; the full author list and
detailed findings live in each `wiki/papers/` note.

1. Ahadi A. et al. (2022). *Skills Taught vs Skills Sought: Using Skills Analytics to Identify the Gaps between Curriculum and Job Markets.* EDM 2022 (poster). — [note](../papers/ahadi-2022-skills-taught-vs-sought.md)
2. Aljohani N.R. et al. (2022). *Bridging the skill gap between the acquired university curriculum and the requirements of the job market.* Journal of Innovation & Knowledge. https://doi.org/10.1016/j.jik.2022.100190 — [note](../papers/aljohani-2022-curriculum-skill-gap-bibliometric.md)
3. Arslan İltüzer E., Özlü Ö.A., Farajijobehdar V. & Eryiğit G. (2026). *Leveraging LLMs For Turkish Skill Extraction.* arXiv:2601.22885. https://arxiv.org/abs/2601.22885 — [note](../papers/arslan-2026-turkish-skill-extraction.md)
4. Chaiaroon P. et al. (2025). *Digital Workforce Matching: A Machine Learning Approach for Skill-Based Job Classification and Recommendation.* J. Current Science and Technology. https://doi.org/10.59796/jcst.V15N4.2025.137 — [note](../papers/chaiaroon-2025-thai-digital-workforce-matching.md)
5. Chen Z., Luo Y. & Sra M. (2025). *Engaging with AI: How Interface Design Shapes Human-AI Collaboration in High-Stakes Decision-Making.* arXiv:2501.16627. https://arxiv.org/abs/2501.16627 — [note](../papers/chen-2025-interface-design-high-stakes.md)
6. Dixon N. et al. (2023). *Occupational models from 42 million unstructured job postings.* Patterns. https://doi.org/10.1016/j.patter.2023.100757 — [note](../papers/dixon-2023-occupational-models-42m.md)
7. Dong H., Chen J., He Y., Liu Y. & Horrocks I. (2023). *Reveal the Unknown: Out-of-Knowledge-Base Mention Discovery with Entity Linking.* CIKM 2023. https://doi.org/10.1145/3583780.3615036 — [note](../papers/dong-2023-out-of-kb-mention-discovery.md)
8. Fettach Y. et al. (2025). *Skill Demand Forecasting Using Temporal Knowledge Graph Embeddings.* arXiv:2504.07233. https://arxiv.org/abs/2504.07233 — [note](../papers/fettach-2025-skill-demand-temporal-kg.md)
9. Herandi A., Li Y., Liu Z., Hu X. & Cai X. (2024). *Skill-LLM: Repurposing General-Purpose LLMs for Skill Extraction.* arXiv:2410.12052. https://arxiv.org/abs/2410.12052 — [note](../papers/herandi-2024-skill-llm.md)
10. Hilliger I. et al. (2022). *Lessons learned from designing a curriculum analytics tool for improving student learning and program quality.* Journal of Computing in Higher Education. https://doi.org/10.1007/s12528-021-09284-2 — [note](../papers/hilliger-2022-curriculum-analytics-tool.md)
11. Januzaj Y. & Luma A. (2022). *Cosine Similarity – A Computing Approach to Match Similarity Between Higher Education Programs and Job Market Demands.* iJET 17(12). https://doi.org/10.3991/ijet.v17i12.30375 — [note](../papers/januzaj-2022-cosine-similarity-he-job-market.md)
12. Kavargyris D.C. et al. (2025). *ESCOX: A tool for skill and occupation extraction using LLMs from unstructured text.* Software Impacts. https://doi.org/10.1016/j.simpa.2025.100772 — [note](../papers/kavargyris-2025-escox-skill-extraction.md)
13. Kumar R., Gulwani D. & Singh S. (2025). *Automated Analysis of Learning Outcomes and Exam Questions Based on Bloom's Taxonomy.* arXiv:2511.10903. https://arxiv.org/abs/2511.10903 — [note](../papers/kumar-2025-bloom-taxonomy-classification.md)
14. Le N.L., Abel M.-H. & Laforge B. (2026). *From Learning Resources to Competencies: LLM-Based Tagging with Evidence and Graph Constraints.* arXiv:2605.28483. https://arxiv.org/abs/2605.28483 — [note](../papers/le-2026-competency-tagging-evidence.md)
15. Lertmethaphat N.N. et al. (2025). *Exploring the Thai Job Market Through the Lens of Natural Language Processing and Machine Learning.* PIER Discussion Paper 228. https://www.pier.or.th/dp/228/ — [note](../papers/lertmethaphat-2025-thai-job-market-nlp.md)
16. Lowphansirikul L. et al. (2021). *WangchanBERTa: Pretraining transformer-based Thai Language Models.* arXiv:2101.09635. https://doi.org/10.48550/arXiv.2101.09635 — [note](../papers/lowphansirikul-2021-wangchanberta.md)
17. Luyen L.N. & Abel M.-H. (2025). *Automated Skill Decomposition Meets Expert Ontologies: Bridging the Granularity Gap with LLMs.* arXiv:2510.11313. https://doi.org/10.48550/arXiv.2510.11313 — [note](../papers/luyen-2025-skill-decomposition-ontology.md)
18. Macedo M.M.G. de et al. (2022). *Practical Skills Demand Forecasting via Representation Learning of Temporal Dynamics.* arXiv:2205.09508. https://arxiv.org/abs/2205.09508 — [note](../papers/macedo-2022-skills-demand-forecasting-temporal.md)
19. Nonesung S. et al. (2025). *ThaiOCRBench: A Task-Diverse Benchmark for Vision-Language Understanding in Thai.* IJCNLP-AACL 2025. arXiv:2511.04479. https://arxiv.org/abs/2511.04479 — [note](../papers/nonesung-2025-thaiocrbench.md)
20. Nonesung S., Nitarach N., Jaknamon T., Taveekitworachai P. & Pipatanakul K. (2026). *Typhoon OCR: Open Vision-Language Model For Thai Document Extraction.* arXiv:2601.14722. https://arxiv.org/abs/2601.14722 — [note](../papers/nonesung-2026-typhoon-ocr.md)
21. Passonneau R. (2006). *Measuring Agreement on Set-valued Items (MASI) for Semantic and Pragmatic Annotation.* LREC 2006. https://aclanthology.org/L06-1392/ — [note](../papers/passonneau-2006-masi-set-agreement.md)
22. Phaphuangwittayakul A. et al. (2018). *Analysis of Skill Demand in Thai Labor Market from Online Jobs Recruitment Websites.* JCSSE 2018 (IEEE). https://doi.org/10.1109/JCSSE.2018.8457393 — [note](../papers/phaphuangwittayakul-2018-thai-skill-demand-jobthai.md)
23. Phatthiyaphaibun W. et al. (2023). *PyThaiNLP: Thai Natural Language Processing in Python.* NLP-OSS @ EMNLP. https://arxiv.org/abs/2312.04649 — [note](../papers/phatthiyaphaibun-2023-pythainlp.md)
24. Rikala P. et al. (2024). *Understanding and measuring skill gaps in Industry 4.0 — A review.* Technological Forecasting and Social Change. https://doi.org/10.1016/j.techfore.2024.123206 — [note](../papers/rikala-2024-skill-gaps-industry40-review.md)
25. Sabet A.J. et al. (2024). *Course-Skill Atlas: A national longitudinal dataset of skills taught in U.S. higher education curricula.* Nature Scientific Data. https://doi.org/10.1038/s41597-024-03931-8 — [note](../papers/sabet-2024-course-skill-atlas.md)
26. Saroglou S., Diamantaras K., Preta F., Delianidi M., Benisis A. & Meyer C.J. (2025). *Enhancing Job Matching: Occupation, Skill and Qualification Linking with the ESCO and EQF taxonomies.* arXiv:2512.03195. https://arxiv.org/abs/2512.03195 — [note](../papers/saroglou-2025-esco-eqf-linking.md)
27. Sarthi P., Abdullah S., Tuli A., Khanna S., Goldie A. & Manning C.D. (2024). *RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval.* ICLR 2024. arXiv:2401.18059. https://arxiv.org/abs/2401.18059 — [note](../papers/sarthi-2024-raptor.md)
28. Seif A. et al. (2024). *A Dynamic Jobs-Skills Knowledge Graph.* RecSys in HR 2024 (CEUR Vol-3788). — [note](../papers/seif-2024-dynamic-jobs-skills-kg.md)
29. Senger E. et al. (2024). *Deep Learning-based Computational Job Market Analysis: A Survey on Skill Extraction and Classification from Job Postings.* NLP4HR @ EACL. https://doi.org/10.48550/arXiv.2402.05617 — [note](../papers/senger-2024-dl-skill-extraction-survey.md)
30. Siddoo V. et al. (2019). *An exploratory study of digital workforce competency in Thailand.* Heliyon. https://doi.org/10.1016/j.heliyon.2019.e01723 — [note](../papers/siddoo-2019-thai-digital-workforce-competency.md)
31. Tipsena R. et al. (2025). *Predicting Workforce Needs in Thailand's Digital Industry: A Machine Learning Approach (2023-2024).* JISTaP 13(3). https://doi.org/10.1633/JISTaP.2025.13.3.1 — [note](../papers/tipsena-2025-predicting-thai-digital-workforce.md)
32. Vo N.N.Y. et al. (2022). *Domain-specific NLP system to support learning path and curriculum design at tech universities.* Computers and Education: Artificial Intelligence. https://doi.org/10.1016/j.caeai.2021.100042 — [note](../papers/vo-2022-nlp-curriculum-learning-path.md)
33. Weerasombat T. & Pumipatyothin P. (2025). *Employers' priority on work skills and the skill gaps: a case of Thailand.* Cogent Education. https://doi.org/10.1080/2331186X.2024.2441656 — [note](../papers/weerasombat-2025-thai-employer-skill-priorities.md)
34. Xu Z. et al. (2025). *From Course to Skill: Evaluating LLM Performance in Curricular Analytics.* arXiv:2505.02324. https://doi.org/10.48550/arXiv.2505.02324 — [note](../papers/xu-2025-llm-curricular-analytics.md)
35. Zaki N., Turaev S., Shuaib K., Krishnan A. & Mohamed E. (2023). *Automating the mapping of course learning outcomes to program learning outcomes using natural language processing for accurate educational program evaluation.* Education and Information Technologies 28(12), 16723–16742. https://doi.org/10.1007/s10639-023-11877-4 — [note](../papers/zaki-2023-clo-plo-mapping-automation.md)
36. Zhang M., van der Goot R. & Plank B. (2024). *Entity Linking in the Job Market Domain.* Findings of EACL 2024. arXiv:2401.17979. https://arxiv.org/abs/2401.17979 — [note](../papers/zhang-2024-job-market-entity-linking.md)
