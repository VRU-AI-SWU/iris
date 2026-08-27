---
type: question
owner: Data Scientist + Researcher
status: open
---

## Question
The national standard publishes skill demand as **prevalence**, not as a probability
distribution. Which alignment metrics are valid on it?

## Why This Matters for Iris
Measured on the 2026-08-27 snapshot: within any career, `count / percentage` is constant,
so `percentage = count / N × 100` where `N` is the postings behind that career.
Percentages across a career therefore sum to far more than 100 — mean 1,358 %, max
3,596 %. **`percentage` is the share of postings mentioning a skill, not the skill's
share of demand.**

The previous design's primary metric was KL divergence, which requires a probability
distribution. Applying it directly to prevalence is simply invalid; applying it after
renormalisation is valid but measures a different quantity than the one reported.

There is a second constraint: the demand vector is **truncated at ~100 skills per
career**, so the market support is incomplete and any divergence computed over it is
biased by construction.

## Options
1. **Level-aware coverage gap on prevalence** — for each demanded skill, the shortfall
   between the level demanded and the level developed, weighted by prevalence. Directly
   interpretable, no distributional assumption
2. **RCA weighting** — down-weight skills every career demands, up-weight discriminating
   ones; keeps the ranked list actionable
3. **Renormalised KL** — `p_i = count_i / Σ count_j`, then KL(market‖programme); valid,
   but the interpretation changes to "share of skill mentions" and must be stated
4. **Growth-adjusted** — weight by `skillsGrowth`, answering whether the curriculum keeps
   pace rather than merely matches the current stock

## Papers Addressing This
- [[sabet-2024-course-skill-atlas]] — the source of the KL-divergence approach, applied to
  syllabus-derived *distributions*, not prevalence; the distinction was not carried into
  our earlier design
- [[ahadi-2022-skills-taught-vs-sought]] — RCA weighting validated with academic
  stakeholders; RCA is defined on shares and needs the same care
- [[skill-gap-quantification]] — set-based, cosine, KL and chi-square alternatives
- [[macedo-2022-skills-demand-forecasting-temporal]] — grounds the growth-adjusted view
- [[rikala-2024-skill-gaps-industry40-review]] — how the field defines and measures gaps;
  useful for justifying a non-distributional primary metric

## Current Working Answer
status: open

Primary metric: **level-aware coverage gap on prevalence, RCA-weighted** — no
distributional assumption, and it says something a curriculum committee can act on.
Renormalised KL retained as a secondary aggregate score, reported only with its changed
interpretation stated explicitly.

**Hard constraint on every metric and every narrative:** absence from a career's list
means *below the ~100-skill cut-off*, never *not demanded*. This is enforced in the
report template rather than left to the writer.

## Remaining Uncertainty
- Is the cap a display limit or a data limit — can full vectors be obtained for research?
  *(external: สป.อว. / KMITL)*
- Does RCA behave sensibly on prevalence, or does it need redefinition?
- How sensitive is the ranked gap list to the truncation? *(testable by re-ranking on
  progressively truncated vectors)*
- What corpus produced the counts — the range 203 to 6.3 M per career is not plausible
  for Thailand alone, which affects what the metric can be said to measure
