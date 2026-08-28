---
type: concept
---

## Definition
**Temporal drift** is the decay of a skill-demand measurement as the labour market moves
away from the moment it was taken. A snapshot describes the past; a curriculum designed
against it graduates students years later.

Two empirical anchors from the corpus:

- **A credible forecast horizon of about 12 months.**
  [[macedo-2022-skills-demand-forecasting-temporal]] finds skill-demand forecasting
  degrades beyond roughly a year.
- **Drift is not uniform across skills.**
  [[fettach-2025-skill-demand-temporal-kg]] finds soft skills stable while technical
  skills are volatile — so a stale snapshot misleads most about exactly the skills a
  computing curriculum cares about.

Mitigations in the literature: sliding-window weighted averages over a dynamic knowledge
graph ([[seif-2024-dynamic-jobs-skills-kg]]), longitudinal panels
([[sabet-2024-course-skill-atlas]]), and explicit forecasting.

## Papers That Discuss This
- [[macedo-2022-skills-demand-forecasting-temporal]] — LSTM/GRU forecasting; credible
  horizon ≈ 12 months
- [[fettach-2025-skill-demand-temporal-kg]] — temporal KG embeddings; soft skills stable,
  technical skills volatile
- [[seif-2024-dynamic-jobs-skills-kg]] — Singapore dynamic jobs-skills KG; sliding-window
  weighted averages
- [[sabet-2024-course-skill-atlas]] — national longitudinal syllabus dataset; drift
  measured over years

## Related Concepts
[[job-posting-analysis]] · [[thailand-skill-mapping]] · [[skill-gap-quantification]] ·
[[kl-divergence]]

## Relevance to Iris
The pivot changed drift from a **threat** into a **signal**.

Under the original design — one static scrape — drift was an unmeasurable risk to
validity, and the response was defensive: a 12-month collection window, documented and
hoped to hold. [[thailand-skill-mapping]] publishes a per-skill **`growth` rate per
career** (10,815 values across the digital industry, range 0–706%), so the direction and
speed of change arrive with the data.

That supports a question the earlier design could not ask: not only *"does this curriculum
cover what the market wants now?"* but *"is it keeping pace with what is rising?"* — the
growth-adjusted view in [[q-prevalence-metrics]]. Fettach et al.'s finding tells us how to
read it: high growth on a technical skill is a real signal, the same figure on a soft
skill is more likely noise.

Two residual concerns. The standard's own snapshot is dated (July 2025 content, mirrored
2026-08-27) and its refresh cadence is unknown, so Iris's snapshot ages the same way any
scrape would — the pinned date is recorded with every analysis for exactly this reason.
And it remains unclear whether the underlying posting counts are a point-in-time
measurement or a cumulative total, which changes what `growth` means. See
[[q-temporal-drift]].
