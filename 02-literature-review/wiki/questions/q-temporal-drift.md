---
type: question
owner: Data Engineer + Data Scientist
status: open
---

## Question
How do we handle temporal drift in job postings — the fact that skill demand shifts over time?

## Why This Matters for Iris
A dataset of job postings from two years ago may not reflect current market demand. If we pool postings across multiple years, older postings may dilute the signal for recently-emerging skills.

## Initial Hypothesis
None. Options include: time-windowed snapshots (most recent N months only), decay weighting (recent postings weighted higher), or trend analysis (track gap evolution over time). The best approach depends on how fast the Thai CS job market evolves.

## Papers Addressing This
- [[macedo-2022-skills-demand-forecasting-temporal]] — LSTM/GRU time series forecasting; 120 monthly observations; credible horizon ≈ 12 months
- [[fettach-2025-skill-demand-temporal-kg]] — temporal KG embeddings; soft skills stable, technical skills volatile; Java declining since 2022
- [[seif-2024-dynamic-jobs-skills-kg]] — Singapore dynamic JSKG; sliding window weighted averages; expert seed + job posting signals
- [[sabet-2024-course-skill-atlas]] — uses KL divergence to measure temporal drift between curriculum and market snapshots

## Current Working Answer
status: partial

**How fast do skills change?**
- macedo-2022 establishes the key empirical finding: credible forecast horizon for skill demand is approximately **12 months**. Beyond 12 months, prediction error grows substantially.
- Soft skills (teamwork, communication) are temporally stable across years (fettach-2025). Technical skills (cloud computing, specific frameworks) can shift significantly within 12–24 months.
- This means job posting data older than 12–18 months should be treated as potentially stale for technical skills.

**How should Iris v1 handle temporal drift?**

**For the static snapshot approach (v1 design)**:
- Collect job postings from a clearly bounded **12-month window** (most recent available)
- Document the collection date prominently — gap scores are valid as of that snapshot
- Report temporal limitation explicitly: Iris v1 is a point-in-time gap score, not a live signal

**For a future live system (beyond v1)**:
- Adopt the seif-2024 sliding window weighted average approach: a 6–12 month rolling window that downweights older signals
- This is the production-ready architecture; v1 static snapshot is an intentional simplification

**Urgency annotation by skill type**:
- Technical skill gaps should carry a higher urgency flag (they become stale faster)
- Soft/professional skill gaps are more stable across time — lower temporal urgency

## Remaining Uncertainty
How fast does the Thai CS job market specifically evolve? We have no Thai-specific temporal analysis. This is a research gap — our Phase 4 convergence analysis could include a temporal stability analysis if we collect data across two time periods.
