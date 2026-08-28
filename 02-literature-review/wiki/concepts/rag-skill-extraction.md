---
type: concept
---

## Definition
Retrieval-Augmented Generation (RAG) applied to skill extraction: rather than asking an LLM to extract skills from text in zero-shot, RAG first retrieves relevant skill definitions from a knowledge base (e.g. a skill taxonomy or prior extracted skills), then prompts the LLM to extract and normalise skills in context of the retrieved examples. This grounds the extraction in an existing skill vocabulary and reduces hallucination.

## Papers That Discuss This
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill base beats zero-shot for
  course→skill extraction
- [[arslan-2026-turkish-skill-extraction]] — embedding retrieval + LLM re-ranking is the
  best configuration for a low-resource language
- [[le-2026-competency-tagging-evidence]] — BM25 + graph-enriched retrieval, then
  constrained LLM selection with evidence spans
- [[zhang-2024-job-market-entity-linking]] — bi-encoder retrieval over a 13,890-entry
  taxonomy; Acc@32 roughly doubles Acc@1
- [[sarthi-2024-raptor]] — hierarchical retrieval for long documents
- [[kavargyris-2025-escox-skill-extraction]] — LLM + taxonomy embeddings against ESCO

## Related Concepts
[[llm-skill-extraction]] · [[zero-shot-prompting]] · [[few-shot-prompting]] · [[skill-extraction]]

## Relevance to Iris
xu-2025-llm-curricular-analytics shows RAG is the top-performing strategy for curriculum skill extraction. Our current design uses zero-shot LLM extraction — this finding suggests we should consider RAG with a growing skill knowledge base. In practice: as we extract skills from the first set of TQF documents, those skills become the retrieval corpus for subsequent extractions, improving consistency.
