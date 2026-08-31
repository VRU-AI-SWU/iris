---
type: question
owner: Data Scientist + Researcher
status: open
---

<!-- lang-switch -->
**English** · [ภาษาไทย](q-prevalence-metrics.th.md)

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
- **[[saroglou-2025-esco-eqf-linking]]** — ⭐ **added 2026-08-28.** Uses Accuracy@1 and
  strict F1 rather than distributional divergence, and links qualification *levels* (EQF)
  alongside entities — precedent for reporting alignment as ranked, level-aware matches
  rather than as a distance between distributions
- [[zhang-2024-job-market-entity-linking]] — Acc@k reporting across k; the natural metric
  family for a truncated candidate list, and a model for how Iris should report against a
  demand vector capped at ~100 skills

## Current Working Answer
status: open

⚠️ **Corrected 2026-08-28.** An earlier working answer here named a *level-aware coverage
gap* as the primary metric — the shortfall between the level a career demands and the level
a programme develops. **That metric is uncomputable.** A career × skill entry carries only
`count` and `percentage`; the three graded levels belong to the skill entity, not to any
career's requirement. There is no demanded level to take a shortfall against.

Primary metric: **prevalence-weighted coverage gap, RCA-weighted** — which skills a career
demands that the programme does not develop, ranked by prevalence and by career
specificity. No distributional assumption, every term measured.

Depth enters from two directions, kept separate and separately labelled:

- **Curriculum side** — the inferred proficiency level ([[q-level-inference]]), a property
  of the programme
- **Demand side** — the **seniority gradient**: Δ prevalence between paired career rungs.
  13 of 138 digital careers are paired, **12 analysable** (`data-scientist` has four rungs). Data Scientist →
  Senior shows predictive modelling +12.67 pp, applied ML +12.02 pp, multivariate
  statistics +10.49 pp, against Java +2.24 pp and analytical skills −0.58 pp

Crossing the two gives the strongest defensible finding — *"the skills that rise most with
seniority are developed only at foundational level here"* — without ever asserting a level
the market requires.

Renormalised KL is retained as a secondary aggregate, reported only with its changed
interpretation stated explicitly.

### ⚠️ RCA is underspecified — and the choice changes the answer (found 2026-08-28)

"RCA weighting" was carried from [[ahadi-2022-skills-taught-vs-sought]] without stating
**which denominator**. RCA is a ratio of shares:

```
RCA(skill s, career c) = (s's share within c) / (s's share across all careers)
```

The numerator is unambiguous — within a career, the share computed from `count` and from
`percentage` is **identical**, because the per-career posting total `N_c` cancels
(verified on the snapshot).

The denominator is not. Two defensible constructions:

| Global denominator | Meaning |
|---|---|
| **count-weighted** — `Σ_c count / Σ_sc count` | careers contribute in proportion to their posting volume |
| **career-equal** — `Σ_c percentage / Σ_sc percentage` | each career is one observation |

Measured on Data Engineer, these are **not interchangeable**: median |ΔRCA| = 3.02, max
23.86, and the **top-15 ranking overlaps by only 8/15**. Since the RCA-ranked list is what
a curriculum committee is shown, the choice materially changes what they are told to
prioritise.

**Working decision: career-equal weighting.** Count-weighted inherits the unresolved
question of what `N` means — it ranges 203 to 6,291,725 per career, and if that reflects a
corpus artefact rather than real demand, count-weighting propagates the artefact into every
ranking. Career-equal weighting is robust to an uncertainty the project cannot currently
quantify. The decision is stated in outputs and the alternative reported as a sensitivity
check, not silently assumed.

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
