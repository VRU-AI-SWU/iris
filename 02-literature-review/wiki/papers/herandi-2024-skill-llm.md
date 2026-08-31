---
type: paper
authors: [Herandi A., Li Y., Liu Z., Hu X., Cai X.]
year: 2024
title: "Skill-LLM: Repurposing General-Purpose LLMs for Skill Extraction"
venue: arXiv (cs.CL) 2410.12052
doi: 10.48550/arXiv.2410.12052
relevance: low
questions: [q-implied-skills, q-skill-taxonomy]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](herandi-2024-skill-llm.th.md)

## Research Question
Does fine-tuning a general-purpose LLM for skill extraction outperform the NER-based
approaches that dominate the field?

## Limitations of Existing Methods
NER-based skill extraction from job descriptions "lacks the precision needed for effective
hiring processes" despite being the standard approach.

## Contribution
Fine-tuning of a specialised Skill-LLM plus a lightweight variant, reported to outperform
prior state of the art on skill extraction.

## Proposed Method
Fine-tuning a general-purpose LLM on skill-extraction data, with a smaller distilled model
for deployment. The public abstract does not name the base model or give fine-tuning
details.

## Key Findings
The authors report outperforming existing SOTA techniques. **No F1 scores or quantitative
comparisons against BERT-based baselines are available in the public abstract**, so the
magnitude of the improvement cannot be assessed from the accessible material.

## Limitations of This Paper
Extraction only — surface skill strings, with no linking to a controlled vocabulary, so it
inherits the terminology-inconsistency problem documented in
[[senger-2024-dl-skill-extraction-survey]]. Fine-tuning requires labelled data that does
not exist for Thai. Reported without accessible numbers.

## Concepts
[[skill-entity-linking]] · [[rag-skill-extraction]]

## Questions Addressed
[[q-implied-skills]] · [[q-skill-taxonomy]]

## Notes for the Project
Recorded for completeness as part of the fine-tuning branch of the field, and **not adopted**.

Two reasons. First, it solves the *extraction* problem — producing skill strings — which the
pivot removed from Iris's scope; the national vocabulary makes linking, not extraction, the
task. Second, fine-tuning presupposes labelled Thai skill data, which does not exist and
which Iris would have to create; the annotation budget in Sprint 4 is committed to
*evaluation*, where it buys a defensible quality claim, rather than to training data.

The comparison worth keeping is with [[arslan-2026-turkish-skill-extraction]], which faced
the same absence of labelled data in a low-resource language and answered it with prompting
plus retrieval rather than fine-tuning — and beat supervised sequence labelling doing so.
That is the branch Iris follows.

Revisit only if Sprint 4 shows retrieval-plus-adjudication plateauing well below what the
project needs, and only after the annotated set exists as a by-product of evaluation.
