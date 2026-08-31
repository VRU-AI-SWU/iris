---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](job-posting-analysis.th.md)

## Definition
**Job posting analysis** treats online job advertisements as a corpus for measuring
labour demand: scrape or license postings, extract skills, aggregate by occupation and
time, and read the result as a signal about what employers want.

It became the dominant empirical method in labour-market analytics because postings are
timely, granular and abundant where official statistics are slow and coarse. Its known
biases are equally well established: postings over-represent formal, urban and
white-collar hiring, one posting is not one job, and re-posting inflates counts.

Scale in the literature ranges from [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]]
(Thai postings, keyword matching) through
[[tipsena-2025-predicting-thai-digital-workforce]] (24,494 Thai digital positions from 10
platforms) to [[dixon-2023-occupational-models-42m]] (42 million postings).

## Papers That Discuss This
- [[dixon-2023-occupational-models-42m]] — occupational models from 42M postings; a
  bounded skill vocabulary suffices at that scale
- [[senger-2024-dl-skill-extraction-survey]] — surveys the computational job-market
  analysis field built on this method
- [[tipsena-2025-predicting-thai-digital-workforce]] — 24,494 Thai digital positions
  across 10 platforms, 2023–24
- [[chaiaroon-2025-thai-digital-workforce-matching]] — ML classification over Thai
  postings; 20-role digital taxonomy
- [[lertmethaphat-2025-thai-job-market-nlp]] — Thai job titles; WangchanBERTa conflates
  closely related roles (97.21% similarity Physician/Dentist)
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — JobThai/JobsDB skill demand
- [[macedo-2022-skills-demand-forecasting-temporal]] — forecasting from posting
  time series; credible horizon ≈ 12 months

## Related Concepts
[[thai-job-market]] · [[skill-extraction]] · [[temporal-drift]] ·
[[skill-gap-quantification]] · [[thailand-skill-mapping]]

## Relevance to Iris
**Iris does not analyse job postings and never will.** The original design scraped four
Thai platforms; [[thailand-skill-mapping]] publishes the aggregate demand already, so the
scrapers, the ToS exposure and the reproducibility problem all left the project together.
See [[q-job-posting-sources]] (closed).

The concept still matters for one reason — **Iris consumes the output of this method
second-hand and inherits its biases without controlling them.** The national standard's
demand figures are derived from postings by a process the project cannot inspect, which
is the root of two open concerns in [`data-feasibility.md`](../../../03-solution-design/data-feasibility.md):
per-career posting counts `N` ranging from 203 to 6,291,725, which is not plausible for
Thailand alone, and a demand vector truncated at roughly 100 skills per career.

Everything this literature says about posting-derived demand therefore applies to Iris's
inputs — one posting is not one job, re-posting inflates, formal sectors dominate — and
belongs in the limitations of any result. Tracked in [[q-prevalence-metrics]].
