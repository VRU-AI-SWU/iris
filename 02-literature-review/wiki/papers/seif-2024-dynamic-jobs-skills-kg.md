---
type: paper
authors: Seif A., Toh S., Lee H.K.
year: 2024
title: "A Dynamic Jobs-Skills Knowledge Graph"
venue: RecSys in HR 2024 (4th Workshop on Recommender Systems for Human Resources, ACM RecSys 2024), CEUR Vol-3788
doi:
relevance: high
questions: [q-temporal-drift, q-skill-taxonomy]
---

## Research Question
How can a jobs-skills knowledge graph be kept dynamically current over time, combining expert knowledge from a national skills framework with continuous signals from labour market data?

## Limitations of Existing Methods
Static knowledge graphs (including published skills frameworks like ESCO, O*NET, SSG Skills Framework) represent a snapshot in time; they become stale as labour market demands evolve. NLP-extracted skill lists from job postings are noisy and lack expert validation. Neither approach alone is sufficient.

## Contribution
Architecture for a **dynamic, self-updating Jobs-Skills Knowledge Graph (JSKG)** that combines: (1) expert-curated national skills framework as a foundation, (2) NLP-extracted job posting signals, (3) sliding window weighted averages for temporal smoothing. Deployed in production for Singapore's SkillsFuture programme.

## Proposed Method
- **Foundation**: Singapore SSG Skills Framework (national expert-curated occupations + skills taxonomy) as the seed knowledge base
- **Data integration**: ML classifiers map job posting entities (job titles, skill mentions) onto JSKG nodes; new entities added when evidence threshold is met
- **Temporal update mechanism**: **Sliding window weighted averages** — skills' association strengths are updated using a moving window over recent postings; older signals are downweighted
- **Graph structure**: Property graph (Neo4j-style); nodes = occupations, skills, courses; edges = REQUIRES\_SKILL, DEVELOPS\_SKILL, with strength and recency properties
- **Context**: Singapore labour market; linked to SkillsFuture course listings as well as job postings

## Key Findings
- Hybrid approach (expert seed + job posting signals) is more robust than either alone: expert knowledge provides stability, job postings provide recency
- Sliding window weighted averages prevent rapid oscillation while still responding to genuine demand shifts — practically, a 6-12 month window is recommended
- Knowledge graph structure allows natural traversal queries: "what skills does occupation X require that course Y does not teach?"
- Singapore context (small, developed, government-driven digital economy) provides a meaningful comparator for Thailand; SkillsFuture ≈ TPQI in role

## Limitations of This Paper
Singapore-specific; national skills framework as seed is not available for all markets (Thailand's TPQI is much less granular). No quantitative evaluation of gap analysis accuracy. Workshop paper — shorter scope, implementation details summarised. Requires sustained data pipeline infrastructure to maintain dynamism.

## Concepts
[[temporal-drift]] · [[skill-taxonomy]] · [[curriculum-analytics]]

## Questions Addressed
[[q-temporal-drift]] · [[q-skill-taxonomy]]

## Notes for Iris
**Two direct implications:**
1. **Sliding window for temporal handling**: The recommendation of a 6–12 month sliding window for smoothing skill demand signals aligns with the macedo-2022 finding that 12 months is the credible forecast horizon. For Iris v1 (static snapshot), we should scope our dataset to the most recent 12 months and note this explicitly. For a future live Iris system, the JSKG sliding window architecture is the right evolution path.
2. **Expert seed + data signal hybrid**: The SSG/JSKG approach validates our planned workflow: start with expert-validated Thai skill vocabulary (from TQF analysis + TPQI reference) as seed, then enrich with extracted job posting signals. This is more robust than purely emergent or purely expert-curated approaches.
The Singapore context is the closest available published analogue to Thailand's situation (small Asian economy, government skills framework, growing digital sector) — cite seif-2024 when discussing our design choices for vocabulary seeding and temporal handling.
