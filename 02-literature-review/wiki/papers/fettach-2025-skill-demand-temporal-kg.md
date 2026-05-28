---
type: paper
authors: Fettach Y., Bahaj A., Ghogho M.
year: 2025
title: "Skill Demand Forecasting Using Temporal Knowledge Graph Embeddings"
venue: arXiv preprint 2504.07233
doi:
relevance: medium
questions: [q-temporal-drift]
---

## Research Question
Can temporal knowledge graph (TKG) embeddings forecast future skill demand for IT occupations more effectively than static approaches?

## Limitations of Existing Methods
Static knowledge graphs represent skill-occupation relationships as they existed at creation time — they cannot reflect the continuous evolution of the labour market. Traditional time series forecasting treats skills independently without capturing inter-skill and skill-occupation relationships.

## Contribution
Formulates skill demand forecasting as temporal link prediction in a KG. Builds a temporal KG from job postings and compares five TKG embedding architectures (DE-TransE, DE-DistMult, TA-TransE, TA-DistMult, TeRo). Provides empirical demand evolution patterns for selected IT skills (Java, data analysis, teamwork).

## Proposed Method
- **Data**: 99,676 Moroccan IT job postings (November 2005 – September 2022); timestamps as discrete quarterly markers
- **Temporal KG structure**: Quadruples (occupation, REQUIRES_SKILL, skill, timestamp); timestamps represent when the fact first appeared
- **Models compared**: DE-TransE/DistMult (diachronic entity embeddings), TA-TransE/DistMult (LSTM-encoded timestamp sequences), TeRo (Hamiltonian complex space)
- **Evaluation**: Hit@1, Hit@3, Mean Reciprocal Rank (MRR) for link prediction

## Key Findings
- **Best model**: TA-DistMult — Hit@1: 61.77%, Hit@3: 84.53%, MRR: 74.20%
- TA models outperform DE models because TA models temporal *relation* changes (demand shifts) while DE models temporal *entity* changes (skill meaning evolution) — the former is more relevant for demand forecasting
- Observed skill trajectories: data analysis demand rising sharply 2021–2023 then declining in 2024; Java demand declining since 2022; teamwork consistently high and stable 2011–2024
- Soft skills (teamwork) exhibit temporal stability; technical skills exhibit higher volatility and phase shifts

## Limitations of This Paper
Moroccan IT market only — generalisability to other regional contexts untested. Closed-world assumption: cannot predict demand for skills or occupations not yet seen in training data (no handling of genuinely new skills). No comparison against time series baselines (LSTM, ARIMA). Computational constraints limited the range of architectures tested.

## Concepts
[[temporal-drift]] · [[skill-taxonomy]]

## Questions Addressed
[[q-temporal-drift]]

## Notes for Iris
**Confirms the soft vs. technical skill volatility pattern** from macedo-2022: soft skills are temporally stable; technical/emerging skills shift rapidly. For Iris, this means:
- Technical skill gaps should carry a temporal urgency annotation in reports
- Our convergence analysis in Phase 4 should stratify by skill type when assessing distribution stability over time
The closed-world assumption limitation is directly relevant to our emergent vocabulary design: a fixed taxonomy (like ESCO or a static Thai skill list) will miss newly emerging skill terms — another validation of our emergent vocabulary approach.
