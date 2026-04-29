<p align="center">
  <img src="assets/iris.svg" alt="IRIS Logo" width="180" />
</p>

# IRIS — Skill Gap Intelligence System

> **Codename:** IRIS
> **Domain:** Text Analytics · Agentic AI
> **Context:** Thai undergraduate academic programmes (TQF / มคอ.2)
> **Status:** Phase 1 — Brainstorm (in progress)

---

## Overview

IRIS is an agentic AI system that quantifies and explains the gap between the skills delivered by an academic programme and those demanded by the current job market. It compares two independent evidence sources — Thai university programme documents (TQF / มคอ.2) and real job postings from the Thai labour market — and produces actionable insights for curriculum designers, faculty, students, and institutional researchers.

IRIS addresses two analytical scenarios:

1. **Programme-to-Programme Gap** — Compare skill distributions from two academic programmes to surface differences and quantify the gap.
2. **Programme-to-Market Gap** — Compare a programme's skill distribution against the skill requirements for a target career path, derived from real job postings.

---

## Problem Statement

Academic programmes are updated on multi-year cycles, while the job market evolves continuously. Without a systematic, data-driven comparison, programme committees rely on anecdotal evidence or infrequent industry surveys to decide which competencies to add, remove, or strengthen. IRIS automates this comparison at scale and makes the evidence reproducible and peer-reviewable.

---

## Data Sources

### Source 1 — Academic Programme (TQF / มคอ.2)

| Item | Description |
|------|-------------|
| Input | Thai university programme specification documents in TQF (มคอ.2) format (PDF) |
| Primary extraction source | Course descriptions (คำอธิบายรายวิชา) |
| Course categories | Major-specific (หมวดวิชาเฉพาะ) · General Education (หมวดวิชาศึกษาทั่วไป) · Free Elective (หมวดวิชาเลือกเสรี) |
| Weighting | Major-specific courses weighted higher; free electives handled via scenario system |
| Output | Credit-weighted skill distribution per programme |

**Scenario system for free electives:**

| Scenario | Description |
|----------|-------------|
| Core | Required courses only (หมวดวิชาเฉพาะ บังคับ) — stable baseline |
| Core + Electives | Include user-specified free elective courses |
| Hypothetical | Proposed future curriculum — add or remove any courses for what-if analysis |

### Source 2 — Job Market Postings (Thailand)

| Item | Description |
|------|-------------|
| Primary sources | JobThai.com · JobsDB Thailand · Indeed Thailand |
| Secondary source | LinkedIn Thailand (anti-scraping constraints — supplementary only) |
| Schema | Unified job posting schema (title, description, requirements, company, date) with per-source adapters |
| Segmentation | CS career path × industry segment × time period |
| Output | Required skill distribution per segment |

**Industry segment enrichment — 3-tier pipeline:**

| Tier | Method | Applies when |
|------|--------|--------------|
| 1. Direct | Extract segment from posting (company name or stated industry) | Segment is explicit |
| 2. Search agent | Look up company profile via Thai registries (DBD, SET) or LinkedIn | Company name known but segment unknown |
| 3. LLM classifier | Infer segment from job description vocabulary | Agency postings that hide employer identity |

Initial segment taxonomy (~12 segments): Finance/Banking · Insurance · Manufacturing · Technology/Software · Healthcare · Retail/E-commerce · Government/Public Sector · Energy/Utilities · Telecommunications · Logistics/Supply Chain · Education · Professional Services.

---

## Core Capabilities

### 1. TQF Curriculum Parser
- Parses Thai TQF (มคอ.2) PDF documents
- Extracts course descriptions, programme learning outcomes, course categories, and credit hours
- Applies credit weighting (major-specific courses > general education)
- Supports scenario system for free elective toggling

### 2. Skill Extraction Agent
- Extracts skills from Thai and bilingual text using a local LLM (gemma-4-31b-it via LM Studio)
- Data-driven emergent vocabulary — no fixed taxonomy forced at extraction time
- Clusters semantically similar skills using text embeddings (text-embedding-embeddinggemma-300m)
- Decomposes into **common skills** (shared baseline) and **unique skills** (distinguishing each programme)
- Optional post-hoc mapping to reference taxonomy (O*NET, ESCO, SFIA) for cross-context comparability

### 3. Job Market Harvesting Agent
- Multi-source scraping with unified schema and per-source adapters
- LLM handles within-source format variation
- Industry segment enrichment via 3-tier pipeline (direct → search agent → LLM classifier)
- Aggregates demand distributions by career path, industry segment, and time period

