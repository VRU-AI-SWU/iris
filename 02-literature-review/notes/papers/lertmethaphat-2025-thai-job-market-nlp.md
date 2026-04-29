---
type: paper
authors: Nuttapol Lertmethaphat, Nuarpear Lekfuangfu, Pucktada Treeratpituk
year: 2025
title: "Exploring the Thai Job Market Through the Lens of Natural Language Processing and Machine Learning"
venue: PIER Discussion Paper 228, Puey Ungphakorn Institute for Economic Research
doi: https://www.pier.or.th/dp/228/
relevance: high
questions: [q-thai-nlp, q-job-posting-sources]
---

## Research Question
How can NLP and ML be used to standardise high-frequency Thai job posting data into occupational codes for real-time labour market monitoring?

## Limitations of Existing Methods
Manual classification of Thai job titles into standard occupational codes (ISCO-2008) is too labour-intensive for the volume and velocity of online job posting data. Existing multilingual models handle Thai poorly; bilingual (Thai/English) job titles compound the difficulty.

## Contribution
An algorithm that automatically maps Thai job titles to ISCO-2008 4-digit occupational codes using sentence embeddings. Validated on data from major Thai online job posting platforms. Enables high-frequency, real-time Thai labour market monitoring at scale.

## Proposed Method
Sentence embedding of job titles using Universal Sentence Encoder (USE) for English and WangchanBERTa for Thai; similarity-based matching to ISCO-2008 codes. Tested on bilingual (Thai and English) job title data from major Thai job portals.

## Key Findings
WangchanBERTa outperforms USE for Thai-language job titles. Bilingual job titles require both Thai and English embeddings for good coverage. The approach enables real-time monitoring and significantly reduces manual processing burden. Thai job portals produce sufficient data volume for labour market tracking.

## Limitations of This Paper
Addresses occupation classification (ISCO codes), not skill extraction — a coarser granularity than what Iris requires. Does not reveal which specific Thai job platforms were used. ISCO taxonomy may not capture the skill-level distinctions Iris needs.

## Concepts
[[thai-nlp]] · [[wangchanberta]] · [[isco-classification]] · [[thai-job-market]] · [[sentence-embedding]]

## Questions Addressed
[[q-thai-nlp]] · [[q-job-posting-sources]]

## Notes for Iris
The first Thai-specific paper directly relevant to our pipeline. WangchanBERTa is validated for Thai job posting NLP — directly applicable to our Thai skill extraction task. Confirms bilingual (Thai+English) job postings are common on Thai platforms, which aligns with our expectation. The occupation-level focus (ISCO) vs our skill-level focus means we need finer-grained extraction, but the embedding approach transfers. Important: does not name which platforms were used — a gap we need to fill for Q6.
