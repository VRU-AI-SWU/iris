# Iris — Phase 4 Implementation Plan

> Rewritten 2026-08-27. Supersedes the 2026-04-30 plan, whose sprints were built around
> job-board scrapers and vocabulary clustering — neither of which exists in the current
> design. Aligned with [`solution-proposal.md`](03-solution-design/solution-proposal.md)
> and [`tech_stack.md`](tech_stack.md).

---

## What went wrong last time, stated plainly

The previous plan opened with the principle *"build pipeline-first: validate skill
extraction on real TQF documents before building the web layer."* Sprints 0–6 were then
built — scaffold, ingestion, vocabulary, scrapers, gap engine, reports, and a backend
migration to Rust — **without a single measurement of extraction quality on a real
document.** The project stalled three months later with a 26-line frontend, two parallel
backends, and 900 MB of build artefacts in git.

This plan is ordered so that cannot happen again. **Sprint 4 is a gate, not a
checkpoint.** No user-facing work starts until linking quality is measured on real
documents against expert annotation. If quality is inadequate, the response is to fix
the method — not to proceed and hope the UI distracts from it.

---

## Principles

- Every sprint ends with something runnable and a number that says how well it works
- The engine reads a **pinned** snapshot of the national standard, never the live API
- Provenance is carried end to end: every linked skill traces to a course, a page, and a
  text span
- Measure before assuming — model size, retrieval depth, and level-inference reliability
  are all empirical questions with sprints attached
- The public web tier must never depend on the engine being reachable

---

## Sprint 0 — Ground clearing

**Goal:** a clean repository and a running skeleton.

- [x] Strip 3,942 committed Rust build artefacts from history (`.git` 289 MB → 27 MB)
- [x] Pin the national standard snapshot (`data/skillmapping/2026-08-27/`)
- [x] Record what the data actually supports (`03-solution-design/data-feasibility.md`)
- [x] Delete `04-implementation/backend-rust/`, `backend/`, `worker/`, `cluster-sidecar/`,
      `frontend/`, `nginx/`, and the docker-compose files — all belong to the old design
- [x] Create `04-implementation/engine/` — Python 3.13 package, ruff, pytest, FastAPI
      `/health`, and an `iris` CLI (the pipeline is CLI-driven through Sprint 7)
- [x] Schema + Alembic baseline: `programme`, `course`, `course_skill_link`,
      `out_of_vocabulary_skill`, `analysis_run`, `job`
- [x] Load the snapshot into the engine as read-only reference data, with the design's
      data-quality filters applied on load and **reported, never silent**
- [x] 23 tests, all passing; ruff clean
- [x] Confirm host capability on `gpu-linux-server`: RTX 3090 24 GB (driver 580.173.02),
      **15.4 GB free**, Ollama running with no models pulled, 193 GB disk, Python 3.12.3
- [x] Verify the engine runs on the host's Python 3.12 — 23 tests pass on 3.12.13
- [x] Account for the ~9 GB of held VRAM: a Prostate MRI training run holds 7.8 GB
      (~2 days remaining), desktop and X11 hold ~1.2 GB permanently. Nothing stale
- [ ] Set `OLLAMA_KEEP_ALIVE` explicitly (currently unset → 5-minute default)
- [ ] Pull and smoke-test candidate models — **deferred until the training run finishes**,
      to avoid competing for VRAM with the lab's other project. The decision itself belongs
      to the Sprint 4 gate regardless

> ⚠️ **`gpu-linux-server` is shared, and the contention lasts days.** The lab's Prostate
> MRI project trains 5-fold CV at ~30 h per fold, ~150 h for a full run, holding 7.8 GB
> throughout. Folds are launched one at a time so the projects can interleave, so the
> dependable windows for work needing the whole card are *between folds*.
>
> Model residency is sized for the *contended* case (~15 GB), not the free case (~23 GB).
> **Sprints 1 and 2 need no GPU at all.** For Sprint 3, the Workers AI provider seam is the
> answer rather than waiting — which is the case for building it early rather than
> retrofitting it.

**Deliverable:** ✅ `GET /health` returns 200 and reports snapshot provenance; the snapshot
loads; 4,376 skills queryable; 12 seniority ladders computed.

