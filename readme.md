<p align="center">
  <img src="assets/iris.svg" alt="IRIS Logo" width="180" />
</p>

# Iris — Skill Gap Analysis System

> **Domain:** Thai Higher Education · Labour Market Analytics
> **Data source:** TQF (มคอ.2) academic programme documents · Thai job postings
> **Status:** Phase 4 — Implementation

---

## What It Does

Iris quantifies the gap between the skill profile of a Thai academic programme (extracted from TQF มคอ.2 documents) and the skills demanded by the current job market for a target career path. It also supports head-to-head comparison between two programmes.

**Two analytical modes:**
1. **Programme-to-Market** — compare a programme's skill distribution against aggregated job posting demand for a career path (e.g., Data Engineer, DevOps)
2. **Programme-to-Programme** — compare skill profiles of two programmes to surface common and unique skills

**Outputs:** Multi-level curriculum analytics report — heatmap (courses × skills) with narrative summary for administrators; course-level drill-down for curriculum designers; PDF export.

---

## Research Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 | Brainstorm — problem scoping, hypotheses, data source design | ✅ Complete |
| 2 | Literature Review — NLP, gap methodologies, Thai ontologies, job sources | ✅ Complete (go decision 2026-04-29) |
| 3 | Solution Design — system architecture, product design | ✅ Complete |
| 4 | Implementation — build and evaluate | 🔄 In Progress |
| 5 | Reports — research paper and institutional report | ⬜ Planned |

---

## Repository Structure

```
iris/
├── 01-brainstorm/
│   └── brainstorm.md            # Problem scoping, go decision, final idea summary
├── 02-literature-review/        # Obsidian knowledge graph (paper + question + concept nodes)
│   └── notes/
├── 03-solution-design/
│   ├── solution-proposal.md     # System architecture, components, risks
│   └── product-design.md        # Personas, use cases, screen inventory, IA
├── 04-implementation/           # Source code (see below)
└── 05-reports/                  # Research papers and institutional reports
```

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Web App (Next.js)  ←→  REST API (FastAPI)                  │
└──────────────────────────┬──────────────────────────────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
    Gap Analysis      Report Gen       Scenario Engine
    (KL div + RCA)    (heatmap + PDF)
          │
    Skill Vocab Builder (embedding clusters)
          │
    ┌─────┴──────┐
    │            │
TQF Pipeline  Job Posting Pipeline
(PDF→skills)  (scrape 4 Thai platforms→skills)
    │            │
    └─────┬──────┘
          │
   Model Server (Ollama / LM Studio)
   gemma-4-31b-it · text-embedding-embeddinggemma-300m
          │
   PostgreSQL
```

---

## Key Technical Decisions

| Decision | Choice | Rationale |
|---|---|---|
| Skill extraction model | gemma-4-31b-it (zero-shot) | Multilingual; handles Thai natively; no fixed taxonomy imposed |
| Embedding model | text-embedding-embeddinggemma-300m | Local; same provider as extraction model |
| Skill vocabulary | Data-driven emergent (bottom-up clustering) | No Thai skill ontology exists; emergent vocabulary is more honest |
| Gap metric | KL divergence, market‖programme direction | Validated in literature (sabet-2024); penalises what graduates lack |
| Skill ranking | RCA (Revealed Comparative Advantage) | Rewards career-discriminating skills over generic common ones |
| Career path taxonomy | chaiaroon-2025 20-role Thai digital taxonomy | Empirically validated on 11,365 Thai job postings |
| Job platforms | Jobthai, Jobsdb, JOBBKK, JOBTOPGUN | Confirmed in Thai academic research; LinkedIn excluded (ToS) |
| Data window | 12-month static snapshot | Credible signal horizon ≈ 12 months (macedo-2022) |
| Model server (dev) | LM Studio on gpu-linux-server host, port 1234 | Already running; OpenAI-compatible API |
| Model server (prod) | Ollama container on CSML, models volume-mounted | Docker-native; same OpenAI-compatible API |
| Primary visualisation | Heatmap (courses × skills) | Validated for academic administrators (ahadi-2022, hilliger-2022) |

---

## Running Locally (Development)

**Prerequisites:** gpu-linux-server with LM Studio running (`gemma-4-31b-it` and `text-embedding-embeddinggemma-300m` loaded), Docker, Docker Compose.

```bash
cd 04-implementation
cp .env.example .env          # edit MODEL_SERVER_URL to point to LM Studio
docker compose -f docker-compose.dev.yml up
```

App available at `http://localhost:80`.

## Running in Production (CSML)

```bash
# On CSML — first time only
sudo nvidia-smi --mig 0       # disable MIG for full GPU allocation
cd 04-implementation
docker compose up -d
```

---

*Iris — Illuminating the gap between academic preparation and industry expectation.*
