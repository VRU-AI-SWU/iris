---
type: paper
authors: Chaiaroon P., Promrit N., Sitdhisanguan K., Waijanya S., Kanraweekultana N.
year: 2025
title: "Digital Workforce Matching: A Machine Learning Approach for Skill-Based Job Classification and Recommendation"
venue: Journal of Current Science and Technology (JCST), Vol. 15 No. 4, Oct–Dec 2025, Article 137, Rangsit University
doi: 10.59796/jcst.V15N4.2025.137
relevance: high
questions: [q-job-posting-sources, q-sample-size, q-segment-taxonomy]
---

## Research Question
How can ML and NLP optimise digital workforce matching in Thailand by classifying job positions and recommending them based on skill requirements across 20 digital job categories?

## Limitations of Existing Methods
Existing Thai job recommendation systems use keyword matching or simple classification without semantic skill understanding. No ML-based, skill-driven job matching system existed for Thailand's digital sector. Job posting data is fragmented across platforms with inconsistent terminology and no centralised skill taxonomy.

## Contribution
End-to-end pipeline: job position classification (FastText) + skill extraction (PyThaiNLP dictionary matching) + skill-based job recommendation (Random Forest). Applied to 11,365 job positions from 5 Thai platforms. Provides the most detailed published taxonomy of Thai digital job roles (20 categories) with mapped skill clusters.

## Proposed Method
- **Platforms**: Top 5 Thai job posting websites by Google Trends 2021: **Jobthai, Jobsdb, JOBBKK, JOBTOPGUN, LinkedIn**
- **Data collected**: 11,365 digital job positions; fields: job title, company, location, salary, posted date, job description, responsibilities, qualifications
- **Skill extraction**: Custom skill dictionary of **10,424 digital skills** (tokenised with PyThaiNLP); binary skill presence per posting; frequency-based filtering (skills in >20% of postings per category → 1, else 0) to reduce noise
- **Job classification**: FastText model; input = PyThaiNLP-tokenised job title + n-grams (n=2); 100-dimensional embeddings; vocabulary of 7,060 words; classifies into 20 job position groups
- **Skill-based recommendation**: Random Forest trained on (job_id, skill vector) → job position label
- **Evaluation**: Cross-validated; accuracy on validation set and unseen postings

## Key Findings
- **75% recommendation accuracy** across 20 digital job categories; **86.67% on unseen job postings**
- Random Forest outperforms Decision Tree by 4% in accuracy
- FastText + PyThaiNLP tokenisation is effective for Thai-English bilingual job title classification
- At least 4 input skills needed to clearly separate job categories in the recommendation system
- Distinct skill clusters confirmed per job group: e.g., Full-stack Developers emphasise Java; Software Engineers emphasise C# and architectural skills

**The 20 Thai digital job position groups:**
1. .Net-developer/programmer
2. Back-end-developer/programmer
3. Business-analyst
4. Cloud (cloud engineer/architect)
5. Data-analyst
6. Data-engineer
7. Database-administrator
8. DevOps
9. Front-end-developer/programmer
10. Full-stack-developer/programmer
11. Information-security
12. IT-support
13. Java-developer/programmer
14. Mobile-developer/programmer
15. Network-engineer
16. Project-manager
17. Software-engineer
18. Tester
19. UX/UI-designer
20. Web-developer/programmer

## Limitations of This Paper
Focused on digital sector only; no non-digital roles. Dataset: 11,365 positions — relatively small; no inter-rater reliability reported for labelling. FastText + Random Forest likely outperformed by transformer-based approaches. Skill dictionary (10,424 skills) manually constructed — coverage gaps possible. LinkedIn inclusion raises TOS concerns.

## Concepts
[[thai-job-market]] · [[skill-extraction]] · [[job-posting-analysis]] · [[thai-nlp]] · [[skill-taxonomy]]

## Questions Addressed
[[q-job-posting-sources]] · [[q-sample-size]] · [[q-segment-taxonomy]]

## Notes for Iris
**Three high-value contributions to Iris design:**
1. **The 20-category Thai digital job taxonomy is directly adoptable**: This is the most detailed published Thai digital role taxonomy to date. Our career path scope for Iris v1 should align with or subset these 20 categories. The taxonomy confirms our intuition about relevant roles (Data Analyst, Data Engineer, Software Engineer, DevOps, Business Analyst, etc.) and adds useful specificity (e.g., separate Java Developer vs. .Net Developer vs. Full-stack Developer).
2. **5 Thai platforms confirmed**: Jobthai + Jobsdb + JOBBKK + JOBTOPGUN + LinkedIn is a validated multi-platform scraping approach. For Iris data collection, target at minimum Jobthai + Jobsdb + JOBBKK to cover the Thai digital job market adequately (skip LinkedIn due to anti-scraping).
3. **Skill dictionary scale**: 10,424 digital skills from 11,365 postings — a vocabulary of this size is expected from Thai digital job postings. Our emergent vocabulary approach should expect to converge on a smaller curated set (200–500 skills) after deduplication and normalisation.