**Decision taken during the sprint.** Models use generic SQLAlchemy types and run on
**SQLite in development, PostgreSQL in production**. Sprints 1–7 are ingestion and
evaluation work that should not require a database server to be running; `DATABASE_URL`
points at PostgreSQL on the deployment host. No PostgreSQL-specific column type is used.

**Feedback to the design.** The loader found that **13 seniority pairs exist but only 12
are analysable** — `senior-frontend-developer` has 5 skills and is caught by the
degenerate-career filter. The solution proposal, product design, `CLAUDE.md` and
`q-prevalence-metrics` were corrected in the same commit, per the feedback-loop rule.

---

## Sprint 1 — Text-layer integrity gate and glyph repair ✅

**Goal:** turn a damaged TQF PDF into trustworthy Thai text, or refuse it clearly.

🟢 **No GPU required for the main path.** The diagnostic, the repair and the gate are
pure CPU work. Only the vision fallback needs the card.

- [x] Thai combining-mark diagnostic — total rate and per-mark rate per 1,000 Thai
      characters, against the 171.0 clean-document baseline
- [x] Classifier: `clean` / `repairable` / `lossy` / `unusable`, with a human-readable
      report — plus `repaired`, the state a document reaches after a successful repair
- [x] **Repair table learned from the document, not hard-coded.** A substituted glyph is
      whichever combining mark turns the word it sits in into a real Thai word; longest
      match wins; votes aggregate per `(font, glyph)`; rounds iterate as density falls
- [x] `ำ`-collapse detection, above a length threshold so narrow vocabulary is not
      mistaken for damage
- [x] Re-run the gate after repair; fail closed if it still does not pass
- [x] `iris check <pdf>` — diagnosis, repair, and the re-run gate
- [x] **Sara-am normalisation** — reverses `ํ`+`า` (Adobe) and consonant+space+`า`
      (MS Word) with no learned table, because Thai orthography determines the answer
- [x] **Validated on five universities and five PDF producers** — see below
- [ ] Vision fallback via Typhoon OCR ⚠️ blocked on GPU, **and no longer on the critical
      path**: every document in the corpus reaches a usable text layer without one
- [ ] Thai-character-proportion check for the vision path's language-bias failure
      *(deferred with the vision path)*

**Measured on five universities, five PDF producers:**

| University | Pages | Producer | Raw | After normalise | After repair |
|---|---|---|---|---|---|
| CMU | 148 | MS Word 2016 | `lossy` | **`clean`** 188.0 | — |
| KU | 28 | MS Word 2013 | `lossy` | **`clean`** 171.0 | — |
| PSU | 229 | macOS Quartz | `repairable` | `repairable` | **`clean`** 175.7 · 83%, 38 rules |
| SU | 254 | Adobe Acrobat Pro | `repairable` | `repairable` | **`clean`** 173.8 · 96%, 14 rules |
| SWU | 216 | Bullzip PDF Printer | `repairable` | `repairable` | **`clean`** 162.9 · 92%, 13 rules |

**Three unrelated damage alphabets with no overlap between the learned tables** — Bullzip
substitutes ASCII (`2`, `=`, `?`), macOS Quartz substitutes a different ASCII set (`b`,
`X`, `F`, `@`), Adobe emits Unicode PUA (`\uf70b`, `\uf70a`). None hard-coded.

Words a reader can verify recovered: `ข้อมูล`, `คอมพิวเตอร์`, `ผลการเรียนรู้`,
`หน่วยกิต`, `เป็น`, `วิเคราะห์`, `สำหรับ`, `จำนวน`, `กำหนด`.

**Deliverable:** ✅ `iris check` diagnoses both documents correctly and routes each to the
right path. 36 tests pass; ruff clean.

**Found during the sprint.**

1. **Per-mark rates are vocabulary-dependent and cannot drive the verdict.** A
   computer-science curriculum uses karan far more than the KU document the baseline came
   from, so `์` sitting below baseline may mean different content rather than lost marks.
   The verdict now rests on the *total* rate and the *intrusion count*, both robust to
   vocabulary; per-mark retention is reported to localise damage for a human, and decides
   nothing. The first version of the gate had this wrong and called a successfully
   repaired document `lossy`.
