# Iris — Literature Review

## Overview

This folder is structured as an Obsidian knowledge graph to support systematic literature review.
Notes are linked bidirectionally so that the Obsidian graph view reveals which research questions
have strong coverage and which are genuine gaps — directly informing our design decisions in Phase 3.

Open `notes/` as your Obsidian vault.

---

## Note Types

| Type | Location | Purpose |
|------|----------|---------|
| Question | `notes/questions/` | One per open research question from the brainstorm — seed nodes of the graph |
| Paper | `notes/papers/` | One per paper read — use LLM ingestion prompt below |
| Concept | `notes/concepts/` | One per method, framework, tool, or idea that appears in multiple papers |

Templates for each type are in `notes/_templates/`.

---

## Workflow

```
1.  Find a paper relevant to one or more open questions
2.  Extract text:  pdftotext paper.pdf - | pbcopy
3.  Paste the ingestion prompt (below) + paper text into LM Studio or Claude
4.  LLM fills the paper note template
5.  Save as  notes/papers/<author>-<year>-<short-title>.md
6.  For each concept slug the LLM suggests, create notes/concepts/<slug>.md if it doesn't exist
7.  Open the relevant question notes and add the paper link + key finding
8.  Repeat
```

When a question note has enough coverage to write a conclusion, draft its section in `literature-review.md`.

---

## LLM Ingestion Prompt

Copy everything below the line, append the paper text at the end, and send to the LLM.

---

```
You are a research assistant helping with a project called IRIS — a skill gap
analysis system for Thai academic programmes. IRIS compares skill distributions
extracted from TQF (มคอ.2) curriculum documents against job posting data from
the Thai labour market, using NLP and agentic AI.

We are conducting a literature review to answer these open research questions:

Q1  [q-skill-taxonomy]       What skill taxonomy or ontology should we use? (O*NET, ESCO, SFIA, or custom?)
Q2  [q-thai-ontology]        Does a Thai skill ontology exist that maps well to TQF content?
Q3  [q-thai-nlp]             How do we handle Thai-language skill extraction — translate first or extract in Thai?
Q4  [q-implied-skills]       How do we handle skills implied by course content but not explicitly stated?
Q5  [q-sample-size]          What is the minimum job posting sample size for a stable career path distribution?
Q6  [q-job-posting-sources]  Where can we obtain Thai job posting datasets ethically?
Q7  [q-temporal-drift]       How do we handle temporal drift in job postings?
Q8  [q-credit-weighting]     Should course credit hours weight the skill contribution?
Q9  [q-visualisation]        What visualisation format is most actionable for academic administrators?
Q10 [q-gap-direction]        Should the gap be symmetric or directional?
Q11 [q-segment-taxonomy]     What is the best practical industry segment taxonomy for Thai context?
Q12 [q-segment-inference]    How reliable is LLM-based segment inference from job description text?
Q13 [q-registry-lookup]      Can Thai company registries (DBD, SET) provide reliable industry segment lookups?

Read the paper below and fill in this note template exactly as shown.
- For "Concepts", suggest 2–5 lowercase-hyphenated slugs for concept notes (e.g. [[esco-ontology]]).
- For "Questions Addressed", list only slugs for questions this paper meaningfully addresses (e.g. [[q-skill-taxonomy]]).
- Keep each section concise — 3 to 5 sentences maximum.

---
type: paper
authors:
year:
title:
venue:
doi:
relevance: high / medium / low
questions: []
---

## Research Question
What problem is this paper solving?

## Limitations of Existing Methods
What gaps or weaknesses in prior work does this paper identify?

## Contribution
What is new in this paper?

## Proposed Method
How do they solve it?

## Key Findings
What did they conclude or demonstrate?

## Limitations of This Paper
What does this paper itself acknowledge as unsolved or out of scope?

## Concepts
(slugs only — e.g. [[esco-ontology]] · [[kl-divergence]])

## Questions Addressed
(slugs only — e.g. [[q-skill-taxonomy]] · [[q-thai-nlp]])

## Notes for Iris
How this maps to our specific design decisions or open questions.

---
[PASTE PAPER TEXT HERE]
```

---

## Obsidian Graph Tips

- **Node colours** — tag questions as `#question`, papers as `#paper`, concepts as `#concept` and colour them differently in Graph View settings
- **Isolated question nodes** — a question with no paper links is a genuine research gap; prioritise finding papers for it
- **Dense concept nodes** — a concept linked by many papers is well-established and safe to rely on in Solution Design
- **Filters** — use the graph filter to show only `#question` + `#paper` nodes when reviewing coverage, or only `#concept` nodes when mapping the method landscape

---

## Synthesis

When the review is complete, synthesise the question notes into `literature-review.md`.
Each question note maps to one section of the final document:
- Status "answered" → write the section
- Status "partial" → write what is known, flag the remaining uncertainty
- Status "open" → record as a risk in the go decision

The go decision gate (in `01-brainstorm/brainstorm.md`) requires all 13 questions to reach at least "partial" before moving to Phase 3.
