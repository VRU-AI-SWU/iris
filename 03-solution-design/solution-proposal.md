# Solution Proposal — Iris (Curriculum Skill Alignment)

> Rewritten 2026-08-27 after the pivot to the national Skill Mapping standard.
> Supersedes the 2026-04-30 proposal, which assumed Iris would build its own skill
> vocabulary and scrape its own labour-market data. Both assumptions are now obsolete.
> Empirical basis: [`data-feasibility.md`](data-feasibility.md).

---

## What changed, and why

In July 2025 the Office of the Permanent Secretary, MHESI (สป.อว.) published the
**Thailand Skill Mapping** database, developed by KMITL. It defines, as national
reference data, a vocabulary of **4,376 skills** — each with a Thai definition and
three graded proficiency levels — mapped to **371 careers** across five priority
industries, with demand figures attached to every career × skill pair.

The platform describes its own purpose as joining a **Demand Side** (skills the labour
market requires) to a **Supply Side** (competencies curricula produce). Only the demand
side is published. **The supply side is unbuilt, and that is precisely what Iris does.**

This reframes the project. Iris is no longer a self-contained system that invents its
own skill vocabulary and measures against data it scrapes itself; it is **the
supply-side engine for a national standard** — the component that reads a Thai
university's TQF (มคอ.2) document and expresses its curriculum in the same vocabulary
the state already uses to describe labour demand.

The consequences are large and mostly subtractive:

| Removed from the design | Because |
|---|---|
| Scrapers for JobThai, JobsDB, JOBBKK, JOBTOPGUN | Demand data is published, already aggregated |
| Emergent vocabulary construction (embedding + HDBSCAN clustering) | The vocabulary is fixed national reference data |
| Python clustering sidecar | Nothing left to cluster |
| `pgvector` / any vector database | 4,376 fixed entries is a 13 MB in-memory matrix |
| Heavy job queue (Celery/Redis, Apalis) | Existed to manage scraping fan-out |
| chaiaroon-2025 20-role taxonomy | Replaced by 138 official digital careers |

And one large addition: because every skill in the standard carries **three
proficiency levels with explicit criteria**, and because TQF documents declare their
own depth signals under regulation, Iris can ask a question no prior work on Thai
curricula has asked — not *"does this programme teach skill X?"* but ***"to what level,
and is that the level the career requires?"***

---

## Problem Statement

Thai academic programmes are documented in the TQF (มคอ.2) format, which specifies
intended learning outcomes in prose and in curriculum-mapping tables. The state now
publishes, in a controlled vocabulary, what skills each career demands. **No mechanism
exists to express a curriculum in that same vocabulary**, so the two halves of the
national skill-mapping effort cannot be compared. Curriculum committees revising a
programme have no reproducible, evidence-based answer to "which skills that our target
careers demand does this curriculum not develop, and at what level do we fall short?"

---

## Proposed Solution

Iris reads a TQF (มคอ.2) document, extracts every course with its description, credit
weighting, and declared learning-outcome responsibilities, and **links each course to
the national skill vocabulary at a stated proficiency level**. Aggregating across
courses yields a *programme skill profile* expressed natively in the national standard.
That profile is then compared against the published demand profile of any of the 138
digital-industry careers, producing a prioritised, level-aware alignment report with
per-course traceability and page-level provenance back into the source document.

**Core research contribution:** skill entity linking from Thai TQF course descriptions to
a national controlled vocabulary **with an inferred proficiency level on the curriculum
side**, evaluated against expert annotation — and alignment measured against the
standard's published demand, including a **seniority gradient** derived from its
paired junior/senior careers.

> ⚠️ **Precision about what "level-aware" means here.** The standard grades every *skill*
> into three levels with criteria, but it does **not** publish a required level per
> career × skill — a career's demand entry carries only `count` and `percentage`. Levels
> therefore exist on the **curriculum side only**. Iris can state *"this programme
> develops SQL to foundational level"*; it cannot state *"the market requires SQL at
> intermediate level"*, and no output may imply otherwise. The demand-side depth signal
> is the seniority gradient described in §5, which is derived from data that exists.

---

## Why this is a stronger research position than the previous design

| Previous design | This design |
|---|---|
| Vocabulary emerged from clustering — unstable across runs, no ground truth | Vocabulary is fixed national reference data — annotation and evaluation are well defined |
| Gap measured against self-scraped postings — not reproducible, ToS-exposed | Gap measured against published state data — anyone can reproduce it |
| Zero-shot extraction, because no retrieval corpus existed | RAG-based linking, because 4,376 skill definitions and 6,058 level criteria *are* the corpus |
| Binary presence of a skill | Graded proficiency, grounded in TQF's own outcome structure |
| Contribution: a tool | Contribution: the missing half of a national standard, plus a reusable Thai skill-linking method |