2. **"No `ำ` means collapse" needs a length threshold.** `คอมพิวเตอร์ ซอฟต์แวร์
   อิเล็กทรอนิกส์` legitimately contains none. The inference is statistical, not logical,
   and now requires 5,000 Thai characters before it fires. A test caught this.
4. **~400 intrusions remain unrepaired** on SWU, led by `.`×178 and `/`×69 — mostly
   legitimate punctuation rather than damage. Reported, never forced.
5. 🔄 **The KU document is not lossy, and the feasibility study was wrong to say so.**
   `pdftotext -layout` renders `ค าอธิบาย` as `คาอธิบาย`, which read as a collapse.
   Character-level extraction shows a **space** where `ำ` belongs — the position survives,
   and since `า` cannot begin a syllable, a space before it is always an artefact. KU and
   CMU both normalise to clean. Corrected in `data-feasibility.md` and the proposal.
6. **Verdict ordering was wrong twice.** Intrusions are evidence of substitution *only
   when marks are missing to explain*; a document at full mark rate with ASCII inside Thai
   words has punctuation, not damage. Judging on intrusions first classified two intact
   documents (CMU at 188.0, PSU at 175.7) as damaged.

> ✅ **Generality validated.** The method was tested against five documents from five
> distinct PDF producers with three unrelated damage alphabets, and learned a working table
> for each without a hard-coded rule. The corpus lives in `data/programmes/` (git-ignored —
> institutional documents).

---

## Sprint 2 — Course extraction 🔄

**Goal:** a TQF PDF becomes a complete, provenance-carrying list of courses.

- [x] **Anchor on the TQF credit specification** `x(y-z-w)` rather than on a section
      heading. Every course in every document carries one, it is language-independent, and
      PSU's `3((2)-2-5)` is the only formatting variant in the corpus
- [x] **Learn each document's course-code shape** by scoring six candidates against the
      anchors — same principle as the repair table
- [x] Extract code, Thai title, English title, credits, description, source page
- [x] **Prose-aware deduplication** — a course appears in the structure tables, the study
      plan and the description section; the entry whose body reads as prose wins
- [x] `iris courses <pdf>`
- [x] **Parse the curriculum-responsibility matrix into `(course, outcome, ● | ○)`** —
      positionally, since the marks are Wingdings glyphs invisible to text extraction
- [x] `iris map <pdf>`
- [x] **Parse per-course CLOs** and the leading verb that carries their cognitive demand
- [x] `iris clo <pdf>`
- [ ] Recover the ~30% of PSU courses whose descriptions are not being found
- [ ] Extend matrix extraction to CMU and PSU (row labels are not course codes there)

**Measured across the corpus — 350 courses with real Thai descriptions:**

| University | Code shape learned | Courses | With English title | With Thai prose |
|---|---|---|---|---|
| CMU | `digits-6` | 91 | 89 | 86 |
| KU | `digits-8` | 64 | 63 | 64 |
| PSU | `hyphen-3-3` | 150 | 77 | **36** ⚠️ |
| SU | `spaced-3-3` | 93 | 93 | 92 |
| SWU | `thai-prefix` | 73 | 70 | 72 |

**Deliverable:** 🔄 `iris courses` extracts a provenance-carrying course list from all
five documents. 72 tests pass; ruff clean.

**Why heading-based location was abandoned.** Only two of five documents contain the
literal `3.1.5 คำอธิบายรายวิชา`. PSU numbers it `4.`, SU omits the number entirely, and
**CMU calls courses `กระบวนวิชา` rather than `รายวิชา`**. The regulated thing is the
credit specification, not the heading — so that is what the extractor anchors on, and
PageIndex is not needed for this step.

**Course learning outcomes — the second level-inference input:**

SWU is the only fully outcome-based document in the corpus. It yields **116 outcomes,
108 tied to a course across 37 courses, 94 with a leading verb**, in a table printed
sideways whose columns are named by its own header
(`ชุดรายวิชา | คำอธิบายรายวิชา | CLOs | MLOs | ELOs`).

The verb distribution is what level inference will read:

| band | count | example |
|---|---|---|
| understand | 42 | `อธิบายหลักการของอัลกอริทึม` |
| apply | 21 | `ประยุกต์ใช้วิธีการพัฒนาระบบ` |
| create | 15 | `ออกแบบฐานข้อมูล` |
| analyse | 9 | `วิเคราะห์หาความต้องการระบบ` |
| evaluate | 6 | |
| recall | 1 | |

