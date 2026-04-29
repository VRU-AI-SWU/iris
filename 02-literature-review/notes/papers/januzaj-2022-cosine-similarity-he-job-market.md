---
type: paper
authors: Januzaj Y., Luma A.
year: 2022
title: "Cosine Similarity – A Computing Approach to Match Similarity Between Higher Education Programs and Job Market Demands Based on Maximum Number of Common Words"
venue: International Journal of Emerging Technologies in Learning (iJET) Vol.17 No.12, 2022
doi: 10.3991/ijet.v17i12.30375
relevance: low
questions: []
---

## Research Question
How can cosine similarity (with TF-IDF normalisation) be applied to compare textual documents representing higher education programme content and job market requirements?

## Limitations of Existing Methods
Keyword-frequency methods treat all words equally, inflating similarity scores for common words. Non-normalised vector comparisons are sensitive to document length differences.

## Contribution
Methodology demonstration of cosine similarity + TF-IDF for document similarity measurement. Argues that TF-IDF normalisation produces more meaningful similarity scores than raw word frequency.

## Proposed Method
Four fabricated toy documents (sentences, not real programme or job posting data). Builds term-frequency matrix. Computes cosine similarity pairwise. Applies TF-IDF reweighting. Compares normalised vs. non-normalised results.

## Key Findings
TF-IDF normalisation changes cosine similarity scores compared to raw frequency. Documents with more common words in the same context score higher. Mathematical demonstration only — no empirical dataset used.

## Limitations of This Paper
**Critical limitation**: This is not an actual comparison of HE programmes with job market data. The four "documents" used are fabricated single sentences (e.g., "Market demands are met by university programs"). No real programme curricula, no real job postings, no evaluation metrics. The paper is a computing methodology tutorial, not an empirical curriculum-job market alignment study. The title is misleading.

## Concepts
[[cosine-similarity]]

## Questions Addressed
*(none)*

## Notes for Iris
**Low operational value.** This paper confirms cosine similarity + TF-IDF as a method class, but provides no empirical evidence about how well it works for real curriculum-to-job-market matching. Do not cite as evidence for cosine similarity as a gap metric — cite sabet-2024 or senger-2024 instead. May be useful only as a minimal background reference for the cosine similarity method definition.
