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
- [ ] Delete `04-implementation/backend-rust/`, `backend/`, `worker/`, `cluster-sidecar/`,
      `frontend/`, `nginx/`, and the docker-compose files — all belong to the old design
- [ ] Create `04-implementation/engine/` — Python package, ruff, pytest, FastAPI health route
- [ ] PostgreSQL schema + Alembic baseline: `programme`, `course`, `course_skill_link`,
      `analysis_run`, `job`
- [ ] Load the snapshot into the engine as read-only reference data
- [ ] Confirm available VRAM on `linux-gpu-server`; select candidate adjudication and
      embedding models

**Deliverable:** `GET /health` returns 200; the snapshot loads; 4,376 skills queryable.

---

## Sprint 1 — Text-layer integrity gate and glyph repair

**Goal:** turn a damaged TQF PDF into trustworthy Thai text, or refuse it clearly.

- [ ] Thai combining-mark diagnostic — marks per 1,000 Thai characters, per mark, with
      the clean-document baseline (~171 total; per-mark table in `data-feasibility.md`)
- [ ] Classifier: `clean` / `repairable` / `unusable`, with a human-readable report
- [ ] Glyph repair table keyed on `(substitute glyph, preceding character)`, derived from
      the SWU document's substitution set (`2`→้, `=`→์, `‚`→ั, `-`→้, `?`→็, `A`→่, …)
- [ ] `ำ`-collapse restoration via PyThaiNLP lexicon, with a reported residual error rate
- [ ] **Vision fallback** — Typhoon OCR (3B) for documents whose text layer is lossy or
      unusable; flag the document as vision-derived in provenance
- [ ] Evaluate [xberg](https://github.com/xberg-io/xberg) as the OCR orchestration layer
      (fallback chains, confidence thresholds, `vlm` backend for Typhoon, TATR/SLANet
      tables). ⚠️ **Do not use its `quality_score` as the trigger** — it returns 1.0 on the
      SWU document. Iris's diacritic diagnostic drives the fallback
- [ ] Thai-character-proportion check to catch vision language-bias (drift into English)
- [ ] Re-run the gate after repair **and after vision extraction**; fail closed if it still
      does not pass

**Evaluation:** character-level accuracy against a manually corrected 2-page sample from
each document. Repair must not introduce new errors.

**Deliverable:** `iris ingest --check <pdf>` prints a diagnosis; repaired text for SWU
passes the gate; the KU excerpt passes via the vision path.

> ⚠️ Validate the repair table against a **third** TQF document from a different producer
> before treating it as general.

---

## Sprint 2 — Document navigation and course extraction

**Goal:** a TQF PDF becomes a complete, provenance-carrying list of courses.

- [ ] PageIndex tree build over a มคอ.2; verify node titles and page ranges
- [ ] Locate `3.1.5 คำอธิบายรายวิชา`, the curriculum mapping table, and the programme ELO list
- [ ] Exhaustive section parsing — course code, Thai title, English title, credits
      `x(y-z-w)`, category, Thai description, English description where present
- [ ] Parse the curriculum mapping table into `(course, outcome, ● | ○)` triples
- [ ] Parse per-course CLOs where the document provides them (SWU ชุดรายวิชา format)
- [ ] Every extracted field records its source page

**Evaluation:** course count and field completeness against manual reading of both
documents — SWU (78 codes seen) and KU (67). Every course must be found.

**Deliverable:** `iris ingest <pdf>` writes a complete programme to the database.

---

## Sprint 3 — Skill linking

**Goal:** each course carries a set of national skill IDs with evidence.

- [ ] Embed skill titles + definitions once; hold as a 13 MB in-memory matrix
- [ ] Hybrid candidate retrieval — dense cosine plus lexical, tuned for tool names
- [ ] LLM adjudication: given a course description and ~30 candidate skills with their
      definitions, select those the course develops; Pydantic-constrained to valid IDs
- [ ] Bilingual channel — link Thai and English descriptions independently where both
      exist; record agreement as a confidence signal
- [ ] Record evidence span and retrieval rank for every accepted link
- [ ] **Out-of-vocabulary as an explicit output**, not a similarity threshold — record
      skills a course appears to develop that the standard does not contain
- [ ] Synonym enhancement from the three surface forms per skill (Thai title, English
      title, Thai definition)

**Evaluation:** retrieval recall@k on a small labelled set, to fix `k` before adjudication
cost is spent.

**Deliverable:** `iris link <programme>` produces course → skill links with evidence.

---

## Sprint 4 — 🚧 EVALUATION GATE 🚧

**Goal:** know how good the linking is. **Nothing downstream starts until this passes.**

- [ ] Stratified annotation sample: ~50 courses across core / elective / general education
- [ ] Annotation guideline written from the standard's own skill definitions
- [ ] **Two annotators**, independently; inter-annotator agreement reported —
      **multiple correct links per course permitted**, since single-gold scoring understates
      performance
- [ ] Precision / recall / F1 **and Acc@k** for linking; error taxonomy (missed, spurious,
      wrong-sense)
- [ ] **Out-of-vocabulary evaluation via KB Versioning** — hold out part of the vocabulary,
      check the linker declines to link courses that develop it. No extra annotation
- [ ] Ablations: dense-only vs hybrid retrieval; Thai-only vs bilingual; `k` sensitivity;
      model size; **supervised ranker vs LLM adjudicator**
- [ ] Prompt revision driven by the error taxonomy, re-measured on a held-out split

**Gate:** linking quality is documented, reproducible, and adequate for the claims the
paper intends to make. If it is not, iterate here — do not proceed.

**Reference points from the literature** (Acc@1 0.23–0.29, end-to-end ≈0.56, and ranking
consistently far ahead of selection). Iris has grounds to expect better — a 3× smaller
vocabulary and a whole course description as input — but its numbers are not directly
comparable and must not be reported as such. The same evidence is why the review screen in
Sprint 9 is a requirement rather than a convenience.

**Deliverable:** an evaluation report in `05-reports/`, and the annotated set committed
as a reusable benchmark.

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

- [ ] Programme profile aggregation — credit-weighted, level-aware, category-aware
- [ ] Load career demand from the snapshot; **filter the 168 `count = 0` pairs and the
      three degenerate careers**
- [ ] Level-aware coverage gap (primary metric), prevalence-weighted
- [ ] RCA career-specificity weighting
- [ ] Growth-adjusted view from `skillsGrowth`
- [ ] KL divergence as a secondary metric, with explicit renormalisation from prevalence
      and a stated interpretation
- [ ] Programme-to-programme comparison — shared / A-only / B-only / different-level
- [ ] **Truncation guard**: no output may assert that a career does not demand a skill

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

- [ ] Cloudflare Tunnel from `linux-gpu-server`; verify it survives a reboot
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
| VRAM available on `linux-gpu-server` | — | Model selection in Sprint 0 |
| Second annotator | department | Sprint 4 gate |

---

## Conventions

- All LLM calls go through one client module — single place for endpoint, retries, and
  prompt logging. **Every prompt and response is logged**; the paper needs them
- Analysis code never calls the live API; it reads the pinned snapshot
- Metric functions are pure and unit-tested against hand-computed values
- Anything asserting what the market does or does not demand passes the truncation guard
- The result schema is versioned; the web tier declares which version it reads