The banding is **evidence, not a level** — mapping it onto the standard's
`พื้นฐาน / ปานกลาง / สูง` is an open question for the Sprint 4 gate, not a decision taken
in the extractor.

**Curriculum-responsibility matrix — the level-inference input:**

| University | Marks assigned | Courses × outcomes | Notes |
|---|---|---|---|
| **SWU** | **646 / 700 (92%)** | 50 × 18 | outcomes labelled `1.1`–`5.2`; **412 ● / 234 ○** |
| SU | 313 / 582 (54%) | 82 × 10 | outcome header not found, columns unlabelled; all marks read as primary |
| CMU, PSU | — | — | matrix pages found, but row labels are not course codes |
| KU | — | — | 28-page excerpt, no matrix — reported as absent, not guessed |

Two things are measured rather than assumed, because both vary by producer:

- **Which glyph means which.** SWU draws ● as Wingdings2 `\x01` and ○ as Wingdings
  `\uf0a1`; SU uses `\uf098`; CMU `\uf050`. Instead of carrying a font table, each glyph
  is **rendered and its ink coverage measured** — a filled circle covers roughly twice the
  area of a hollow one (SWU: 0.108 vs 0.076).
- **Page rotation.** SWU prints the matrix sideways, so reading order and coordinate axes
  do not coincide.

Outcome columns come from clustering the *marks* by position, not from the header labels —
producers pack the whole header row (`1.1 1.2 … 5.2`) into a single text span, so per-column
positions cannot be read from it.

**Open.**

1. ⚠️ **PSU finds only 36 usable descriptions from 150 codes.** Its layout puts curriculum-
   map rows adjacent to credit specs, and its code list includes service courses from other
   faculties. The other four documents are at 86–100%.
2. 🔄 **Positional extractors were bypassing the repair pipeline.** They read spans
   directly rather than the flat character stream, so verbs arrived as `ประยุกต=` and 44 %
   of verb matches were lost. Fixed by a shared `repaired_lines` reader — which then had
   to be made **intrusion-aware**: applying the table to every character turned the course
   code `คพ242` into `คพ้4้`, because SWU's table maps `2` to `้`. Substitution now happens
   only where a character has Thai on both sides, the same rule the main repair uses.
   Caching the reader took a run from 12.6 s to 0.1 ms.
3. **Marks lost as whitespace are not recovered.** SWU drops some mai ek into a space —
   `ไม่น้อยกว่า` extracts as `ไม น้อยกว า`. Unlike the sara-am case, **no orthographic
   constraint makes recovery safe**: Thai uses spaces as phrase separators, and `ไม` (silk)
   is as real a word as `ไม่` (not), so a wrong repair changes meaning. Measurement found
   the candidate detections to be almost entirely false positives. Deliberately not
   attempted; whether the residue affects linking is a Sprint 4 measurement, not a guess.

---

## Sprint 3 — Skill linking

**Goal:** each course carries a set of national skill IDs with evidence.

- [x] **Lexical retrieval first** — BM25 over three surface forms per skill, plus a
      consonant-skeleton channel for the tone-mark damage Sprint 2 deliberately left
      unrepaired. Needs no model, so it gives a baseline before any GPU is available.
      Measured on a 6-course development set: **recall@10 75 %, @50 83 %** (67 % / 75 %
      without the skeleton channel). `k = 30` carried forward
- [ ] Embed skill titles + definitions once; hold as a 13 MB in-memory matrix
- [ ] Hybrid candidate retrieval — add dense cosine to the measured lexical baseline
- [x] LLM adjudication: given a course description and ~30 candidate skills with their
      definitions, select those the course develops; JSON-schema-constrained, and a
      selection outside the shortlist is rejected rather than repaired
- [ ] Bilingual channel — link Thai and English descriptions independently where both
      exist; record agreement as a confidence signal
- [x] **Provider seam** — one provider-blind interface over a local OpenAI-compatible
      endpoint and Cloudflare Workers AI. Port the quota handling from Argus
      `server/llm.ts`: a `code:4006` 429 is quota exhaustion and must never be retried;
      other retryable statuses get backoff honouring `Retry-After`
