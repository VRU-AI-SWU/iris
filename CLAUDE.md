# Project Iris — Skill Gap Analysis

## Overview

Iris is a skill gap analysis system that identifies and quantifies discrepancies between skill profiles. It serves two primary analytical functions:

1. **Programme-to-Programme Gap** — Compare skill distributions from two academic programmes to surface differences and summarise the gap.
2. **Programme-to-Market Gap** — Compare skill distributions from a given academic programme against required skills for a target career path, extracted from real job postings.

## Objectives

- Give academic institutions actionable insight into how their programmes align with each other and with labour market demands.
- Help students and career advisors understand skill gaps relative to target career paths.
- Produce outputs suitable for both academic research publication and practical institutional use.

## Domain

Higher education, curriculum design, labour market analysis, HR and talent acquisition.

**Domain Expert for this project:** Higher education / labour market specialist.

## Current Phase

Phase 4 — Implementation

## Key Concepts

- **Skill distribution** — A structured representation of the skills and their relative emphasis within a programme or job posting set.
- **Skill gap** — A quantified difference between two skill distributions; can be directional (programme A has more X than programme B) or deficit-based (programme lacks Y required by the market).
- **Job postings** — Source data for market skill requirements; must be scraped, cleaned, and skill-extracted.
- **Curriculum data** — Source data for programme skill profiles; may come from course syllabi, learning outcomes, or programme specifications.

## Team Focus for Iris

| Role | Focus |
|---|---|
| Researcher | Literature on skill gap methodologies, NLP for skill extraction, labour market studies |
| Data Engineer | Job posting ingestion pipeline, curriculum data parsing |
| Data Scientist | Skill distribution modelling, gap quantification methods |
| AI Engineer | NLP skill extraction model, embedding-based skill matching |
| Data Analyst | Gap visualisation, summary dashboards |
| Product Manager | Use case definition, stakeholder requirements |
| UX/UI Designer | Gap report UI, comparison visualisation |
| Full Stack Developer | Web application for analysis and reporting |
| Test Engineer | Data pipeline tests, model evaluation framework |
| Domain Expert | Curriculum and labour market validation |

## Key Questions to Answer

1. What is the best representation for a "skill distribution"? (taxonomy, embeddings, frequency vectors?)
2. How do we extract skills from free-text syllabi and job postings reliably?
3. What distance/similarity metric best captures a meaningful "skill gap"?
4. What output format is most useful to academic administrators and students?

## Status (last updated: 2026-04-29)

**Go decision made 2026-04-29. Phases 1 & 2 complete. Now in Phase 4 — Implementation.**

Phase 2 literature review produced 13+ paper notes across 9 question nodes in the Obsidian knowledge graph (`02-literature-review/notes/`). All literature-targeted open questions resolved; 3 questions deferred to Phase 4 empirical validation (credit weighting, segment inference reliability, Thai registry lookup). Key validated decisions: gemma-4-31b-it + USE extraction pipeline, KL divergence (market‖programme) as primary gap metric, RCA for skill weighting, 4 confirmed Thai job platforms, 12-month data window, chaiaroon-2025 20-role taxonomy, heatmap + multi-level output. See `01-brainstorm/brainstorm.md` for the full decision log and final idea summary.

## Tech Stack

- **Backend API** — Rust / Axum
- **Worker** — Apalis (Rust-based job queue)
- **Clustering Sidecar** — Python / HDBSCAN
- **Frontend** — (see `04-implementation/frontend/`)

## Related Files

- `01-brainstorm/` — Problem scoping and hypothesis definition
- `02-literature-review/` — Survey of skill gap methodologies and NLP skill extraction
- `03-solution-design/` — System architecture and product design
- `04-implementation/` — Source code
- `05-reports/` — Research papers and institutional reports
