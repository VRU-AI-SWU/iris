---
type: paper
authors: Tipsena R., Chansanam W., Tuamsuk K., Manorom P.
year: 2025
title: "Predicting Workforce Needs in Thailand's Digital Industry: A Machine Learning Approach (2023-2024)"
venue: Journal of Information Science Theory and Practice (JISTaP) 13(3):1-16, 2025
doi: 10.1633/JISTaP.2025.13.3.1
relevance: high
questions: [q-job-posting-sources, q-sample-size, q-segment-taxonomy]
---

## Research Question
Can machine learning models predict future workforce requirements across five segments of Thailand's digital industry using web-scraped job posting data from 2023–2024?

## Limitations of Existing Methods
Prior Thai workforce studies relied on government statistics (headcount data, not skill-level), small expert surveys, or single-platform scraping. No study had collected job postings at scale across multiple Thai platforms and multiple digital industry segments simultaneously for predictive modelling.

## Contribution
Largest recent Thai digital industry job posting dataset: **24,494 job positions** from **10 Thai job advertisement websites** (2023–2024). Predictive ML classification model for workforce segment forecasting. Five-segment digital industry taxonomy validated for Thai labour market.

## Proposed Method
- **Data collection**: Web scraping from 10 Thai job advertisement websites (2023–2024); 24,494 positions collected
- **Five digital segments**: (1) hardware & smart devices, (2) software & software services, (3) digital services, (4) digital content, (5) telecommunications
- **Preprocessing**: Text cleaning, punctuation removal, tokenisation, stop word removal, TF-IDF feature extraction
- **Models**: Logistic regression, Decision tree, K-Nearest Neighbors (KNN), Naïve Bayes
- **Evaluation**: Accuracy, precision, recall, F1-score, ROC-AUC
- **Best model**: KNN — accuracy/AUC 0.792, precision 0.793, recall 0.731, F1 0.751

## Key Findings
- KNN outperforms logistic regression, decision tree, and Naïve Bayes for segment classification
- All models achieve AUC > 0.5 — above random; KNN achieves 0.792
- **Digital services** segment shows the strongest upward trend in job demand (2023–2024 data)
- 10 Thai job advertising websites used — confirms that multiple Thai platforms beyond JobThai/JobsDB exist and can be scraped
- TF-IDF features from job descriptions are sufficient to predict which digital industry segment a posting belongs to
- Thai digital industry is growing but faces skill mismatch (companies cannot find workers with required digital competencies)

## Limitations of This Paper
Focus is on segment classification prediction, not skill-level extraction or gap quantification. TF-IDF representation does not capture semantic relationships between skills. No breakdown of which 10 websites were used (names not disclosed). Prediction is segment-level, not career-path-level. Study period is 2023–2024 only — no longitudinal trend beyond this window.

## Concepts
[[thai-nlp]] · [[job-posting-analysis]] · [[skill-gap-quantification]]

## Questions Addressed
[[q-job-posting-sources]] · [[q-sample-size]] · [[q-segment-taxonomy]]

## Notes for Iris
**Three key implications for Iris:**
1. **Sample size benchmark**: 24,494 positions across 10 websites and 5 segments — this is the most recent large-scale Thai digital job posting dataset. If we divide by 5 segments, that's ~4,900 per segment on average. This gives us a realistic target: our v1 data collection should aim for at least 1,000–2,000 postings per career path to be in a credible range.
2. **Five-segment taxonomy**: The hardware/software/digital-services/digital-content/telecom segmentation aligns well with our planned career path scope and confirms a widely used framing for Thai digital workforce analysis. Consider adopting or adapting this taxonomy for our segment classification.
3. **10 Thai platforms**: Confirms that viable Thai job posting sources extend well beyond JobThai and JobsDB. Our Data Engineer should investigate which 10 platforms were used — contacting the authors (Khon Kaen University, Wirapong Chansanam wirach@kku.ac.th) may yield the platform list.