- [x] **Pin the provider per run.** No mid-run fallback — quota exhaustion fails the run
      and requeues on the other provider from the start. Record provider + model on
      `analysis_run`
- [x] **Model selected on measurement:** `iris-adjudicator` (`qwen3:8b`, `num_ctx 8192`,
      `temperature 0`) — 6.6 GB resident against 10.0 GB at Ollama's default context,
      ~4.2 s per course. ⚠️ Reasoning must be disabled (`reasoning_effort: "none"`) or the
      answer arrives empty; a truncated completion is a **failure**, never a zero-link
- [x] Record evidence span and retrieval rank for every accepted link, and **verify the
      span occurs in the course text** — folding Thai whitespace and combining marks, so
      the damage Sprint 2 leaves unrepaired does not reject real provenance
- [ ] **Out-of-vocabulary as an explicit output**, not a similarity threshold — record
      skills a course appears to develop that the standard does not contain.
      ⚠️ Decided **per skill after decomposition, never per course title**: measured
      2026-08-31, the vocabulary has no entry named *วิศวกรรมซอฟต์แวร์* but 46 `Software *`
      skills the course develops. See `q-out-of-vocabulary`
- [x] Synonym enhancement from the three surface forms per skill (Thai title, English
      title, Thai definition)
- [ ] Bilingual channel and the supervised ranking baseline — carried into Sprint 4

**Evaluation:** retrieval recall@k on a small labelled set, to fix `k` before adjudication
cost is spent. ✅ *Done for the lexical channel; re-run when the dense half lands.*

**Deliverable:** `iris link <programme>` produces course → skill links with evidence.

---

## Sprint 4 — 🚧 EVALUATION GATE 🚧

**Goal:** know how good the linking is **and whether reviewing it helps**. Nothing
downstream starts until this passes.

The gate has two halves. Iris's deliverable is *reviewed* links, so measuring the model
alone would pass the gate on a number that is not the product's quality — and would leave
the review premise untested until Sprint 9, after everything has been built on it. The
second half is nearly free: the annotators are already performing the reviewer's task.

### 4a — Model quality

- [ ] Stratified annotation sample: ~50 courses across core / elective / general education.
      ⚠️ **Blocked on a Sprint 2 gap:** SWU yields 73 courses with descriptions (62 `คพ`,
      11 general education), but nothing yet extracts *which major courses are core and
      which are elective* — that lives in the programme-structure section, not the course
      catalogue. Either extract it or have the domain expert mark it once by hand
- [x] Annotation guideline written from the standard's own skill definitions —
      [`04-implementation/annotation/annotation-guideline.md`](04-implementation/annotation/annotation-guideline.md),
      in Thai, for departmental faculty.
      🔴 **It must state the three rules Sprint 3's development set violated:** labels are
      derived exhaustively from the *description text* (a course names more skills than its
      title suggests); labels are fixed **before** any model output is seen; multiple
      correct links per course are permitted. Scoring against a narrow single-gold set gave
      a precision figure that reading the source text showed to be simply wrong
- [ ] **Two annotators**, independently; **multiple correct links per course permitted**,
      since single-gold scoring understates performance
- [ ] Agreement computed as **Krippendorff's α with the MASI distance** (Jaccard ×
      monotonicity) — ⚠️ *not* Cohen's or Fleiss' κ. The task is set-valued, so exact-match
      κ scores `{A,B}` vs `{A,B,C}` as total disagreement, and that subset pattern is the
      *expected* form of disagreement between a strict and a generous annotator
- [ ] Precision / recall / F1 **and Acc@k** for linking; error taxonomy (missed, spurious,
      wrong-sense)
- [ ] **Out-of-vocabulary evaluation via KB Versioning** — hold out part of the vocabulary,
      check the linker declines to link courses that develop it. No extra annotation
- [ ] Ablations: dense-only vs hybrid retrieval; Thai-only vs bilingual; `k` sensitivity;
      model size; **supervised ranker vs LLM adjudicator**
- [ ] Prompt revision driven by the error taxonomy, re-measured on a held-out split
- [ ] Level agreement as **Krippendorff's α with an *ordinal* distance** — ⚠️ not MASI:
      level is ordinal (`พื้นฐาน < ปานกลาง < สูง`), so adjacent-level disagreement must
      count as partial agreement