The literature already collected in Phase 2 becomes *more* relevant, not less: ESCO
skill-linking work ([`kavargyris-2025-escox`](../02-literature-review/wiki/papers/kavargyris-2025-escox.md),
[`senger-2024-dl-skill-extraction-survey`](../02-literature-review/wiki/papers/senger-2024-dl-skill-extraction-survey.md),
[`luyen-2025-skill-decomposition-ontology`](../02-literature-review/wiki/papers/luyen-2025-skill-decomposition-ontology.md))
is now the direct methodological analogue — linking free text to a fixed occupational
taxonomy — rather than a loose parallel.

---

## Use Cases

### UC1 — Programme-to-Career Alignment Report
- **Actor:** Curriculum committee member / academic administrator
- **Precondition:** TQF document ingested; a target career selected from the 138
  digital careers
- **Flow:** select programme → select career → system compares the programme's
  level-aware skill profile against the career's published demand → produces a ranked
  alignment report
- **Outcome:** a prevalence-ranked list of *demanded skills the curriculum does not
  develop*; where the career is seniority-paired, a second panel showing *skills that gain
  prominence at the senior rung and the level the curriculum develops them to*. Every entry
  traceable to specific courses and to a page in the source มคอ.2

### UC2 — Programme-to-Programme Comparison
- **Actor:** Curriculum committee, accreditation reviewer
- **Precondition:** both programmes ingested and their links reviewed
- **Flow:** both profiles are expressed in the same national vocabulary and decomposed
  into four sets — shared at the same level, shared at *different* levels, A-only, B-only
- **Outcome:** an objective differentiation profile. This is the department's stated
  motivation for the project: comparing its own curriculum against peers'
- **Constraint:** an unreviewed programme may not enter a comparison. Comparing one
  reviewed profile against one raw model output would present linking error as curricular
  difference. Both sides must carry the same review status, and the report states it
- ⚠️ **Not deliverable in v1 as things stand.** UC2 needs *two* complete, reviewed
  programmes. Only the SWU document is complete; the KU file is an excerpt. Each review is
  a substantial block of a faculty member's time, so this is limited by reviewer availability, not
  by compute. UC2 is built in Sprint 8 but cannot be *demonstrated* until a second full
  มคอ.2 is obtained and reviewed — the highest-value external dependency the project has

### UC3 — Curriculum Revision Scenario
- **Actor:** Curriculum designer, during a มคอ.2 revision cycle
- **Precondition:** a reviewed baseline profile exists
- **Flow:** three edit types, all recomputing the profile and alignment without
  re-running the LLM —
  1. **include / exclude a course** (electives in or out, a course retired)
  2. **adjust a link** (accept, reject, or change level) inherited from the review screen
  3. **add a hypothetical course** by pasting a draft description, which *does* invoke
     linking for that course alone
- **Outcome:** the skill consequence of a proposed change, before it is committed
- **Constraint:** scenarios are never published. A scenario is a hypothetical curriculum,
  and publishing one would put a programme that does not exist on the public site

### UC4 — Public Programme Profile
- **Actor:** Anyone visiting vru-ai.com
- **Flow:** browse published analyses — programme profiles, alignment heatmaps,
  narrative summaries
- **Outcome:** the research is legible and citable without an account

*Dropped from the previous design:* the "student career alignment" use case. It implies
individual-level advice the programme-level analysis cannot support, and no student
stakeholder was ever available to validate it.

---

## Architecture

Two deployables, on purpose. The analysis engine needs a GPU, native Python libraries,
and tens of minutes per run; the public web tier must stay up regardless.

```
┌─ CLOUDFLARE ───────────────────────────────────────────────────────────┐
│                                                                        │
│  vru-ai.com/iris                    vru-ai.com/iris/app                │
│  ┌──────────────────────┐           ┌────────────────────────────┐    │
│  │ Astro static site    │           │ Cloudflare Access          │    │
│  │ published results    │           │ (department faculty only)  │    │
│  │ as build-time JSON   │           └─────────────┬──────────────┘    │
│  │ — no backend         │                         │                    │
│  └──────────────────────┘                         │                    │
└───────────────────────────────────────────────────┼────────────────────┘
                                                    │ Cloudflare Tunnel
                                                    │ (outbound only)
┌─ gpu-linux-server — department office, 24/7 ──────▼────────────────────┐
│                                                                        │
│  FastAPI ── job table ──► worker process                               │
│                             │                                          │
│    ┌────────────────────────▼─────────────────────────────────────┐   │
│    │ INGESTION                                                     │   │
│    │  text-layer integrity gate → glyph repair → PageIndex tree    │   │
│    │  → section extraction (courses, CLOs, curriculum map)         │   │
│    ├───────────────────────────────────────────────────────────────┤   │
│    │ LINKING                                                       │   │
│    │  candidate retrieval (in-memory matrix, 4,376 × d)            │   │
│    │  → LLM adjudication against level criteria                    │   │
│    │  → level inference from CLO / ● ○ map / year / prerequisites  │   │
│    ├───────────────────────────────────────────────────────────────┤   │
│    │ ANALYSIS                                                      │   │
│    │  programme profile → alignment vs published demand → report   │   │
│    └───────────────────────────────────────────────────────────────┘   │
│                             │                                          │
│  PostgreSQL (source of truth) ──► publish/export ──► static JSON       │
│  LLM + embeddings via OpenAI-compatible endpoint (local)               │
└────────────────────────────────────────────────────────────────────────┘
```

