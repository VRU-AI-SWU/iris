<p align="center">
  <img src="assets/iris.svg" alt="IRIS Logo" width="180" />
</p>

# Iris — Curriculum Skill Alignment

> **Domain:** Thai higher education · curriculum analytics
> **Aligned to:** [Thailand Skill Mapping](https://www.skillmapping.in.th/en) — the national skill standard published by สป.อว. (OPS MHESI), developed by KMITL
> **Status:** Phase 4 — Implementation, Sprint 0 *(redesigned 2026-08-27)*

---

## What it does

Thailand's Skill Mapping standard describes what skills each career demands, in a
controlled vocabulary of **4,376 skills** across **371 careers**. It defines its own
purpose as joining a *demand side* to a *supply side* — what the labour market wants,
and what curricula produce. Only the demand side is published.

**Iris builds the supply side.** It reads a Thai university's TQF (มคอ.2) document,
links every course to the national skill vocabulary **at a stated proficiency level**,
and compares the resulting programme profile against any career's published demand.

Output: a level-aware alignment report — *which demanded skills the curriculum does not
develop, and where it develops them too shallowly* — traceable to specific courses and
to specific pages of the source document.

**Research contribution:** level-aware skill entity linking from Thai TQF course
descriptions to a national controlled vocabulary, evaluated against expert annotation.

---

## Why it was redesigned

The original design built its own skill vocabulary by clustering terms extracted from
documents, and measured demand by scraping four Thai job boards. In July 2025 สป.อว.
published a national standard that supersedes both. The pivot removed the scrapers, the
clustering, the vector database, and the job queue — and added something the previous
design could not attempt: every skill in the standard carries **three proficiency levels
with explicit criteria**, and TQF documents declare their own depth signals under
regulation, so alignment can be measured by *level*, not merely by presence.

See [`03-solution-design/solution-proposal.md`](03-solution-design/solution-proposal.md).

---

## Research phases

| Phase | Description | Status |
|---|---|---|
| 1 | Brainstorm — problem scoping, hypotheses | ✅ Complete |
| 2 | Literature review — 23 papers across 13 questions | 🔄 Updating for the pivot |
| 3 | Solution design — architecture, product, data feasibility | ✅ Rewritten 2026-08-27 |
| 4 | Implementation — build and evaluate | 🔄 Sprint 0 |
| 5 | Reports — research paper and institutional report | ⬜ Planned |

---

## Repository

```
iris/
├── 01-brainstorm/                  problem scoping, decision log
├── 02-literature-review/           Obsidian wiki — papers, concepts, questions
├── 03-solution-design/
│   ├── solution-proposal.md        architecture, method, risks
│   ├── product-design.md           personas, surfaces, screens
│   └── data-feasibility.md         what the data actually supports  ◄ read this first
├── 04-implementation/
│   ├── engine/                     Python — ingestion, linking, alignment, API
│   └── web/                        Astro — public site + gated app
├── 05-reports/
└── data/skillmapping/              pinned snapshots of the national standard
```

---

## Architecture

Two deployables. The engine needs a GPU and tens of minutes per run; the public site
must stay up regardless.

```
Internet ──► Cloudflare · vru-ai.com/iris
              │
              ├─ public   Astro static · published results · no backend
              │
              └─ /app     Cloudflare Access (department faculty)
                            │ Cloudflare Tunnel (outbound only)
                            ▼
                          gpu-linux-server · department office · 24/7
                            FastAPI · PostgreSQL · local LLM
                            ingest → link → level → align → report → publish
```

The engine **publishes** versioned result documents; the web tier only reads them.
Nothing on the public site touches the GPU server at request time.

---

## Key decisions

| Decision | Choice | Rationale |
|---|---|---|
| Skill vocabulary | **National standard, pinned snapshot** | Reproducible, comparable, and the vocabulary the sector is adopting |
| Demand data | **Published state data** — no scraping | Anyone can reproduce the result; no ToS exposure |
| Linking method | RAG — retrieve candidates, LLM adjudicates | The standard's 4,376 definitions and 6,058 level criteria *are* the retrieval corpus |
| Proficiency level | Inferred from CLOs, curriculum map ● ○, and curriculum position | TQF declares its own depth signals; disagreement is reported, not hidden |
| Primary metric | Level-aware coverage gap, prevalence-weighted | Demand figures are prevalence, not a distribution — see below |
| Vector store | **None** — 13 MB in-memory matrix | A fixed 4,376-entry vocabulary needs exact search, not an index |
| Damaged Thai PDFs | Diagnostic gate + deterministic glyph repair | The damage is substitution, not deletion — repair is auditable where OCR is not |
| Engine language | Python | PDF parsing, Thai NLP, numerics, evaluation tooling |
| Web | Astro on Cloudflare Workers | Matches how `vru-ai-web` already deploys |

---

## Known limitations

Stated up front because they constrain what may be claimed:

- **The demand vector is truncated** at ~100 skills per career. A skill's absence means
  *below the cut-off*, never *not demanded*.
- **`percentage` is prevalence, not a distribution share** — percentages across a career
  sum to well over 100. Any distributional metric requires explicit renormalisation.
- **The demand corpus provenance is unconfirmed.** Posting counts range from 203 to 6.3 M
  per career, which is not plausible for Thailand alone. Being clarified with สป.อว./KMITL;
  until then Iris does not claim to measure the *Thai* labour market specifically.
- **The upstream API is beta** (`0.8.1-beta-public`). Analyses run against a pinned
  snapshot, never the live API.

---

## The snapshot

```bash
python3 data/skillmapping/fetch_snapshot.py                 # digital industry
python3 data/skillmapping/fetch_snapshot.py --industry all
```

Stdlib only. Writes a dated, self-describing snapshot with a manifest. The committed
snapshot is the reproducibility anchor — an analysis records which one it used.

---

*Iris — expressing a curriculum in the language the labour market is already described in.*
