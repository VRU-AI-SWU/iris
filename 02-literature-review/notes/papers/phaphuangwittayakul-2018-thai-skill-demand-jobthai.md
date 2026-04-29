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
- **Data sources**: JobThai.com and JobsDB Thailand (two largest Thai job portals at time of publication)
- **Scraping**: Python with Scrapy + BeautifulSoup; auto-triggered monthly; fields extracted: job title, company, skill level, required experience, education degree, industry, job function, job location, salary, job description, qualification
- **Storage**: MySQL database; each posting stored as a record with 11 attributes
- **Keyword extraction**: RAKE algorithm (Rapid Automatic Keyword Extraction) applied to job description and qualification text; RAKE chosen over Hulth and TextRank for higher effectiveness; output: keywords + frequency per job category
- **Visualisation**: Power BI treemap (job category proportions) and word cloud (skills per job category)
- **Standardisation**: Post-extraction keyword normalisation to reduce synonymous variant forms

## Key Findings
- Job category treemap visualises labour demand distribution across sectors: IT/Technology, Finance, Engineering, Sales/Marketing most prominent
- Word cloud output for IT job category shows dominant skills: programming, database, web development, communication, teamwork — both Thai and English keywords present
- Bilingual (Thai+English) nature of job postings confirmed — skill keywords appear in both languages depending on the posting
- RAKE produces richer, more contextually meaningful keyword phrases compared to single-word extraction methods
- Demonstrated fully automated, monthly-updated pipeline for Thai job market skill demand monitoring

## Limitations of This Paper
Published in 2018 — skill demand landscape has changed significantly. Keyword-based extraction (word clouds) is a shallow method: no semantic normalisation, no taxonomy alignment, no embedding-based clustering. Does not report exact sample size. Word cloud output is not machine-readable for downstream analysis.

## Concepts
[[thai-job-market]] · [[skill-extraction]] · [[thai-nlp]] · [[job-posting-analysis]]

## Questions Addressed
[[q-job-posting-sources]] · [[q-sample-size]] · [[q-segment-taxonomy]]

## Notes for Iris
**Confirms JobThai and JobsDB as viable research sources** — the earliest academic paper to use both platforms. The 2018 vintage is a limitation, but the methodology validates that web scraping from both platforms is feasible for research. The shallow keyword method is a baseline; our embedding + LLM approach is a significant step forward. The bilingual (Thai+English) nature of postings is confirmed here too.