**The publish step is the contract.** The engine writes a versioned result document;
the web tier only ever reads published result documents. Nothing on the public site
queries the GPU server at request time, so the site is unaffected when the engine is
busy, restarting, or offline.

### Components

| Component | Responsibility | Technology |
|---|---|---|
| Snapshot mirror | Pin a reproducible copy of the national standard | `fetch_snapshot.py` (stdlib) |
| Text-layer gate | Classify a PDF `clean / repairable / unusable` via Thai mark-rate diagnostic | Python |
| Glyph repair | Restore tone marks and karan lost to WinAnsi font encoding | Python, deterministic mapping table |
| Document indexer | Build a navigable tree of the มคอ.2; locate sections with page provenance | PageIndex |
| Section extractor | Exhaustively parse the located sections into courses, CLOs, curriculum map | Python |
| Candidate retriever | Top-k skill candidates per course from the fixed vocabulary | NumPy in-memory matrix + lexical |
| Skill linker | Decide which candidates apply; assign proficiency level with evidence | Local LLM, structured output |
| Alignment engine | Compare programme profile to career demand; rank gaps | NumPy / SciPy |
| Report generator | Heatmap, ranked gap table, narrative, PDF | Python, WeasyPrint |
| API | Upload, job status, results, publish | FastAPI |
| Web | Public results + gated analysis UI | Astro on Cloudflare Workers |

---

## Method

### 1. Ingestion, with an integrity gate

Real TQF documents produced by print drivers lose Thai tone marks and karan to WinAnsi
font encoding (measured: karan 1 % retained, mai tho 14 % in the SWU document), while
others silently collapse `ำ` to `า`. Both defects are invisible to a naive parser and
would poison every downstream stage.

Every document therefore passes a **diagnostic gate** before ingestion: the rate of
Thai combining marks per 1,000 Thai characters, compared against a clean-document
baseline (~171). Documents are classified:

- **clean** → use the text layer
- **repairable** → apply the glyph repair table, re-run the gate, proceed on pass
- **lossy or unusable** → re-extract with a Thai vision-language model, re-run the gate,
  and **flag the document as vision-derived in its provenance**

The repair is deterministic and auditable — a table keyed on the substitute glyph and
its preceding character — rather than an OCR or LLM guess, so wherever it applies the
pipeline stays reproducible and every restored character can be justified. It is preferred
for that reason.

A **normalisation** pass runs first and reverses structural breaks that need no learned
table, because Thai orthography determines the answer: `ำ` written as `ํ` + `า` (Adobe), or
as consonant + space + `า` (MS Word). `า` is a dependent vowel and cannot begin a syllable,
so a space before it is always an artefact.

Across five universities and five PDF producers, **every document reaches a usable text
layer without a vision model** (see `data-feasibility.md`). The vision fallback therefore
remains for a document that genuinely needs one — a scan, or deletion rather than
substitution — but it is no longer on the critical path, and **ingestion has no GPU
dependency**. Typhoon OCR reaches Levenshtein 0.04 on Thai government forms at 3B
parameters, self-hostable alongside the adjudication model. The
provenance flag matters, because a vision extraction is a model output rather than a
faithful reading, and any finding traced back to it must say so. The integrity gate runs on
the vision output too — Thai diacritic loss is a documented failure mode of vision models
as well, so the same check applies — together with a Thai-character-proportion check to
catch the language-bias failure where a model drifts into English.

### 2. Document navigation

มคอ.2 has a regulated section structure, but universities paginate and format it
differently. PageIndex builds a tree index of the document (from the PDF's own layout,
with LLM summarisation of nodes) and locates the target sections — `3.1.5
คำอธิบายรายวิชา`, the curriculum mapping table, the programme ELO list.

Two constraints on its use:

