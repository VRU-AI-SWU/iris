---
type: paper
authors: Garcia de Macedo M.M., Clarke W., Lucherini E., Baldwin T., Queiroz Neto D., de Paula R., Das S.
year: 2022
title: "Practical Skills Demand Forecasting via Representation Learning of Temporal Dynamics"
venue: arXiv preprint 2205.09508
doi:
relevance: high
questions: [q-temporal-drift]
---

## Research Question
How effectively can past skill demand patterns from online job advertisements predict future demand, and what temporal modelling approach produces the most reliable forecasts?

## Limitations of Existing Methods
No systematic temporal forecasting pipeline existed for skill demand from job postings. Point-in-time (snapshot) analyses are standard in the literature but cannot anticipate which skills will grow or decline. BLS surveys provide ground truth but with 1–2 year lag; job postings provide near-real-time signal but are noisy.

## Contribution
End-to-end pipeline for multi-step skill demand forecasting from monthly job posting aggregations. Comparison of LSTM, CNN+LSTM, and GRU architectures. Key empirical finding on the credible forecasting horizon for skill demand.

## Proposed Method
- **Data**: 120 monthly observations (2010–2019); computer and mathematical occupations; US labour market
- **Preprocessing**: 3-month moving average smoothing → first-differencing → z-score normalisation; training on 2010–2018, testing 2019
- **Models**: LSTM, CNN+LSTM, GRU; variable lag windows tested (12, 24, 36 months)
- **Forecast horizons**: 6, 12, 24, 36 months ahead (one-shot multi-step)
- **Evaluation**: NRMSE (normalised root mean squared error); multivariate vs. univariate comparison

## Key Findings
- **Credible forecast horizon ≈ 12 months**: Error increases substantially beyond 12-month predictions; 6-month forecasts are most reliable. Critical quote: *"the horizon over which we can make credible forecasts (about a year) is much shorter than people's learning and working lives."*
- Skill demand volatility varies by skill type: business management skills are stable (NRMSE 0.08); cloud computing is volatile (NRMSE 0.42)
- Monthly aggregation with 3-month smoothing is the right temporal granularity — weekly is too noisy, quarterly loses responsiveness
- Multivariate models (capturing inter-skill correlations) outperform univariate — skills are interdependent in demand
- Excluded 2020 data due to COVID disruption — external shocks require special handling

## Limitations of This Paper
US-only; computer and mathematical occupations only — generalisability untested. 120 observations insufficient for deep architectures (adding layers did not improve performance). Implicit skill bias: skills not mentioned in postings but practised on the job are invisible. External shock blindness: model cannot predict demand shifts caused by non-market events until reflected in posting behaviour.

## Concepts
[[temporal-drift]] · [[job-posting-analysis]] · [[skill-gap-quantification]]

## Questions Addressed
[[q-temporal-drift]]

## Notes for Iris
**Critical design implication for data collection strategy:** The 12-month credible forecast horizon means job posting data older than approximately 12–18 months should be treated as potentially stale for market signal purposes. For Iris v1 using a static snapshot dataset, we should:
1. Collect postings from a clearly defined recent time window (ideally the most recent 12 months)
2. Document the collection date prominently — our gap scores are valid as of that snapshot
3. Flag temporal limitation explicitly in the methods: Iris v1 produces a static gap score, not a live signal
The volatility finding (technical/emerging skills change faster than soft skills) is also relevant: in our gap report, technical skill gaps deserve higher urgency flags than soft skill gaps since they are more likely to be current.
