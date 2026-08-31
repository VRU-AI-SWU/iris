---
type: paper
authors: [Sarthi P., Abdullah S., Tuli A., Khanna S., Goldie A., Manning C.D.]
year: 2024
title: "RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval"
venue: ICLR 2024 (arXiv 2401.18059)
doi: 10.48550/arXiv.2401.18059
relevance: medium
questions: [q-implied-skills, q-visualisation]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](sarthi-2024-raptor.th.md)

## Research Question
Can retrieval over long documents be improved by building a **hierarchy of abstractions**
rather than retrieving flat, contiguous chunks?

## Limitations of Existing Methods
Standard RAG retrieves "only short contiguous chunks from a retrieval corpus, limiting
holistic understanding of the overall document context". A question whose answer depends on
material spread across a long document cannot be served by top-k chunk similarity.

## Contribution
A retrieval index built as a tree of recursively clustered and summarised text, allowing
retrieval at several levels of abstraction simultaneously.

## Proposed Method
- Embed text chunks, **cluster them in embedding space**, summarise each cluster with an
  LLM, and repeat — producing a bottom-up tree whose upper nodes are progressively more
  abstract summaries
- At query time, retrieve across multiple tree levels rather than from the leaves alone

## Key Findings
- **+20% absolute accuracy** on the QuALITY benchmark when RAPTOR retrieval is paired with
  GPT-4
- State-of-the-art results on several question-answering benchmarks
- Largest gains on complex, multi-step reasoning over long documents

## Limitations of This Paper
The tree is derived from **embedding-space clustering plus LLM-generated summaries**, not
from the document's own structure, so upper nodes can discard fine-grained detail and the
hierarchy need not correspond to anything a human would recognise as the document's
organisation. Index construction costs an LLM pass over the whole corpus. Evaluated on QA,
where retrieving the *most relevant* passage is the goal.

## Concepts
[[rag-skill-extraction]] · [[curriculum-analytics]] · [[thai-pdf-text-integrity]]

## Questions Addressed
[[q-implied-skills]] · [[q-visualisation]]

## Notes for the Project
The academic reference point for the tree-structured retrieval family that Iris's document
navigation belongs to, and the paper to cite when justifying that choice over flat
chunking.

It also clarifies, by contrast, **why Iris uses PageIndex rather than RAPTOR**. RAPTOR
*infers* a hierarchy by clustering embeddings and summarising; PageIndex *reads* the
hierarchy the document already declares. For a มคอ.2 — whose section structure (หมวดที่ 1–8,
3.1.5 คำอธิบายรายวิชา, the curriculum mapping table) is fixed by regulation — an inferred
hierarchy would be strictly worse than the real one, and its nodes would not carry the page
ranges Iris needs for provenance. RAPTOR's own limitation, that clustering-derived
summaries "can discard fine-grained details", is disqualifying for a task that must recover
every course description without loss.

The deeper caveat applies to both, and is already recorded in the solution proposal:
**RAPTOR optimises retrieving the most relevant node, while Iris needs exhaustive
enumeration.** A +20% QA gain says nothing about whether all 78 courses were found. Tree
retrieval is used to *locate* the section; extraction within it is deterministic and
complete.

Worth revisiting if Iris later ingests documents with no reliable declared structure — an
older มคอ.2 without a usable table of contents, or a vision-derived extraction where
section boundaries are uncertain. There, an inferred hierarchy is better than none.