- **Locate, then extract exhaustively.** PageIndex is a retrieval system; Iris needs
  *all* courses, not the most relevant ones. It is used to find section boundaries,
  after which the section is parsed in full.
- **Provenance is a deliverable.** Tree nodes carry page ranges, so every extracted
  course description records the page it came from — required for the paper and for
  a curriculum committee to trust a finding.

### 3. Skill linking

For each course, candidate skills are retrieved from the 4,376-entry vocabulary, then
adjudicated by a local LLM against the candidates' definitions.

- **Retrieval** combines dense similarity (embeddings of skill title + definition,
  held as a 13 MB in-memory matrix — exact cosine, no ANN index, no vector database)
  with lexical matching, which is essential for tool names and English terms.
- **Bilingual channel, where the document provides one.** The vocabulary is fully
  bilingual, and some TQF documents give every course an English description. Where both
  exist, linking runs on each independently and agreement is recorded as a confidence
  signal.
  ⚠️ **It is a cross-check, not a safety net, and the two documents show why.** KU gives
  every course a full English description but is the *milder* damage case; SWU is
  Thai-only in its course descriptions (English appears in titles) and is the *severe*
  case. The channel is therefore absent from the document that would benefit most from
  it. Coverage must be reported per document, and no design decision may assume it.
- **Adjudication is multiple-choice, not open generation** — "which of these 30
  candidate skills does this course develop?" — which is materially easier for a small
  local model than free-form extraction, and produces output that is constrained to
  valid skill IDs by construction. Every accepted link carries an **evidence span**; the
  constrained, evidence-producing formulation is reported to outperform unconstrained
  prompting, not merely to explain it better.
- **Out-of-vocabulary is an explicit decision, not a threshold.** A curriculum teaches
  theory, research method and ethics that no job advertisement describes; mapping those to
  the nearest labour-market skill would be confidently wrong. Modelling "none of these"
  as a first-class output beats similarity thresholding.
- **The model provider is a seam, not a hard-coded choice.** Embedding and adjudication
  run behind one provider-blind interface with two implementations: a local
  OpenAI-compatible endpoint on `gpu-linux-server`, and **Cloudflare Workers AI**. The
  pattern is taken from the lab's Argus project, which already runs it in production.

  Three reasons it fits Iris better than it fits Argus:

  | | Argus | Iris |
  |---|---|---|
  | Data sensitivity | health claims — **must not leave the machine**, so local is the default | TQF documents are **public institutional records**, so no such constraint |
  | Usage shape | interactive demo, needs ~32 cases/day | batch, a handful of programmes **per year** |
  | Free-tier fit | exhausted the 10,000 neurons/day allowance once in development | ≈ **$0.036 per programme** — about a third of one day's free allowance |

  Derived from the measured token cost (§3, ~310 k input tokens per programme) at the
  rates Argus recorded for `@cf/google/gemma-4-26b-a4b-it`: roughly **three programmes per
  day within the free tier**, against a project that will analyse a handful in total.

  It also mitigates a risk recorded below: when the lab's other projects are training,
  `gpu-linux-server` has ~15 GB free rather than 23 GB, and linking can run on Workers AI
  instead of queueing behind them.

  **Ingestion cannot move.** PDF text extraction, PageIndex navigation and the Typhoon OCR
  fallback are native or Python work with no Workers equivalent. The seam sits at *linking*,
  not at the pipeline boundary.

- 🔴 **The provider is pinned per analysis run. There is no mid-run fallback.** Argus
  switches provider mid-case and records which model read each page; that is right for a
  demo and wrong here. A programme whose 78 courses were linked by two different models is
  not a reproducible analysis and cannot be compared with another programme. If a quota is
  exhausted mid-run, **the run fails and requeues on the other provider from the start**.
  `analysis_run` records the provider alongside the model and the snapshot date.

  The corollary binds the evaluation: **the Sprint 4 gate must measure whichever provider
  and model will serve production.** Measuring a local model and shipping a Workers AI one
  would invalidate every number the paper reports.

- **An LLM adjudicator is not assumed to be the best ranker.** A supervised ranking
  baseline is included in the evaluation, because at least one comparable study found
  supervised models beating decoder-only LLMs at this step.
- **A course may legitimately link to nothing.** General-education courses — Thai
  language, physical education, ethics — develop capabilities a labour-market vocabulary
  does not name. Zero links is a valid, recorded outcome, distinguished in the data from
  *not yet processed* and from *processed and failed*. The proportion of zero-link courses
  per category is a reportable statistic and a coverage signal about the standard itself,
  not an error to be suppressed.

#### Cost and runtime

