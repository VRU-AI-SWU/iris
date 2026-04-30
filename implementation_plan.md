# Iris — Phase 4 Implementation Plan

> Supersedes earlier draft. Aligned with Phase 3 solution-proposal.md (2026-04-30).

---

## Principles

- Build pipeline-first: validate skill extraction on real TQF documents before building the web layer
- Each sprint produces a testable, runnable artefact — no dead stubs
- Dev runs on gpu-linux-server (LM Studio, port 1234); production runs on CSML (Ollama container)
- The same OpenAI-compatible API is used in both environments — only the `MODEL_SERVER_URL` env var changes
- PostgreSQL is the single source of truth; pipeline outputs are always persisted before being served

---

## Sprint Map

### Sprint 0 — Scaffold & Infrastructure
**Goal:** Full docker-compose stack starts cleanly; database schema migrated; LM Studio connection verified.

- [x] `04-implementation/` directory structure created
- [ ] `docker-compose.yml` (production — CSML/Ollama)
- [ ] `docker-compose.dev.yml` (dev override — LM Studio)
- [ ] `.env.example` with all required variables
- [ ] `nginx/nginx.conf`
- [ ] Backend `Dockerfile` + `requirements.txt`
- [ ] Worker `Dockerfile` + `requirements.txt`
- [ ] `backend/app/main.py` — FastAPI app, health check route
- [ ] `backend/app/config.py` — settings from env
- [ ] `backend/app/database.py` — SQLAlchemy + Alembic setup
- [ ] `backend/app/models/` — ORM models (Programme, Course, Skill, JobPosting, SkillVocab, GapResult)
- [ ] Alembic initial migration
- [ ] `worker/celery_app.py` — Celery + Redis config
- [ ] Verify: `docker compose -f docker-compose.dev.yml up` starts all services

**Deliverable:** All services start; `GET /health` returns 200; DB schema created.

---

### Sprint 1 — TQF Ingestion Pipeline
**Goal:** Upload a TQF PDF → parsed courses → extracted skills → stored in DB.

- [ ] `worker/pipeline/tqf_parser.py` — PDF text extraction (pdftotext/pdfplumber); TQF section detection; course description extraction; credit-hour and category (major/general/elective) parsing
- [ ] `worker/pipeline/thai_preprocessor.py` — PyThaiNLP tokenisation, stop word removal
- [ ] `worker/pipeline/skill_extractor.py` — LLM zero-shot extraction; JSON output; retry logic
- [ ] `worker/tasks/tqf_tasks.py` — Celery task wrapping the pipeline
- [ ] `backend/app/api/routes_programmes.py` — `POST /api/programmes/upload`, `GET /api/programmes`, `GET /api/programmes/{id}`
- [ ] Manual evaluation: run on SWU and KU TQF PDFs; check extracted skills quality

**Deliverable:** Upload TQF PDF via API → skills stored in DB and retrievable.

---

### Sprint 2 — Skill Vocabulary Builder
**Goal:** Cluster extracted skills into canonical vocabulary; store in DB.

- [ ] `worker/pipeline/skill_embedder.py` — batch embedding via LM Studio/Ollama `/v1/embeddings`
- [ ] `worker/pipeline/vocab_builder.py` — HDBSCAN clustering of skill embeddings; canonical label per cluster; cluster membership mapping
- [ ] `worker/tasks/vocab_tasks.py` — Celery task; rebuild vocabulary when new programmes added
- [ ] `backend/app/api/routes_vocab.py` — `GET /api/vocab`, `POST /api/vocab/rebuild`
- [ ] Skill distribution construction: credit-weighted frequency vector per programme over canonical vocab

**Deliverable:** Skill vocabulary built from uploaded programmes; distribution vectors computed and stored.

---

### Sprint 3 — Job Posting Pipeline
**Goal:** Scrape and extract skills from Thai job postings for at least one career path.

- [ ] `worker/pipeline/scraper/base.py` — abstract scraper; unified job posting schema; rate limiting; robots.txt respect
- [ ] `worker/pipeline/scraper/jobthai.py` — Jobthai.com scraper (Scrapy spider)
- [ ] `worker/pipeline/scraper/jobsdb.py` — JobsDB Thailand scraper
- [ ] `worker/pipeline/scraper/jobbkk.py` — JOBBKK.com scraper
- [ ] `worker/pipeline/scraper/jobtopgun.py` — JOBTOPGUN.com scraper
- [ ] Job skill extraction using same `skill_extractor.py` pipeline
- [ ] `worker/tasks/job_tasks.py` — Celery scraping + extraction task
- [ ] `backend/app/api/routes_jobs.py` — `POST /api/jobs/scrape`, `GET /api/jobs`, `GET /api/jobs/distributions`
- [ ] Market demand distribution: frequency vector per career path over canonical vocab (12-month window)