### 4. Gap Analysis Engine
- **Set-based gap** — skills present in demand but absent from programme (and vice versa); most interpretable for non-technical stakeholders
- **Cosine distance** — overall similarity score between skill distribution vectors
- **KL divergence** — asymmetric gap measurement (programme supply vs market demand)
- Hybrid output: set-based gap for human-readable reports, cosine/KL for aggregate scoring

### 5. Reporting Agent
- Gap summary report with common/unique skill decomposition
- Per-skill traceback to source courses (for programme side) and job postings (for market side)
- Scenario comparison view — side-by-side skill distributions across scenarios
- Industry segment heatmap — programme fit score per industry segment
- Outputs: PDF/Markdown report · interactive web dashboard

---

## Skill Vocabulary Approach

IRIS uses a data-driven emergent vocabulary rather than a fixed taxonomy:

1. Extract raw skills from TQF course descriptions using LLM
2. Cluster semantically similar skills using embeddings (e.g., "machine learning" ≈ "predictive modelling")
3. Build a shared skill vocabulary from the union of all programmes being compared
4. Decompose into common skills and unique skills
5. Optionally map clusters to a reference taxonomy for cross-context comparability

This approach avoids the assumption that a gold-standard taxonomy exists for Thai academic programmes, and lets the data surface what skills are actually present.

---

## Key Metrics

| Metric | Description |
|--------|-------------|
| Supply–Demand Alignment Score | Overall goodness-of-fit between programme output and job market demand |
| Top-N Skill Gaps | Skills most demanded by the market but least covered by the curriculum |
| Top-N Surpluses | Skills well-covered by the curriculum but rarely demanded by the target market |
| Segment Fit Score | Programme alignment score per industry segment |
| Coverage Rate | Percentage of demanded competencies present in the curriculum |

---

## Target Users

| User | Key Need |
|------|----------|
| Academic administrator | Evidence of which skills are over/under-represented vs market demands |
| Curriculum designer | Specific, actionable skill gaps to address in course design |
| Student | Understand their programme's coverage relative to a target career path |
| Career advisor | Data-driven comparison tool for advising sessions |
| Accreditation body | Benchmark programmes against industry standards |
| Employer / HR | Transparency into what skill profile a programme produces |

---

## Constraints & Assumptions

- TQF documents are in Thai — skill extraction must handle Thai text; bilingual documents (Thai + English) are a bonus
- Course descriptions vary in richness — some are brief; extraction must be robust to sparse text
- Job posting data must be ethically sourced and legally usable
- Analysis must be explainable to non-technical academic stakeholders — black-box results will not be trusted or acted on
- Must produce outputs suitable for academic publication (rigorous and reproducible methodology)
- AI models run locally via LM Studio — no external cloud API; primary inference on gpu-linux-server (gemma-4-31b-it)
- v1 scope: Thai-language TQF documents; English-taught Thai programmes are an extension

---

## Out of Scope (v1)

- Real-time job posting scraping (start with a static snapshot dataset)
- Individual student skill assessment (programme-level analysis only)
- Soft skills and personality traits (focus on technical and domain skills)
- Automated curriculum redesign recommendations (gap identification only, not prescription)
- Overseas academic programmes (different regulatory frameworks)

---

## Research Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 1 | Brainstorm — problem scoping, hypothesis definition, data source design | 🔄 In Progress |
| Phase 2 | Literature Review — skill extraction NLP, gap methodologies, Thai ontologies, job posting sources | ⬜ Planned |
| Phase 3 | Solution Design — system architecture, product design | ⬜ Planned |
| Phase 4 | Implementation — build and evaluate the system | ⬜ Planned |
| Phase 5 | Reports — research paper and institutional report | ⬜ Planned |

---

## Repository Structure

```
iris/
├── readme.md                    # This file
├── CLAUDE.md                    # Project context for AI-assisted development
├── assets/                      # Project assets (logo, images)
├── 01-brainstorm/
│   └── brainstorm.md            # Problem scoping, hypotheses, initial ideas
├── 02-literature-review/        # Survey of methods and related work
├── 03-solution-design/          # System architecture and product design
├── 04-implementation/           # Source code
└── 05-reports/                  # Research papers and institutional reports
```

Data is stored separately (not committed to Git):

```
data/
├── tqf/                         # Raw TQF PDF documents
│   └── <university>/<programme>/
├── job-postings/                # Raw job posting datasets
│   └── thailand/
└── processed/                   # Generated outputs (never edit manually)
    ├── skill-distributions/     # Extracted skill vectors per programme
    └── job-skills/              # Extracted skill vectors per career path
```

---

*IRIS — Illuminating the gap between academic preparation and industry expectation.*