Derived rather than asserted, from the pinned snapshot: skill definitions have a median
length of 149 characters, so at `k = 30` candidates a prompt carries roughly 3,400 tokens
of candidate context plus ~270 for the course description and ~300 of instruction —
**≈ 3,970 input tokens per course**, and **≈ 310 k input tokens per programme** of 78
courses in one language, doubling where a bilingual channel exists. Output is a short
structured object.

That is a modest load for a locally served model and is not the bottleneck. The
document-side stages — PageIndex tree construction over 216 pages, and vision
re-extraction where the gate demands it — dominate wall-clock. A full run is expected in
minutes rather than tens of minutes; the figure is measured in Sprint 10 rather than
promised here, and the interface is designed for a wait regardless.

### 4. Level inference

Proficiency level is inferred from evidence the document already contains, not guessed
from the description alone:

1. **Course learning outcomes (CLOs)** where present — matched against the skill's own
   level criteria from the standard
2. **Curriculum mapping table** — ● ความรับผิดชอบหลัก vs ○ ความรับผิดชอบรอง, the
   programme's own regulated declaration of how central an outcome is to a course
3. **Position in the curriculum** — year of study from the course code, and
   prerequisite depth

Where the sources disagree, the conflict is recorded rather than silently resolved;
disagreement rate is itself a reportable finding.

Two constraints from the literature. First, **level is not asked of the LLM holistically**:
zero-shot LLM classification of learning outcomes into Bloom levels measures at 0.72–0.73,
more than twenty points behind a classical verb-feature classifier on the same data, so a
non-LLM baseline over CLO text is part of the evaluation and may win. Second, **the ● / ○
matrix is evidence, not ground truth** — it is hand-authored for accreditation, and
reconstructing it automatically reaches only 83–88% agreement with domain experts, varying
by five points between two programmes at one institution. That variance is also a caveat on
cross-institution comparison.

### 5. Alignment measurement

The published demand figure is **prevalence** — the share of postings for a career that
mention a skill — not a probability distribution; percentages across a career sum to far
more than 100. And, as noted above, **it carries no level**. Metrics are defined on what
the data actually contains.

#### Programme profile

Aggregating course-level links into a programme profile. For each skill *s*:

| Component | Definition |
|---|---|
| `covered` | at least one course links to *s* after review |
| `level` | **max** over linking courses — a programme develops a skill to the deepest level any course reaches |
| `depth` | number of linking courses, and total credits of those courses |
| `sources` | the courses themselves, for traceability |

`max` rather than a weighted mean for level, because a curriculum's capability is set by
its most advanced treatment, not by an average diluted by introductory mentions. Credit
weighting enters `depth`, not `level` — how much of the programme is devoted to a skill is
a different question from how deeply it is taught. See [[q-credit-weighting]].

#### Primary metric — prevalence-weighted coverage gap

For a target career, rank the skills it demands that the programme does not develop,
weighted by prevalence:

> *"65 % of Data Engineer postings mention SQL — the programme develops it (advanced, CP242).
> 58 % mention Data Warehousing — no course develops it."*

Every term is measured. No claim is made about a level the market requires.

#### Career specificity weighting (RCA)

Down-weights skills every career demands, up-weights discriminating ones, so the ranked
list is actionable rather than dominated by universal soft skills.

⚠️ **The denominator must be stated, because the choice changes the ranking.** RCA is a
ratio of shares. The numerator — a skill's share within a career — is identical whether
computed from `count` or `percentage`, since `N_c` cancels. The *global* denominator is
not: weighting careers by posting volume gives a different answer from treating each
career as one observation. Measured on Data Engineer, median |ΔRCA| = 3.02, max 23.86, and
**the top-15 ranking overlaps by only 8/15**.

**Iris uses career-equal weighting.** Count-weighting inherits the unresolved meaning of
`N` (203 to 6,291,725 per career); if that range is a corpus artefact, count-weighting
propagates it into every ranked list. The choice is stated in every output, and the
alternative is reported as a sensitivity check. See [[q-prevalence-metrics]].

#### Seniority gradient — the demand-side depth signal

The standard contains **13 seniority-paired careers** in the digital industry, of which
**12 are analysable** — `senior-frontend-developer` has only 5 skills and is excluded by the
degenerate-career filter (verified in code, Sprint 0):
`data-scientist` has four rungs (base → senior → lead → chief); `data-engineer`,
`web-developer`, `developer`, `application-developer` and `sound-designer` have
base → senior; `project-manager` and `animator` have base → lead; `software-engineer` has
junior → base.

For a paired career, the change in a skill's prevalence between rungs is a measured signal
of which skills become more central with experience. For Data Scientist → Senior Data
Scientist:

