---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](thai-job-market.th.md)

## Definition
The **Thai labour market** context for computing graduates: which roles exist, what
employers ask for, and how that is documented in Thai-language sources.

What the corpus establishes:

| Finding | Source |
|---|---|
| A 20-category taxonomy of Thai digital job roles | [[chaiaroon-2025-thai-digital-workforce-matching]] |
| 24,494 Thai digital positions across 10 platforms (2023–24); 5-segment DEPA framework | [[tipsena-2025-predicting-thai-digital-workforce]] |
| A 3-category Thai digital competency taxonomy (EFA-derived) | [[siddoo-2019-thai-digital-workforce-competency]] |
| A confirmed skill mismatch between Thai employers' priorities and graduate supply | [[weerasombat-2025-thai-employer-skill-priorities]] |
| Thai job titles resist fine-grained discrimination by Thai LMs | [[lertmethaphat-2025-thai-job-market-nlp]] |

Principal platforms in the research literature: JobThai, JobsDB Thailand, JOBBKK,
JOBTOPGUN. Thai PDPA 2019 governs collection; job metadata is not personal data.

## Papers That Discuss This
- [[chaiaroon-2025-thai-digital-workforce-matching]] — ML skill-based job classification;
  20-category Thai digital taxonomy
- [[tipsena-2025-predicting-thai-digital-workforce]] — 24,494 positions, 10 platforms,
  DEPA 5-segment framework
- [[siddoo-2019-thai-digital-workforce-competency]] — EFA-derived competency categories
- [[weerasombat-2025-thai-employer-skill-priorities]] — employer priorities and the
  confirmed mismatch
- [[phaphuangwittayakul-2018-thai-skill-demand-jobthai]] — earliest Thai skill-demand
  analysis in the corpus
- [[lertmethaphat-2025-thai-job-market-nlp]] — Thai job-title discrimination failure

## Related Concepts
[[job-posting-analysis]] · [[thailand-skill-mapping]] · [[thai-nlp]] · [[tpqi-framework]] ·
[[skill-gap-quantification]]

## Relevance to Iris
This literature **motivates** the project and no longer **supplies** it.
[[weerasombat-2025-thai-employer-skill-priorities]] confirms the mismatch Iris exists to
measure, and [[siddoo-2019-thai-digital-workforce-competency]] shows Thai competency
frameworks stopping at a granularity too coarse to act on — the gap the national standard
now fills at 4,376 entries.

The role taxonomies are superseded rather than wrong. Chaiaroon's 20 categories and
Tipsena's 5 DEPA segments were reasonable answers when no official list existed;
[[thailand-skill-mapping]] publishes **138 digital careers** with demand vectors attached,
and a career must be one the standard names for its demand to be readable at all. See
[[q-segment-taxonomy]] (superseded).

⚠️ **One caution this concept carries into the current design.** Everything above concerns
the *Thai* labour market, and Iris's demand data may not. Per-career posting counts in the
standard range from 203 to 6,291,725, which is not plausible for Thailand alone — so until
สป.อว./KMITL clarify the corpus, Iris does not claim to measure Thai labour demand
specifically, and the Thai-specific findings here cannot be assumed to describe its inputs.
See [`data-feasibility.md`](../../../03-solution-design/data-feasibility.md).
