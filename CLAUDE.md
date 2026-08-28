# Project Iris — Curriculum Skill Alignment

## Overview

Iris expresses a Thai university curriculum in the vocabulary of the **national
Thailand Skill Mapping standard** (สป.อว. / KMITL), so it can be compared against the
skill demand that standard publishes for each career.

It reads a TQF (มคอ.2) document, links each course to the national skill vocabulary
**at an inferred proficiency level**, and reports which skills a target career demands
that the curriculum does not develop — plus, for the 13 seniority-paired careers, which
skills gain prominence with experience and how deeply the curriculum develops those.

## Current Phase

**Phase 4 — Implementation, Sprint 0.** Phase 3 was rewritten 2026-08-27 after a pivot;
Phase 2 is being updated to match.

## The pivot (2026-08-27) — read this before touching anything

The design before this date assumed Iris would build its own skill vocabulary by
clustering extracted terms, and measure demand by scraping four Thai job boards. The
national standard supersedes both. **If you find a document or a code path that assumes
scraping, HDBSCAN clustering, an emergent vocabulary, `pgvector`, Celery/Redis, Apalis,
or the chaiaroon-2025 20-role taxonomy, it is stale.**

Removed: job-board scrapers · emergent vocabulary construction · clustering sidecar ·
vector database · heavy job queue · the Rust backend · the Next.js scaffold.

Added: level-aware linking against a fixed controlled vocabulary · a Thai PDF integrity
gate · PageIndex document navigation · a two-surface Cloudflare deployment.

## Canonical documents

Read in this order. Where they disagree, the feasibility study wins — it is the only one
grounded in measurement.

| Document | Contains |
|---|---|
| [`03-solution-design/data-feasibility.md`](03-solution-design/data-feasibility.md) | What the standard and the real TQF documents actually support. **Read first** |
| [`03-solution-design/solution-proposal.md`](03-solution-design/solution-proposal.md) | Architecture, method, evaluation, risks |
| [`03-solution-design/product-design.md`](03-solution-design/product-design.md) | Surfaces, personas, screens |
| [`tech_stack.md`](tech_stack.md) | Stack and decision log |
| [`implementation_plan.md`](implementation_plan.md) | Sprint order and the evaluation gate |

## Architecture in one picture

```
Cloudflare · vru-ai.com/iris
  ├─ public   Astro static · published results · no backend
  └─ /app     Cloudflare Access → Tunnel → linux-gpu-server (office, 24/7)
                                            FastAPI · PostgreSQL · local LLM
```

The engine publishes versioned result documents; the web tier only reads them.

## Non-negotiables

1. **The evaluation gate (Sprint 4) blocks everything after it.** The previous phase
   declared a pipeline-first principle, built six sprints without measuring extraction
   quality once, and stalled. Do not repeat it.
2. **Analyses read a pinned snapshot, never the live API.** The upstream is beta and its
   data will change; reproducibility is a publication requirement.
3. **Never assert that a career does not demand a skill.** The published demand vector is
   truncated at ~100 skills per career. Absence means below the cut-off. This is enforced
   in the narrative template, not left to judgement.
4. **`percentage` is prevalence, not a distribution share.** Any distributional metric
   requires explicit renormalisation and a stated change of interpretation.
5. **Levels exist on the curriculum side only.** The demand side carries `count` and
   `percentage` and nothing else — no required level per career × skill. Never state or
   imply a proficiency level the market requires. The demand-side depth signal is the
   **seniority gradient** across the 13 paired careers, which measures which skills gain
   prominence with experience, not how deeply they are required.
6. **Provenance end to end.** Every linked skill traces to a course, a page, and a text
   span. Committee members will challenge specific assignments.
7. **Show disagreement.** Where level-inference sources conflict, surface the conflict.
8. **No vector database.** 4,376 fixed entries is a 13 MB in-memory matrix.

## Key concepts

- **National skill vocabulary** — 4,376 skills, each with a Thai definition and three
  proficiency levels (`ระดับพื้นฐาน` / `ระดับปานกลาง` / `ระดับสูง`) with explicit criteria
- **Skill linking** — mapping free Thai course-description text to skill IDs in that fixed
  vocabulary. This is entity linking, not open extraction
- **Level inference** — assigning a proficiency level from CLOs, the curriculum mapping
  table (● ความรับผิดชอบหลัก / ○ ความรับผิดชอบรอง), and curriculum position
- **Text-layer integrity gate** — Thai combining-mark rate per 1,000 Thai characters,
  used to classify a PDF `clean` / `repairable` / `unusable` before ingestion
- **Prevalence** — share of a career's postings mentioning a skill; not a probability

## Environment

- Engine runs on **`linux-gpu-server`** — the project's own machine, department office,
  24/7. **Not CSML** (shared, contended GPU)
- Models served over an OpenAI-compatible endpoint; dev and production differ only by
  `MODEL_SERVER_URL`
- Model selection is **pending a VRAM check** — decide on measured linking quality, not
  model size. RAG makes adjudication a constrained selection task, which favours smaller
  models more than open generation does

## Open external dependencies

- Full KU มคอ.2 — the file on hand is an excerpt without the curriculum mapping table
- Demand corpus provenance (Thai or international, window, whether `N` is cumulative) —
  blocks the methods section
- Whether the ~100-skill cap is a display limit or a data limit
- A third TQF from a different PDF producer, to validate the glyph repair table

## Team focus

| Role | Focus |
|---|---|
| Researcher | Skill entity linking to controlled vocabularies; curriculum analytics; annotation protocol |
| Data Engineer | TQF ingestion, integrity gate, glyph repair, PageIndex navigation |
| AI Engineer | Retrieval, LLM adjudication, level inference, evaluation harness |
| Data Scientist | Alignment metrics on prevalence data; RCA weighting; growth adjustment |
| Full Stack Developer | FastAPI engine, Astro web, Cloudflare Tunnel and Access |
| UX/UI Designer | Skill-link review screen; heatmap; Thai typography |
| Test Engineer | Metric unit tests; reproducibility checks |
| Domain Expert | Annotation, level validation, curriculum-committee fit |

## Status (last updated 2026-08-28)

Phase 3 rewritten. National standard snapshot pinned
(`data/skillmapping/2026-08-27/` — 138 digital careers, 4,376 skills, 2,043 with full
level detail). Feasibility measured on real SWU and KU documents: both text layers are
damaged, the damage is characterised and repairable, and the SWU document carries the
curriculum mapping table that level inference depends on. Old implementation removed;
`engine/` and `web/` are created in Sprint 0.

**Design review 2026-08-28**, before Sprint 0. Caught that the primary metric as written
was uncomputable — the demand side carries no required level — and replaced it with a
prevalence-weighted coverage gap plus a seniority gradient derived from the standard's 13
paired careers. Also reconciled the Alternatives table with the vision-fallback decision,
corrected an overstated bilingual-channel claim, and specified the profile aggregation,
zero-link handling, and cost model that were missing.
