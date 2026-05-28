---
type: paper
authors: Le Ngoc Luyen, Marie-Hélène Abel
year: 2025
title: "Automated Skill Decomposition Meets Expert Ontologies: Bridging the Granularity Gap with LLMs"
venue: arXiv:2510.11313 (cs.AI)
doi: 10.48550/arXiv.2510.11313
relevance: medium
questions: [q-skill-taxonomy, q-implied-skills]
---

## Research Question
How can LLMs automatically decompose high-level skills into fine-grained sub-skills while maintaining structural alignment with expert ontologies?

## Limitations of Existing Methods
Expert ontologies are either too coarse (missing fine-grained skill distinctions) or too granular (impractical for use). Manually decomposing skills into appropriate granularity is expensive and does not scale. Earlier automated approaches lack alignment with expert knowledge structures, producing decompositions inconsistent with established ontologies.

## Contribution
An evaluation framework for LLM skill decomposition with two new metrics: semantic F1-score (content accuracy) and hierarchy-aware F1-score (structural correctness relative to ontology). Evidence that few-shot prompting with exemplars improves ontology-aligned decomposition.

## Proposed Method
Zero-shot and few-shot prompting of LLMs for skill decomposition; embedding-based semantic matching for evaluation; tested on ROME-ESCO-DecompSkill curated dataset. Latency analysis included to assess practical viability.

## Key Findings
Few-shot prompting consistently stabilises phrasing and granularity, improving alignment with expert ontologies compared to zero-shot. Zero-shot provides a solid but less consistent baseline. Exemplar-guided prompts sometimes exceed zero-shot in speed efficiency due to more schema-compliant output (less post-processing needed).

## Limitations of This Paper
Tested on a curated subset of ROME-ESCO; may not generalise to all ontologies or domains. European/English ontologies only. Does not address low-resource language scenarios.

## Concepts
[[skill-ontology]] · [[llm-skill-extraction]] · [[few-shot-prompting]] · [[esco-ontology]] · [[skill-decomposition]]

## Questions Addressed
[[q-skill-taxonomy]] · [[q-implied-skills]]

## Notes for Iris
The granularity problem is directly relevant — our emergent vocabulary clustering must decide at what level of granularity to define skills. The finding that few-shot prompting improves consistency is actionable: our LLM ingestion prompts for TQF course descriptions should include exemplars of good skill extractions, not just zero-shot instructions. The hierarchy-aware F1-score metric is worth considering for evaluating our extraction quality in Phase 4.
