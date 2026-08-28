# Iris — Technology Stack

> Rewritten 2026-08-27 for the national-standard pivot. The previous stack
> (Rust/Axum + Apalis + HDBSCAN sidecar, or before that FastAPI + Celery + JSON files)
> was built around scraping job boards and clustering an emergent skill vocabulary.
> Neither exists any more. See [`solution-proposal.md`](03-solution-design/solution-proposal.md).

---

## Shape of the system

Two deployables with one contract between them.

| | Engine | Web |
|---|---|---|
| **Runs on** | `linux-gpu-server` — department office, 24/7 | Cloudflare Workers |
| **Language** | Python 3.12 | TypeScript |
| **Why there** | Needs a GPU, native libraries, and tens of minutes per run | Must stay up regardless of the engine |
| **Reached by** | Cloudflare Tunnel, behind Cloudflare Access | `vru-ai.com/iris` |

The engine **publishes** versioned result documents. The web tier only reads published
results. Nothing on the public site touches the GPU server at request time.

---

## Engine — Python

| Concern | Choice | Note |
|---|---|---|
| Language | Python 3.12 | The whole task — PDF parsing, Thai NLP, numerics, evaluation tooling — is Python-native |
| API | FastAPI | Upload, job status, results, publish |
| Job execution | DB-backed job table + a worker process | Runs are minutes-long and few; Celery/Redis would be machinery without a purpose |
| Database | PostgreSQL 16 | Source of truth. **No `pgvector`** — see below |
| Migrations | Alembic | |
| PDF text | PyMuPDF | Verified against poppler on both test documents — identical output, so either works; PyMuPDF for the richer API |
| Document index | [PageIndex](https://github.com/VectifyAI/PageIndex) | Locates มคอ.2 sections across universities; nodes carry page ranges, giving provenance |
| Thai NLP | PyThaiNLP | Tokenisation, and lexicon-based restoration of collapsed `ำ` |
| Vision fallback | Typhoon OCR (3B) | For text layers that are lossy rather than merely substituted. Thai government forms at Levenshtein 0.04, self-hosted; output flagged as vision-derived |
| Numerics | NumPy, SciPy | Retrieval matrix, alignment metrics |
| Report | Jinja2 + WeasyPrint | HTML report, PDF export |
| Structured LLM output | Pydantic v2 | Linking output constrained to valid skill IDs |
| Tests | pytest | Metric functions have known-input/known-output tests |
| Lint / format | ruff | |

### Why not a vector database

The skill vocabulary is **fixed national reference data**: 4,376 entries. At 768
dimensions that is a 13 MB `float32` matrix. Exact cosine similarity over it is a
single `numpy` matrix multiply — microseconds, no index to build, no extra service to
run, no approximation to tune.

`pgvector` was in the previous design to hold an *emergent* vocabulary that grew as new
programmes were clustered in. The pivot deleted that vocabulary. The scaling problem a
vector database solves does not exist here.

Retrieval combines that dense matrix with lexical matching — necessary because tool
names (`Docker`, `.NET Core`, `Apache Spark`) match far better lexically than
semantically.

### Models

Served over an OpenAI-compatible endpoint so dev and production differ only by
`MODEL_SERVER_URL`.

| Role | Requirement |
|---|---|
| Adjudication | Follows a constrained multiple-choice instruction and returns valid JSON. RAG reduces this from open generation to selection among ~30 candidates, so a model sized to the available VRAM is viable — to be confirmed at the evaluation gate, not assumed |
| Embedding | Multilingual, handles Thai and English skill terms |
| Serving | LM Studio (dev) / Ollama (production), both on `linux-gpu-server` |

> ⚠️ Model choice is **pending a VRAM check** on `linux-gpu-server`. A previous commit
> recorded dropping from `gemma-4-31b-it` to `gemma-4-e4b` to fit 19 GB. Decide against
> measured linking quality, not model size.

---

## Web — Astro on Cloudflare

| Concern | Choice | Note |
|---|---|---|
| Framework | Astro | Static-first with islands for the interactive views; matches how `vru-ai-web` already deploys |
| Hosting | Cloudflare Workers (static assets) | Same pattern as the lab site |
| Route | `vru-ai.com/iris` | Listed among lab projects |
| Auth | Cloudflare Access | Department faculty allowlist. No login code in the application |
| Engine access | Cloudflare Tunnel | Outbound-only from the office server — no port forwarding, no public IP, no university firewall changes |
| Charts | Client-side island | Heatmap (courses × skills), ranked gap tables |
| Published results | **Build-time JSON** | Not D1/R2 in v1 — a handful of programmes, versioned in git, reproducible. Move to D1/R2 when the result set outgrows a build artefact |

### Public and gated surfaces

```
vru-ai.com/iris          public  · Astro static · published results · no backend
vru-ai.com/iris/app      gated   · Cloudflare Access → Tunnel → FastAPI
```

The public surface has no runtime dependency on the engine, so it is unaffected when
the engine is busy, restarting, or offline.

---

## Data storage

| What | Where | Committed? |
|---|---|---|
| National standard snapshot | `data/skillmapping/<YYYY-MM-DD>/` | **Yes** — the reproducibility anchor |
| Source TQF PDFs | `data/programmes/` | No — institutional documents |
| Engine working data | PostgreSQL | No |
| Published results | Versioned JSON, built into the web tier | **Yes** |
| Generated PDF reports | Engine filesystem; R2 if they outgrow it | No |

The snapshot is pinned deliberately: the upstream API is beta (`0.8.1-beta-public`) and
its data will change. **The engine never calls the live API during an analysis** — it
reads the pinned snapshot, so a result can be reproduced years later.

---

## Repository layout

```
iris/
├── 01-brainstorm/
├── 02-literature-review/
├── 03-solution-design/
│   ├── solution-proposal.md
│   ├── product-design.md
│   └── data-feasibility.md
├── 04-implementation/
│   ├── engine/                 Python — ingestion, linking, analysis, API
│   └── web/                    Astro — public site + gated app
├── 05-reports/
└── data/skillmapping/          pinned national standard snapshots
```

---

## Environment

```
# Model server
MODEL_SERVER_URL=http://localhost:1234/v1     # LM Studio (dev)
# MODEL_SERVER_URL=http://ollama:11434/v1     # Ollama (production)
EXTRACTION_MODEL=<pending VRAM check>
EMBEDDING_MODEL=<pending VRAM check>

# Database
DATABASE_URL=postgresql://iris:...@localhost:5432/iris

# Standard snapshot
SKILLMAP_SNAPSHOT=data/skillmapping/2026-08-27

# PageIndex
PAGEINDEX_MODE=local
```

---

## Decision log

| Decision | Rationale |
|---|---|
| Python everywhere in the engine | PDF parsing, Thai NLP, numerics, and evaluation tooling are all Python. Rust's advantage was scraping concurrency, which the pivot removed; a Rust core would have needed a Python sidecar regardless |
| No vector database | Fixed 4,376-entry vocabulary fits in RAM; exact search beats approximate search at this size |
| No Celery/Redis | Few, long, low-concurrency jobs. A job table and a worker process are less to operate and easier to reproduce |
| PageIndex for document navigation | มคอ.2 structure is regulated but formatting is not; page-range provenance is a research requirement |
| Deterministic glyph repair **first**, vision fallback second | Where damage is substitution, repair is exact, auditable and free. Where the text layer has genuinely lost information (KU's `ำ` collapse), no table can recover it — a self-hostable Thai-tuned 3B VLM is the fallback, with provenance flagged |
| Two deployables | The public site must not depend on a GPU server's availability |
| Own `linux-gpu-server`, not CSML | CSML's GPU is contended across the department; this machine is dedicated and always on |
| Cloudflare Tunnel + Access | Reaches a machine behind university NAT with no inbound exposure, and provides auth without application code |
| Astro, not Next.js | Data-display workload; matches the lab site's existing deployment; better static/SEO fit for a project page |
| Build-time JSON, not D1/R2, in v1 | Small result set, versioned in git, one fewer moving part |
| Snapshot pinned and committed | Upstream is beta and will change; reproducibility is a publication requirement |