**Deliverable:** Job postings scraped and skills extracted for ≥1 career path; market distribution stored.

---

### Sprint 4 — Gap Analysis Engine
**Goal:** Compute KL divergence and RCA-ranked gap between a programme and a career path.

- [ ] `worker/pipeline/gap_engine.py`:
  - Distribution alignment (zero-fill missing skills)
  - KL divergence D_KL(market ‖ programme)
  - RCA computation per skill
  - Set decomposition (common / programme-unique / market-unique)
  - Cosine similarity (aggregate score)
- [ ] `worker/tasks/analysis_tasks.py` — Celery gap analysis task
- [ ] `backend/app/api/routes_analysis.py` — `POST /api/analysis/run`, `GET /api/analysis/{id}`
- [ ] Programme-to-programme comparison mode (set decomposition only)

**Deliverable:** `POST /api/analysis/run` returns ranked gap table, KL score, and skill decomposition.

---

### Sprint 5 — Report Generator
**Goal:** Produce heatmap and narrative summary from gap analysis results.

- [ ] `worker/pipeline/report_generator.py`:
  - Heatmap data structure (courses × skills matrix)
  - Narrative summary via LLM (structured prompt → plain-language paragraph)
  - PDF export (WeasyPrint or reportlab)
- [ ] `worker/tasks/report_tasks.py` — Celery report generation task
- [ ] `backend/app/api/routes_reports.py` — `POST /api/reports/generate/{analysis_id}`, `GET /api/reports/{id}`, `GET /api/reports/{id}/pdf`

**Deliverable:** Gap analysis result → downloadable PDF report with heatmap and narrative.

---

### Sprint 6 — Web Frontend
**Goal:** Non-technical user can upload TQF, run analysis, view report, export PDF — all via UI.

- [ ] Next.js 14 app scaffold (App Router, TypeScript, Tailwind, shadcn/ui)
- [ ] Programme Library screen
- [ ] TQF upload + skill review screen
- [ ] Career path selector (20-role taxonomy)
- [ ] Gap Report screen (heatmap, ranked gap table, narrative summary)
- [ ] Programme-to-programme comparison screen
- [ ] Scenario Builder screen
- [ ] PDF export button
- [ ] API client (auto-generated from FastAPI OpenAPI spec)

**Deliverable:** Full end-to-end flow works via browser.

---

### Sprint 7 — Evaluation & Hardening
**Goal:** Validate extraction quality; harden pipeline; prepare for academic publication.

- [ ] Manual evaluation: 50-course sample — precision/recall of skill extraction
- [ ] Prompt tuning based on evaluation results
- [ ] Load test: full TQF document (120+ courses) — measure end-to-end pipeline time
- [ ] Error handling: LLM unavailable, malformed PDF, empty course description
- [ ] Data ethics audit: confirm no PII in stored job postings
- [ ] Document collection date, platform, and methodology for paper methods section
- [ ] Write unit tests for gap_engine.py (known distributions → expected scores)
- [ ] Write integration tests for TQF upload → analysis pipeline

---

## Development Conventions

- All LLM calls go through `worker/pipeline/llm_client.py` — single point for model server URL, retry logic, and prompt logging
- Pydantic v2 schemas in `backend/app/schemas/` are shared between API layer and worker (import directly)
- Celery tasks are thin wrappers — all logic lives in `worker/pipeline/` modules so it can be unit-tested without Celery
- Never store raw model weights in the repo; models live on the host filesystem and are volume-mounted
- Thai text: always preprocess with PyThaiNLP before passing to LLM; log the preprocessed text for debugging

---

## Environment Variables (.env.example)

```
# Model server
MODEL_SERVER_URL=http://host.docker.internal:1234/v1   # dev (LM Studio)
# MODEL_SERVER_URL=http://ollama:11434/v1              # prod (Ollama container)
EXTRACTION_MODEL=gemma-4-31b-it
EMBEDDING_MODEL=text-embedding-embeddinggemma-300m

# Database
DATABASE_URL=postgresql://iris:iris@postgres:5432/iris

# Celery / Redis
REDIS_URL=redis://redis:6379/0

# App
SECRET_KEY=change-me-in-production
DEBUG=true
```