### 4b — System quality *(minimal interface, not the Sprint 9 screen)*

- [ ] Minimal review surface — a spreadsheet or CLI listing proposed links with skill
      definition, evidence span, level and confidence. **Deliberately not the real screen**:
      the point is to test the premise before designing the interface
- [ ] **Review-assisted quality** — annotators review raw model output; the reviewed result
      is scored against the gold standard
- [ ] **Throughput** — decisions per hour, extrapolated to a 78-course programme
      (624–1,092 decisions; 104–182 min at 10 s each if every link is inspected)
- [ ] **Confidence calibration** — are high-confidence links right at close to their stated
      confidence? Load-bearing, because hitting the 90-minute target requires bulk-accepting
      ~70 % of links on that score
- [ ] Record which confidence components carry the signal — retrieval rank, Thai/English
      channel agreement, level-source agreement
- [ ] ⚠️ **Evaluate the provider that will serve production.** If Workers AI is primary,
      the gate measures the Workers AI model. Measuring local and shipping Workers AI would
      invalidate every number the paper reports

**Gate — both halves:**
1. Linking quality is documented, reproducible, and adequate for the intended claims
2. **Reviewed output beats raw model output.** If it does not, the review premise is wrong
   and the *design* changes, not the interface
3. Throughput is sustainable, or the interface plan changes before Sprint 9 builds it

If any fails, iterate here — do not proceed.

**Reference points from the literature** (Acc@1 0.23–0.29, end-to-end ≈0.56, and ranking
consistently far ahead of selection). Iris has grounds to expect better — a 3× smaller
vocabulary and a whole course description as input — but its numbers are not directly
comparable and must not be reported as such. The same evidence is why the review screen in
Sprint 9 is a requirement rather than a convenience.

**Deliverable:** an evaluation report in `05-reports/` covering both halves, and the
annotated set committed as a reusable benchmark. The Sprint 9 review screen is then built
against a measured throughput baseline rather than a guess.

---

## Sprint 5 — Level inference

**Goal:** links carry a proficiency level, justified by evidence.

- [ ] Level assignment from CLO text matched against the skill's own level criteria
- [ ] Level signal from the curriculum mapping table (● vs ○)
- [ ] Level signal from curriculum position — year from course code, prerequisite depth
- [ ] **Non-LLM baseline: a verb-feature classifier over CLO text.** Zero-shot LLM Bloom
      classification measures at 0.72–0.73 against 94% for a classical model on the same
      data — this baseline may win, and that must be found out before an LLM-only path is built
- [ ] Combine the sources; **record disagreement rather than silently resolving it**
- [ ] Report per-source reliability and disagreement rate. The ● / ○ matrix reconstructs at
      only 83–88% against domain experts — treat it as evidence, not ground truth

**Evaluation:** agreement with expert-assigned level on the Sprint 4 sample.

> ⚠️ Blocked on obtaining the **full KU มคอ.2** — the current file is an excerpt with no
> curriculum mapping table, so this is evaluable on one programme until it arrives.

**Deliverable:** `course_skill_link.level` populated with per-source provenance.

---

## Sprint 6 — Alignment engine

**Goal:** a programme profile compared against a career's published demand.

- [ ] Programme profile aggregation — `level` = **max** over linking courses;
      `depth` = course count and total credits; both recorded per skill
- [ ] Load career demand from the snapshot; **filter the 168 `count = 0` pairs and the
      three degenerate careers**
- [ ] **Prevalence-weighted coverage gap (primary metric)** — ⚠️ *not* a level shortfall:
      the demand side carries no required level (see `data-feasibility.md`)
- [ ] **Seniority gradient** — Δ prevalence between paired career rungs (13 pairs;
      `data-scientist` has four). Cross with curriculum level to produce the report's
      strongest finding. Mark clearly in output when a target career has no pair
- [ ] RCA career-specificity weighting — **career-equal global denominator**, stated in
      output; count-weighted reported as a sensitivity check (top-15 overlap is only 8/15
      between the two, so this is not a free choice)
- [ ] Growth-adjusted view from `skillsGrowth`
- [ ] KL divergence as a secondary metric, with explicit renormalisation from prevalence
      and a stated interpretation
