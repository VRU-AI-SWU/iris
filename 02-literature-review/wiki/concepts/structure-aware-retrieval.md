---
type: concept
---

## Definition
**Structure-aware retrieval** indexes a long document by its organisation rather than as a
flat sequence of chunks, so retrieval can operate at several levels of granularity. Two
families differ in where the structure comes from:

| | Inferred structure | Declared structure |
|---|---|---|
| Source | embedding-space clustering + LLM summarisation | the document's own layout / table of contents |
| Example | [[sarthi-2024-raptor]] (RAPTOR), TreeRAG | PageIndex |
| Cost | an LLM pass over the whole corpus | cheap; layout parse plus optional node summaries |
| Node identity | a cluster, with no external meaning | a real section, with a page range |
| Fails when | fine detail is lost in summarisation | the document has no reliable declared structure |

Both outperform flat top-k chunking on long documents — RAPTOR reports **+20% absolute
accuracy** on QuALITY with GPT-4 — because a query whose answer is spread across a document
cannot be served by nearest-chunk similarity.

## Papers That Discuss This
- [[sarthi-2024-raptor]] — recursive clustering and summarisation into a bottom-up tree;
  the reference point for the inferred-structure family, and the source of its known
  limitation that summarisation "can discard fine-grained details"
- [[xu-2025-llm-curricular-analytics]] — RAG grounded in a skill base beats zero-shot for
  course→skill extraction, and copes with brief or abstract course documents

## Related Concepts
[[rag-skill-extraction]] · [[curriculum-analytics]] · [[thai-pdf-text-integrity]]

## Relevance to Iris
A มคอ.2 runs to 200+ pages with a section structure **fixed by regulation** (หมวดที่ 1–8,
`3.1.5 คำอธิบายรายวิชา`, the curriculum mapping table) but formatting and pagination that
vary by university. That is the ideal case for declared-structure indexing: the hierarchy
is real, so inferring one would be strictly worse, and the nodes carry **page ranges** —
which is how Iris gives every extracted course description a citable source page.

One constraint governs the whole use. These systems are built to retrieve the *most
relevant* passage; **Iris needs exhaustive enumeration** — all 78 courses, none missed. A
retrieval benchmark improvement says nothing about completeness. The structure index is
therefore used only to *locate* section boundaries, after which extraction inside the
section is deterministic and complete.

Inferred-structure methods become relevant again if Iris ingests a document with no usable
declared structure — an older มคอ.2 without a machine-readable table of contents, or a
vision-derived extraction where boundaries are uncertain.
