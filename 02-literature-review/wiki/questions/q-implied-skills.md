---
type: question
owner: AI Engineer + Data Scientist
status: open
---

## Question
How do we handle skills that are implied by course content but not explicitly stated in the course description?

## Why This Matters for Iris
Course descriptions vary widely in richness. A course on "Database Systems" implies SQL, normalisation, and indexing even if those words do not appear. Ignoring implied skills underestimates a programme's actual skill coverage.

## Initial Hypothesis
LLM-based extraction with instructed inference (asking the model to reason about implied skills from the course title and description context) may capture a significant portion of implied skills. The reliability of this needs validation.

## Papers Addressing This
- [[xu-2025-llm-curricular-analytics]] — LLMs handle brief and abstract curriculum documents well; RAG outperforms zero-shot for skill extraction
- [[luyen-2025-skill-decomposition-ontology]] — few-shot prompting with exemplars improves skill granularity consistency; LLMs can infer sub-skills from high-level descriptions
- [[senger-2024-dl-skill-extraction-survey]] — the field lacks consensus on what counts as an "implied" skill vs an "explicit" skill

## Current Working Answer
status: partial

LLMs with few-shot prompting (exemplars of good extraction including implied skills) are the most promising approach for capturing implied skills. RAG grounded in a growing skill vocabulary further helps by providing context for what skills are typically associated with a given topic. Zero-shot extraction likely misses implied skills — this is a known risk.

## Remaining Uncertainty
No benchmark exists for evaluating implied skill extraction specifically. We need to define evaluation criteria (what counts as a correctly inferred implied skill?) before we can measure extraction quality in Phase 4.