- [ ] Programme-to-programme comparison — shared / A-only / B-only / different-level
- [ ] **Truncation guard**: no output may assert that a career does not demand a skill
- [ ] **Level guard**: no output may state or imply a level the market requires

**Evaluation:** unit tests with known distributions and hand-computed expected values.

**Deliverable:** `iris analyse <programme> --career <slug>` returns a ranked, level-aware
gap table.

---

## Sprint 7 — Reports and the publish contract

**Goal:** results a curriculum committee can read, and a versioned artefact the web can consume.

- [ ] Heatmap data structure — courses × skills, level-shaded
- [ ] Ranked gap table with course traceability and source page references
- [ ] Narrative summary generated under a template that cannot overstate truncated data
- [ ] HTML report; PDF export via WeasyPrint
- [ ] **Versioned result schema** — the contract between engine and web; changes are
      versioned, never silent
- [ ] `iris publish <analysis>` emits the JSON the web tier builds against

**Deliverable:** a complete report for the SWU programme against a chosen digital career.

---

## Sprint 8 — Public web tier

**Goal:** the project is visible at `vru-ai.com/iris`.

- [ ] Astro site, deployed as static assets on Cloudflare Workers, matching `vru-ai-web`
- [ ] Project overview page — the research, the method, the limitations
- [ ] Published analysis views: programme profile, alignment heatmap, ranked gaps, narrative
- [ ] Programme comparison view
- [ ] PDF download
- [ ] Reads **build-time JSON** — no backend dependency

**Deliverable:** published results are browsable publicly; the site is fully functional
with the engine switched off.

---

## Sprint 9 — Gated analysis application

**Goal:** department faculty can ingest and analyse a programme themselves.

- [ ] Cloudflare Tunnel from `gpu-linux-server`; verify it survives a reboot
- [ ] Cloudflare Access policy — department faculty allowlist
- [ ] Upload → job → progress → result flow
- [ ] Skill-link review screen: accept / reject / adjust level, with the evidence span shown
- [ ] Curriculum revision scenario (UC3)
- [ ] Publish action — promotes a reviewed analysis to the public site
- [ ] Rate limiting and upload validation

**Deliverable:** a faculty member uploads a มคอ.2 and reads a report without touching a terminal.

---

## Sprint 10 — Hardening and write-up

- [ ] End-to-end runtime on the full 216-page document
- [ ] Failure paths: model unavailable, unusable PDF, malformed section, empty description
- [ ] Reproducibility check — a pinned snapshot plus a document yields identical results
- [ ] Methods section: snapshot date, model, prompts, annotation protocol, agreement
- [ ] Limitations section: demand-vector truncation, corpus provenance, `ำ` restoration error
- [ ] Operational notes — backup, tunnel recovery, snapshot refresh

---

## Sequencing

```
S0 ── S1 ── S2 ── S3 ── S4 GATE ── S5 ── S6 ── S7 ─┬─ S8  web (public)
     ground   ingest   link   evaluate  level  gap  │
     truth                                     report└─ S9  app (gated) ── S10
```

Sprints 8 and 9 may run in parallel once the Sprint 7 result schema is fixed. **Nothing
from Sprint 5 onward begins before the Sprint 4 gate passes.**

---

## External dependencies

| Needed | From | Blocks |
|---|---|---|
| Full KU มคอ.2 (current file is an excerpt) | KU | Sprint 5 evaluation breadth |
| Provenance of the demand corpus — Thai or international, window, whether `N` is cumulative | สป.อว. / KMITL | Methods section wording |
| Whether the ~100-skill cap is a display or data limit | สป.อว. / KMITL | Strength of gap claims |
| A third TQF from a different PDF producer | any Thai university | Generality of the glyph repair table |
| VRAM available on `gpu-linux-server` | — | Model selection in Sprint 0 |
| Second annotator | department | Sprint 4 gate |

---

## Conventions

- All LLM calls go through one client module — single place for endpoint, retries, and
  prompt logging. **Every prompt and response is logged**; the paper needs them
- Analysis code never calls the live API; it reads the pinned snapshot
- Metric functions are pure and unit-tested against hand-computed values
- Anything asserting what the market does or does not demand passes the truncation guard
- The result schema is versioned; the web tier declares which version it reads
