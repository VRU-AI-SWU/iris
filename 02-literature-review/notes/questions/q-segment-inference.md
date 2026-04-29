---
type: question
owner: AI Engineer + Data Scientist
status: open
---

## Question
How reliable is LLM-based segment inference from job description text alone, when employer identity is hidden?

## Why This Matters for Iris
Agency postings — common in Thailand — intentionally hide the employer. Our 3-tier enrichment pipeline falls back to LLM classification from job description vocabulary for these cases. If this tier is unreliable, a significant portion of postings will be mis-segmented.

## Initial Hypothesis
LLMs should perform reasonably well because industry segments produce distinctive vocabulary patterns (fintech uses different language than manufacturing). Reliability likely varies by segment — Technology/Software may be easy; Government vs. Professional Services may be harder to distinguish.

## Papers Addressing This
_(none yet)_

## Current Working Answer
_(pending literature review)_

## Remaining Uncertainty
_(pending literature review)_
