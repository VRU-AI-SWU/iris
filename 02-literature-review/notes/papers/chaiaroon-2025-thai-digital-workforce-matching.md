---
type: paper
authors: Paweena Chaiaroon, Nuttachot Promrit, Karanya Sitdhisanguan, Sajjaporn Waijanya, Natratanon Kanraweekultana
year: 2025
title: "Digital Workforce Matching: A Machine Learning Approach for Skill-Based Job Classification and Recommendation"
venue: Journal of Current Science and Technology, Vol. 15 No. 4 (Oct–Dec 2025)
doi: https://ph04.tci-thaijo.org/index.php/JCST/article/view/9319
relevance: high
questions: [q-job-posting-sources, q-sample-size, q-segment-taxonomy]
---

## Research Question
How can machine learning and NLP optimise job-to-worker matching in Thailand's digital economy by classifying and recommending jobs based on skill requirements?

## Limitations of Existing Methods
Existing Thai job recommendation systems rely on keyword matching or simple classification without semantic skill understanding; no ML-based skill-to-job matching system existed for Thailand's digital sector specifically.

## Contribution
ML pipeline combining FastText (job categorisation) and Random Forest (skill-based matching) across 20 digital job categories in the Thai market. Skill cluster analysis revealing distinct skill groupings within Thailand's digital sector.

## Proposed Method
NLP preprocessing of Thai job postings from Thailand's leading recruitment platforms; FastText for initial job categorisation; Random Forest for skill-based matching and recommendation; cross-validation for evaluation. 20 digital job categories defined.

## Key Findings
75% accuracy in job recommendations across 20 digital job categories. 86.67% accuracy on previously unseen job postings. Identified distinct skill clusters within Thailand's digital sector. Random Forest outperformed Decision Trees by 4% in accuracy.

## Limitations of This Paper
Specific platform names and posting counts not disclosed. Focused on digital sector only. FastText + Random Forest may be outperformed by transformer-based approaches. Skill extraction method not fully detailed.

## Concepts
[[thai-job-market]] · [[skill-extraction]] · [[job-posting-analysis]] · [[thai-nlp]]

## Questions Addressed
[[q-job-posting-sources]] · [[q-sample-size]] · [[q-segment-taxonomy]]

## Notes for Iris
**Key contribution for Iris**: confirms that 20 digital job categories is a workable granularity for Thailand's digital sector — aligns with our proposed ~12-segment taxonomy. The paper validates that Thai recruitment platform data is sufficient for skill clustering and classification. Platform names not disclosed (limitation for reproducibility), but the feasibility is confirmed. The 75–87% accuracy range on digital Thai job matching is a useful benchmark for our own evaluation in Phase 4.