| Δ prevalence | Skill |
|---|---|
| **+12.67 pp** | การสร้างแบบจำลองทำนาย (predictive modelling) |
| **+12.02 pp** | การประยุกต์ใช้การเรียนรู้ของเครื่อง (applied ML) |
| **+10.49 pp** | สถิติเชิงพหุ (multivariate statistics) |
| +2.24 pp | จาวา (Java) |
| −0.58 pp | ทักษะการวิเคราะห์ (analytical skills) |

Crossing this with the curriculum's own levels gives the report's strongest finding:

> *"The skills that rise most from Data Scientist to Senior Data Scientist — predictive
> modelling, applied ML, multivariate statistics — are developed by this programme only
> at foundational level."*

This is **not** a proficiency requirement and must never be presented as one. It is a
statement about which skills gain prominence with seniority, which is the question a
curriculum committee can act on: *are we preparing graduates for the entry-level role, or
for the career?*

Availability is the constraint — 12 analysable ladder steps across 138 digital careers, so
this axis is present for some target careers and absent for others. Reports state which.

The ladders, with the top riser measured on the pinned snapshot:

| Ladder | shared skills | top rise |
|---|---|---|
| `data-engineer → senior-data-engineer` | 86 | Data Architecture **+17.9 pp** |
| `developer → senior-developer` | 77 | SQL **+17.7 pp** |
| `data-scientist → lead-data-scientist` | 80 | Predictive Modeling **+15.2 pp** |
| `data-scientist → senior-data-scientist` | 76 | Predictive Modeling **+12.7 pp** |
| `web-developer → senior-web-developer` | 75 | Mobile Web Design **+23.6 pp** |
| `junior-software-engineer → software-engineer` | 74 | RESTful WebServices **+5.9 pp** |

⚠️ **Direction is not uniform.** `senior-`, `lead-`, `principal-` and `chief-` sit *above*
the unprefixed career; `junior-` sits *below* it. The engine resolves this once, in
`SeniorityPair.from_rung`, rather than at each call site.

#### Growth-adjusted view

The standard publishes a per-skill `growth` rate per career, supporting a second temporal
question: is the curriculum keeping pace with skills that are rising, not merely with the
current stock? Read with [[q-temporal-drift]]'s finding that technical skills are volatile
and soft skills stable.

#### Distributional divergence (secondary)

KL divergence remains available, but only after explicit renormalisation of prevalence into
a share distribution, and the changed interpretation — "share of all skill mentions" —
must be stated wherever it is reported.

#### Hard constraints on every metric and narrative

1. **Truncation.** The demand vector is capped at roughly 100 skills per career. Absence
   means *below the cut-off*, never *not demanded*.
2. **No demand-side level.** No output may state or imply a level the market requires.
3. **Degenerate data.** The 168 career × skill pairs with `count = 0` and the three
   near-empty careers are filtered before any computation.

---

## Evaluation

The evaluation gate governs the project: **no user-facing feature is built until
linking quality is measured.** This is the discipline the previous phase stated and
then did not follow, and it is why that phase stalled.

**⚠️ The gate must measure the system that produces the output, not the model alone.**
Iris's deliverable is a set of **reviewed** links, not raw model output — that is the whole
justification for the review screen. But an evaluation of model precision and recall says
nothing about the quality of what a reviewer actually produces, and the evidence is that
this cannot be assumed: human–AI pairs frequently underperform the AI alone under
automation bias. A gate that passes on model F1 would license building everything
downstream on an untested assumption, and the screen itself would not be validated until
Sprint 9 — after the entire design has been committed to it.

The gate therefore has two halves. The second costs almost nothing, because the Sprint 4
annotators are performing the reviewer's task already:

| Half | Measures | Why |
|---|---|---|
| **Model** | precision / recall / F1 / Acc@k against expert annotation | Is retrieval-plus-adjudication good enough to be worth reviewing? |
| **System** | review-assisted quality · throughput · confidence calibration | Does review *improve* the output, at a rate a committee member can sustain? |

The system half runs on a **minimal interface** — a spreadsheet or CLI, not the Sprint 9
screen — because the point is to test the *premise* before the screen is designed, not the
screen itself. Three numbers come out of it:

- **Review-assisted quality** — reviewed output measured against the gold standard. If it
  is not better than raw model output, the review premise is wrong and the design must
  change, not the interface.
- **Throughput** — decisions per hour, extrapolated to a 78-course programme. Reviewing
  every proposed link is 624–1,092 decisions, or 104–182 minutes at 10 s each; the
  90-minute target is reachable only by bulk-accepting on confidence, which makes the next
  number load-bearing.
- **Confidence calibration** — are high-confidence links right at close to their stated
  confidence? If ~70 % of links are accepted without individual inspection, an
  uncalibrated score is a route for confident errors into a published report.

