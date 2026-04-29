---
type: paper
authors: Phaphuangwittayakul A., Saranwong S., Panyakaew S.N., Inkeaw P., Chaijaruwanich J.
year: 2018
title: "Analysis of Skill Demand in Thai Labor Market from Online Jobs Recruitment Websites"
venue: 15th International Joint Conference on Computer Science and Software Engineering (JCSSE 2018), Nakhon Ratchasima, IEEE
doi: 10.1109/JCSSE.2018.8457393
relevance: high
questions: [q-job-posting-sources, q-sample-size, q-segment-taxonomy]
---

## Research Question
What skills are in demand in the Thai labour market, and how can job posting data from Thai recruitment websites be analysed to surface these demands?

## Limitations of Existing Methods
Prior analysis of Thai labour market skill demand relied on surveys or manual review; no automated analysis of Thai job posting data existed at scale. Skill demand was not systematically broken down by job function or firm type.

## Contribution
First systematic NLP-based analysis of Thai labour market skill demand using web scraping from JobThai and JobsDB. Keyword extraction and word cloud visualisation applied to job descriptions and qualification requirements across job functions.

## Proposed Method
Web scraping of job postings from JobThai.com and JobsDB Thailand; keyword extraction from job description and qualification fields; visualisation via word clouds per job function. Exact posting count not published.

## Key Findings
Skill demand in Thailand prioritised in order: cognitive skills > social skills > EQ > thinking skills > growth mindset > information and digital literacy > communication > creativity. Significant variation in skill demand across firm sizes. Both Thai and English keywords present in job postings.

## Limitations of This Paper
Published in 2018 — skill demand landscape has changed significantly. Keyword-based extraction (word clouds) is a shallow method: no semantic normalisation, no taxonomy alignment, no embedding-based clustering. Does not report exact sample size. Word cloud output is not machine-readable for downstream analysis.

## Concepts
[[thai-job-market]] · [[skill-extraction]] · [[thai-nlp]] · [[job-posting-analysis]]

## Questions Addressed
[[q-job-posting-sources]] · [[q-sample-size]] · [[q-segment-taxonomy]]

## Notes for Iris
**Confirms JobThai and JobsDB as viable research sources** — the earliest academic paper to use both platforms. The 2018 vintage is a limitation, but the methodology validates that web scraping from both platforms is feasible for research. The shallow keyword method is a baseline; our embedding + LLM approach is a significant step forward. The bilingual (Thai+English) nature of postings is confirmed here too.
