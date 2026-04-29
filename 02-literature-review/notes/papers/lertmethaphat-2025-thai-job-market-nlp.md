---
type: paper
authors: Lertmethaphat N.N., Lekfuangfu W.N., Treeratpituk P.
year: 2025
title: "Exploring the Thai Job Market Through the Lens of Natural Language Processing and Machine Learning"
venue: PIER Discussion Paper 228, Puey Ungphakorn Institute for Economic Research (August 2024)
doi: https://www.pier.or.th/dp/228/
relevance: high
questions: [q-thai-nlp, q-job-posting-sources, q-sample-size]
---

## Research Question
How can NLP and ML automatically standardise high-frequency, bilingual Thai job posting data into ISCO-2008 occupational codes to enable construction of the Thai Beveridge curve and real-time labour market monitoring?

## Limitations of Existing Methods
No consistent Thai vacancy data exists (unlike US JOLTS or UK Vacancy Survey). Manual classification of Thai job titles to ISCO codes is prohibitively labour-intensive at the scale of online job portals. WangchanBERTa alone is insufficient — it cannot disambiguate closely related Thai job titles (e.g., Physician vs. Dentist scored 97.21% similarity).

## Contribution
First large-scale NLP pipeline for classifying bilingual (Thai+English) Thai job titles into 4-digit ISCO-2008 codes. Demonstrates USE + XGBoost achieves ~90% classification accuracy. Applied to 1.1 million job posts from two Thai platforms (Q4 2020 – Q3 2023), enabling the first approximation of Thailand's Beveridge curve from job posting data.

## Proposed Method
- **Training data**: Thailand Department of Employment (DOE) dataset — hundreds of thousands of manually annotated records from regional offices nationwide + ISCO codebooks (1988 + 2008)
- **Embedders compared**: WangchanBERTa (Thai BERT, AIRESEARCH) vs. Universal Sentence Encoder (USE)
- **Models evaluated**: Cosine Similarity Classifier, Hierarchical Cosine Similarity Classifier, Random Forest, XGBoost, Neural Networks, BERTopic
- **Data cleaning**: "Majority rule" (modal ISCO code per unique title) + "close-match" (USE cosine similarity above calibrated threshold)
- **Evaluation**: 5-fold cross-validation; accuracy at 1-digit through 4-digit ISCO level
- **Application dataset**: 1.1 million job posts from two Thai online job platforms, Q4 2020 – Q3 2023 (platforms unnamed in paper)

## Key Findings
- **Best model: USE + XGBoost — ~90% accuracy at 4-digit ISCO level** (most granular); outperforms all other configurations
- **WangchanBERTa limitation confirmed**: struggles to discriminate closely related Thai job titles — high similarity scores between semantically distinct roles (e.g., 97.21% between Physician and Dentist in Thai; 93.08% between Accountant and Bookkeeping Clerks)
- **USE outperforms WangchanBERTa** for this disambiguation task — better at distinguishing related occupational categories in both Thai and English text
- Bilingual (Thai+English) nature of postings confirmed: both embedders needed for full coverage
- Applied to 1.1M job posts: provides first high-frequency, real-time Thai labour market demand signal; enables Beveridge curve construction for Thailand

## Limitations of This Paper
Occupation-level classification (ISCO codes), not skill-level extraction — coarser granularity than what Iris requires. The two application platforms are unnamed — limits reproducibility and direct reuse by other researchers. Training data sourced from DOE (formal language) may underperform on informally written online postings. WangchanBERTa's weakness on related job titles is a significant finding for our skill extraction design.

## Concepts
[[thai-nlp]] · [[wangchanberta]] · [[job-posting-analysis]] · [[sentence-embedding]]

## Questions Addressed
[[q-thai-nlp]] · [[q-job-posting-sources]] · [[q-sample-size]]

## Notes for Iris
**Critical design implication: do NOT use WangchanBERTa alone for Thai job title or skill classification.** The paper directly demonstrates that WangchanBERTa fails to discriminate closely related Thai terms — a fatal flaw for fine-grained skill extraction. USE + XGBoost or a multilingual LLM approach (e.g., gemma-4-31b-it) is preferred. For Iris specifically: our pipeline should use USE or a multilingual embedding model for semantic matching, and rely on the LLM (gemma-4-31b-it) for the extraction step rather than WangchanBERTa. The 1.1M posts dataset covers Q4 2020–Q3 2023 — contact PIER (Pucktada Treeratpituk) to explore whether data can be accessed for research.