**What "adequate" means.** Four independent studies put strict top-1 skill linking against
a large occupational vocabulary at **0.23–0.29**, and end-to-end pipeline scores near
**0.56** — and all of them report that ranking is far better than selection (Acc@32 roughly
double Acc@1; MRR 0.82 against F1 0.57). Iris has grounds to expect better, with a
3× smaller candidate space and a whole course description rather than a job-posting span as
input, but must not present its numbers as comparable to theirs. **The consequence is that
the human review screen is a requirement of the method, not a convenience: at these accuracy
levels an unreviewed mapping is not evidence.**

| Stage | Method | Gate |
|---|---|---|
| Text-layer repair | Character-level accuracy on a manually corrected sample | Repair must not introduce errors |
| Section extraction | Course count and field completeness vs manual reading of both documents | All courses found |
| Skill linking | Precision / recall / F1 and Acc@k against expert annotation of a stratified sample of ~50 courses, two annotators. **Multiple correct links per course permitted** — single-gold scoring understates performance. Agreement reported as **Krippendorff's α with the MASI distance**, *not* Cohen's/Fleiss' κ: the task is set-valued, and exact-match κ would score a strict annotator's `{A,B}` against a generous one's `{A,B,C}` as total disagreement | Established before any UI work |
| Out-of-vocabulary | Hold out part of the vocabulary and check the linker declines to link courses that develop it (KB Versioning) | No extra annotation needed |
| Level inference | Agreement with expert-assigned level, as **Krippendorff's α with an *ordinal* distance** — level is `พื้นฐาน < ปานกลาง < สูง`, not a set, so adjacent-level disagreement must count as partial agreement (MASI would discard the ordering). Per-source agreement analysis | Reported honestly, including disagreement |
| **Review-assisted quality** | Annotators act as proxy reviewers over raw model output on a minimal interface; reviewed output scored against the gold standard | **Must beat raw model output**, or the review premise fails |
| **Review throughput** | Decisions per hour, extrapolated to 78 courses | Sustainable in one sitting, or the interface plan changes |
| **Confidence calibration** | Reliability of the confidence score used for bulk-accept | Calibrated before a screen relies on it |
| End-to-end | Runtime on a full 216-page document | Fits an interactive workflow |

⚠️ **The evaluation is single-programme in practice.** Only the SWU document is complete;
the KU file is an excerpt without a curriculum mapping table. A ~50-course stratified
sample drawn from one programme at one university supports claims about *the method*, not
about cross-institution generality — and [[zaki-2023-clo-plo-mapping-automation]] found
5 points of precision variation between two programmes at a *single* institution, purely
from how outcomes are written. Every result carries this limitation until a second
complete document is obtained.

---

## Data

| Source | Type | Volume | Licence / access |
|---|---|---|---|
| Thailand Skill Mapping API | Public open-data JSON | 4,376 skills · 371 careers · snapshot 14 MB | Open, no auth; pinned locally per analysis |
| TQF (มคอ.2) documents | PDF | 2–10 per study | Published by universities; SWU and KU obtained |
| Expert annotation | Manual labels | ~50 courses | Produced by the project |

**Ethics.** No personal data is processed. Job postings are never touched — only
aggregate published statistics. TQF documents are public institutional records.
Programme analyses are published only with the owning department's consent.

---

## Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| **Demand corpus is not Thai-only.** Posting counts range 203 to 6.3 M per career, implausible for Thailand alone; the corpus may be international or cumulative | High | High | Clarify with สป.อว./KMITL before writing methods. If international, reframe claims from "Thai labour market" to "the national standard's reference demand data" — the contribution survives, the wording must not overstate |
| Demand vector truncated at ~100 skills per career | Certain | Medium | Stated as a limitation; no "not demanded" claims; ask whether full vectors are available for research |
| Glyph repair table does not generalise to other producers | Medium | Medium | Validate on a third document from a different producer; the integrity gate fails safe by rejecting rather than silently corrupting |
| `ำ` collapse (KU) is genuinely lossy | Certain for that document | Medium | Lexicon-based restoration; report residual error rate; prefer a better source file |
| Full KU มคอ.2 unavailable — current file is an excerpt without the curriculum map | High | **High** | Request the full document. It blocks three things at once: level inference is evaluable on one programme only, cross-institution generality cannot be claimed, and **UC2 (comparison) — the department's stated motivation for the project — cannot be demonstrated at all** |
| Review does not improve the output, or is too slow to sustain | Medium | **High** | Measured at the Sprint 4 gate on a minimal interface, before the screen is built. If reviewed output does not beat raw output, the design changes rather than the interface |
| Confidence score is uncalibrated while ~70 % of links are bulk-accepted on it | Medium | High | Calibration is a Sprint 4 gate measurement; correction rate monitored per programme before publication |
| Local model too weak for reliable linking | Medium | High | RAG turns the task into constrained selection; if quality is insufficient, escalate model size before changing method — measured at the evaluation gate, not assumed |
| API is beta (0.8.1) and may change | Medium | Low | Snapshots are pinned and versioned; the engine never calls the live API during analysis |
| Single self-hosted server is a single point of failure | Medium | Low | Public site is fully static and unaffected; engine downtime delays new analyses only |
| Thai quality of the Workers AI model is unvalidated | Medium | High | The Sprint 4 gate evaluates the provider that will serve production, not a proxy. If Workers AI models handle Thai adequately the seam pays for itself; if not, local remains primary and the seam still absorbs GPU contention for non-Thai-critical stages |
| Silent provider switching corrupts an analysis | Low, if the rule holds | **High** | Provider is pinned per run and recorded; a quota exhaustion fails the run and requeues rather than switching. Enforced in the engine, not by convention |
| **GPU contention with the lab's other projects, measured in days not hours.** `gpu-linux-server` is shared. The Prostate MRI project trains 5-fold cross-validation at ~30 h per fold — **~150 h for a full run** — holding 7.8 GB of the 24 GB card throughout and leaving 15.4 GB. Folds are run one at a time so projects can interleave, which means the reliable windows are *between* folds. Desktop and X11 hold a further ~1.2 GB permanently | High — it is the normal state, not an incident | **High** | Size model residency for the **contended** case (~15 GB), not the free case, so an analysis does not fail unpredictably when another project is training. Set `OLLAMA_KEEP_ALIVE` explicitly so models release VRAM between runs rather than holding it. Check free VRAM before starting a run and queue rather than fail. Sprints 1–2 need no GPU at all, so ingestion work proceeds regardless |

---

## Alternatives Considered

| Alternative | Why not |
|---|---|
| Continue with an emergent, self-clustered vocabulary | Unstable across runs, no ground truth, and now incompatible with the national standard the sector is adopting |
| Keep scraping job postings | Duplicates published state data, exposes the project to ToS risk, and produces results nobody can reproduce |
| Vector database (pgvector, Qdrant) for skill retrieval | 4,376 fixed vectors fit in 13 MB of RAM; exact search is microseconds. A vector DB solves a scaling problem this design does not have |
| Vision extraction as the *default* path for Thai PDFs | Where damage is glyph substitution, deterministic repair recovers the text exactly, costs nothing and is auditable — properties a model output cannot offer. Vision is the **fallback** for lossy or unusable text layers, not the default (§1) |
| A different extraction engine | poppler, PyMuPDF and xberg return byte-identical damage on the SWU document (134.5 marks per 1,000 Thai chars each). The defect is the PDF's missing `ToUnicode` mapping; no reader can recover what is not there |
| Delegating the integrity decision to a document engine's own quality score | xberg reports `quality_score: 1.0` on a document whose karan is 99 % destroyed. Generic quality metrics do not model Thai diacritic integrity, so an automatic low-quality fallback would never fire |
| Keep the Rust backend | Its concurrency advantage existed for scraping. The remaining work is PDF parsing, Thai NLP, numerics, and evaluation tooling — all Python — and a Rust core would need a Python sidecar anyway |
| Run the engine on CSML | CSML's GPU is contended across the whole department and its availability is outside the project's control. `gpu-linux-server` is **not dedicated either** — it is shared with the lab's other projects — but the contention is *self-scheduled*: the same people decide what runs and when. That is the real distinction, and it is smaller than "dedicated" would imply |
| Expose the analysis API publicly | Unauthenticated GPU access is abuse-prone; the department's faculty are the only intended users at this stage |
| Next.js for the web tier | The public tier is data display; OpenNext machinery is not justified. Astro matches the lab site's existing static-assets-on-Workers deployment |

---

## Open Questions

Blocking the methods section:

- What corpus underlies the demand counts — Thai or international, what window, is `N`
  cumulative? *(external — สป.อว. / KMITL)*
- Is the ~100-skill cap a display limit or a data limit, and can full vectors be
  obtained for research? *(external)*

Empirical, resolved during implementation:

- Does the glyph repair table generalise across PDF producers?
- What retrieval depth `k` balances recall against adjudication cost?
- Which of the three level-inference sources is most reliable, and how often do they
  disagree?
- Can a model that fits the available VRAM adjudicate reliably, given RAG turns the
  task into constrained selection?
- How should skills a course develops that the *standard* does not contain be recorded?

---

_Phase 3 is complete when: this proposal is agreed, the product design is rewritten to
match, and the implementation plan's Sprint 0 can begin._
