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
_(none yet)_

## Current Working Answer
_(pending literature review)_

## Remaining Uncertainty
_(pending literature review)_
