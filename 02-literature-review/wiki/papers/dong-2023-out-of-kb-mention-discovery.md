---
type: paper
authors: [Dong H., Chen J., He Y., Liu Y., Horrocks I.]
year: 2023
title: "Reveal the Unknown: Out-of-Knowledge-Base Mention Discovery with Entity Linking"
venue: CIKM 2023
doi: 10.1145/3583780.3615036
relevance: high
questions: [q-out-of-vocabulary, q-skill-taxonomy]
---

<!-- lang-switch -->
**English** · [ภาษาไทย](dong-2023-out-of-kb-mention-discovery.th.md)

## Research Question
How can an entity-linking system recognise that a mention has **no corresponding entry**
in the knowledge base, instead of forcing it onto the nearest available entity?

## Limitations of Existing Methods
Out-of-KB (NIL) detection was handled "mostly by the simple threshold-based approach and
feature-based classification" — a similarity cut-off, tuned by hand. Evaluation datasets
for the problem were "relatively rare", so the failure mode was under-studied despite
being ubiquitous.

## Contribution
**BLINKout**: a BERT-based entity linker that models out-of-KB status explicitly by
matching such mentions to a dedicated NIL entity, plus a method for *generating* out-of-KB
evaluation data from ordinary in-KB datasets.

## Proposed Method
- **NIL entity representation and classification** — the NIL case is a first-class target
  the model can select, not a residue below a threshold
- **Synonym enhancement** to strengthen in-KB representations, so genuine matches are less
  likely to be pushed into NIL
- **KB Pruning and Versioning** — remove entities from a KB, or use two KB versions across
  time, to synthesise out-of-KB mentions automatically and cheaply
- **Evaluation:** five datasets over clinical notes, biomedical publications and
  Wikipedia, against UMLS, SNOMED CT and WikiData

## Key Findings
- BLINKout outperformed threshold-based and feature-based NIL handling across all five
  datasets and three knowledge bases
- Treating NIL as an explicit prediction target beats post-hoc thresholding
- KB Versioning produces realistic out-of-KB cases without new annotation, since entities
  genuinely absent from an older KB version are known to be absent

## Limitations of This Paper
Evaluated on biomedical and encyclopedic KBs, not occupational or educational ones.
Synthetic out-of-KB mentions from KB pruning may be easier than naturally occurring ones,
since pruned entities were by construction well-formed KB entries.

## Concepts
[[skill-entity-linking]] · [[thailand-skill-mapping]] · [[esco-ontology]]

## Questions Addressed
[[q-out-of-vocabulary]] · [[q-skill-taxonomy]]

## Notes for the Project
This paper supplies the **name, the method, and the evaluation trick** for the problem
[[q-out-of-vocabulary]] raises. Iris adopts a fixed 4,376-entry vocabulary derived from
labour-market data, and a university curriculum contains material no job advertisement
describes — theoretical foundations, research method, mathematics, ethics. Those are
out-of-KB mentions in exactly this sense.

Three things transfer:

1. **Make out-of-vocabulary an explicit decision, not a threshold.** The design already
   leans this way; BLINKout shows that an explicit NIL target measurably beats a
   similarity cut-off, which settles the implementation question and rules out option 3
   ("map to nearest in-vocabulary skill") in [[q-out-of-vocabulary]] on evidence rather
   than on principle.
2. **Synonym enhancement is directly available.** The national standard ships Thai and
   English titles plus a Thai definition for every skill — three surface forms per entry,
   free — which is precisely the enhancement BLINKout had to construct.
3. **KB Versioning gives Iris a cheap evaluation set.** Holding out a random subset of the
   4,376 skills and checking that the linker declines to link courses that develop them
   produces out-of-vocabulary test cases with no extra annotation. Worth adding to the
   Sprint 4 gate.

The out-of-vocabulary residue is also a *deliverable*: accumulated across programmes it
becomes a coverage report back to สป.อว./KMITL on what the standard does not yet name.
