---
type: concept
---

## Definition
**Skill decomposition** breaks a coarse skill statement into finer constituent skills, to
resolve the **granularity mismatch** between how text names a capability and how a
taxonomy enumerates it.

The mismatch runs both ways. A course description says *"การพัฒนาเว็บ"* (web development)
where the vocabulary holds a dozen specific entries; or it lists `HTML`, `CSS` and
`JavaScript` where the taxonomy has one broader entry. Neither side is wrong; they are
described at different resolutions.

[[luyen-2025-skill-decomposition-ontology]] shows LLMs can decompose skills to match an
expert ontology's granularity, with [[few-shot-prompting]] closing the gap — examples
convey the intended resolution better than instructions do.

## Papers That Discuss This
- [[luyen-2025-skill-decomposition-ontology]] — LLM decomposition aligned to expert
  ontologies; few-shot prompting improves alignment
- [[le-2026-competency-tagging-evidence]] — same group; segments resources into
  *pedagogical fragments* before tagging, a granularity decision at the input end
- [[dong-2023-out-of-kb-mention-discovery]] — the boundary case: decomposition cannot help
  when the constituent simply is not in the vocabulary

## Related Concepts
[[skill-ontology]] · [[skill-entity-linking]] · [[nil-entity-linking]] ·
[[few-shot-prompting]] · [[proficiency-levels]]

## Relevance to Iris
Granularity mismatch is real in Iris and is handled by **retrieval breadth rather than by
decomposition**. A single course description is scored against all 4,376 skills at once, so
a course covering `HTML`, `CSS` and `JavaScript` surfaces all three as candidates without
anyone deciding in advance what resolution to work at. Retrieving generously and letting
adjudication select is the simpler mechanism, and it is what the Acc@32-versus-Acc@1 gap in
[[zhang-2024-job-market-entity-linking]] recommends.

One structural note: the national vocabulary is **flat** ([[skill-ontology]]), so there is
no hierarchy to decompose *against*. Decomposition in Luyen and Abel's sense presupposes an
ontology with levels of specificity, and the standard supplies only a three-way type
distinction.

The place decomposition would earn its cost is the **input** end rather than the taxonomy
end, following [[le-2026-competency-tagging-evidence]]'s fragment segmentation. A SWU
`ชุดรายวิชา` (course module) bundles several courses under one description; splitting at
the individual-course level before linking is the analogous decision, and Iris already
takes it. Whether to split further — clause by clause within a long description — is an
open Sprint 3 question, since a 4-sentence description may develop skills that a
whole-description embedding averages away.
