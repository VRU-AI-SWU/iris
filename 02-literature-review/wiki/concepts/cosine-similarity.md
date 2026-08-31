---
type: concept
---

<!-- lang-switch -->
**English** · [ภาษาไทย](cosine-similarity.th.md)

## Definition
**Cosine similarity** measures the angle between two vectors, ignoring magnitude:

```
cos(A, B) = (A · B) / (‖A‖ ‖B‖)     ∈ [-1, 1]
```

It is the default similarity for [[sentence-embedding]] retrieval because embedding norm
carries little meaning while direction carries the semantics. It also serves as a symmetric
aggregate comparison between two frequency or distribution vectors — an alternative to
[[kl-divergence]], which is asymmetric and directional.

[[januzaj-2022-cosine-similarity-he-job-market]] applies it at its simplest: cosine over
common-word vectors to match higher-education programmes to job-market demand — an
approach that establishes the idea while ignoring synonymy and, being symmetric, saying
nothing about *which side* is deficient.

## Papers That Discuss This
- [[januzaj-2022-cosine-similarity-he-job-market]] — cosine over common words to match HE
  programmes to job-market demand
- [[lertmethaphat-2025-thai-job-market-nlp]] — cosine as the diagnostic that exposed
  WangchanBERTa's failure (97.21% Physician/Dentist)
- [[zhang-2024-job-market-entity-linking]] — bi-encoder retrieval scored by embedding
  similarity
- [[saroglou-2025-esco-eqf-linking]] — entity-level vs sentence-level embeddings compared
  under cosine similarity

## Related Concepts
[[sentence-embedding]] · [[kl-divergence]] · [[skill-gap-quantification]] ·
[[skill-entity-linking]]

## Relevance to Iris
Used in exactly one place: **exact cosine between a course-description embedding and the
4,376-row skill matrix**, to generate candidates for adjudication. At this size the
retrieval is a single matrix multiply, so no approximate index and no vector database.

It is deliberately **not** used as a gap metric. Iris's earlier design listed cosine
similarity as an aggregate programme-to-market score, following
[[januzaj-2022-cosine-similarity-he-job-market]]. Two objections retired it. Cosine is
symmetric, so it cannot express the directional question a curriculum committee actually
asks — *what do our graduates lack?* — which is the argument preserved in
[[q-gap-direction]]. And the standard publishes prevalence rather than a distribution, so
vector-space distance between the two sides needs justification the design would rather
not owe; see [[q-prevalence-metrics]].

The remaining role for cosine at the reporting level is **programme-to-programme
comparison**, where symmetry is appropriate — neither curriculum is the reference.
