---
type: concept
---

## Definition
A **sentence embedding** maps a phrase or sentence to a fixed-length dense vector such
that semantically similar inputs land near each other, enabling similarity search over
text without exact term overlap. Standard models include Universal Sentence Encoder (USE),
Sentence-BERT, and multilingual variants.

Similarity is measured with [[cosine-similarity]]. The critical property for occupational
work is **discrimination**: an embedding space that places related-but-distinct terms too
close is unusable for retrieval, however well it performs on general benchmarks.
[[lertmethaphat-2025-thai-job-market-nlp]] is the cautionary case — WangchanBERTa put
Thai *Physician* and *Dentist* at 97.21% similarity, while USE with XGBoost reached ~90%
accuracy on the same discrimination task.

## Papers That Discuss This
- [[lertmethaphat-2025-thai-job-market-nlp]] — the discrimination failure; USE preferred
  over [[wangchanberta]] for fine-grained Thai occupational terms
- [[kavargyris-2025-escox-skill-extraction]] — ESCO embeddings for skill/occupation linking
- [[zhang-2024-job-market-entity-linking]] — bi-encoder retrieval over 13,890 ESCO skills;
  Acc@32 (48.98%) roughly double Acc@1 (23.55%)
- [[arslan-2026-turkish-skill-extraction]] — embedding retrieval then LLM re-ranking is
  the best low-resource configuration
- [[saroglou-2025-esco-eqf-linking]] — **entity-level embeddings outperform full-sentence
  embeddings** for the similarity module; fine-tuned `all-mpnet-base-v2`
- [[le-2026-competency-tagging-evidence]] — BM25 plus graph-enriched profiles; lexical
  retrieval remains competitive

## Related Concepts
[[cosine-similarity]] · [[skill-entity-linking]] · [[skill-normalisation]] ·
[[thai-bert]] · [[rag-skill-extraction]]

## Relevance to Iris
Sentence embeddings are the **dense half of candidate retrieval**: the 4,376 national
skills are embedded once from title plus definition and held as a 13 MB in-memory matrix,
against which each course description is scored. No vector database — at this size exact
cosine over the full matrix is microseconds.

Four constraints come from the papers above.

**Discrimination over benchmark rank.** The vocabulary contains near-identical Thai
phrases — *Relational* vs *Logical Data Modeling* — so the model is chosen on measured
retrieval recall against these entries, not on general Thai benchmarks. This is what rules
out [[thai-bert]].

**Multilingual, necessarily.** Skill titles exist in Thai and English, and course
descriptions code-switch, so both must occupy one space.

**Lexical retrieval alongside, not instead.** The `tools` type (`Docker`, `.NET Core`,
`Apache Spark`) matches lexically far better than semantically, and
[[le-2026-competency-tagging-evidence]] reached its results with BM25 in the retrieval
stage.

**Embed the right unit.** [[saroglou-2025-esco-eqf-linking]] found entity-level embeddings
beating full-sentence ones for similarity — worth testing whether Iris should embed skill
title alone, title+definition, or both as separate vectors.
