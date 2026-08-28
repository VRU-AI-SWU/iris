---
type: question
owner: Researcher + Domain Expert
status: open
---

## Question
What should happen to skills a course clearly develops that the **national vocabulary
does not contain**?

## Why This Matters for Iris
Adopting a fixed controlled vocabulary buys reproducibility and comparability, and pays
for it in coverage. The standard's 4,376 skills were derived from labour-market data for
five industries; a university curriculum contains material that no job advertisement
describes — theoretical foundations, research method, mathematics, ethics, and
locally-specific content.

If those are silently dropped, Iris systematically under-represents exactly the parts of
a curriculum that distinguish a degree from vocational training — and a curriculum
committee will notice immediately, and reasonably distrust the whole report.

## Options
1. **Discard** — clean vocabulary, but a biased picture of the programme
2. **Record as out-of-vocabulary**, reported separately and never scored — honest, and
   the residue is itself evidence about the standard's coverage
3. **Map to the nearest in-vocabulary skill** — keeps everything scoreable, but
   fabricates precision and corrupts the comparison
4. **Propose additions upstream** — the accumulated residue becomes feedback to
   สป.อว./KMITL, which is a contribution in its own right

## Papers Addressing This
- [[dixon-2023-occupational-models-42m]] — a bounded 775-skill vocabulary sufficed at US
  national scale, suggesting fixed vocabularies can have adequate coverage for
  *labour-market* description; a curriculum is a different distribution
- [[senger-2024-dl-skill-extraction-survey]] — fixed-taxonomy approaches consistently miss
  emerging and domain-specific skills; a recognised, unsolved limitation
- [[sabet-2024-course-skill-atlas]] — uses fixed O*NET DWAs on syllabi and notes the same
  limitation; the closest precedent for the curriculum side specifically
- [[luyen-2025-skill-decomposition-ontology]] — decomposition can bridge granularity
  mismatch, but not genuine absence
- **[[dong-2023-out-of-kb-mention-discovery]]** — ⭐ **added 2026-08-28.** BLINKout models
  out-of-KB status as an explicit NIL prediction target and beats threshold- and
  feature-based methods across five datasets and three knowledge bases. Also contributes
  *KB Pruning and Versioning* — synthesising out-of-KB evaluation cases from an ordinary
  in-KB dataset, with no new annotation
- [[zhang-2024-job-market-entity-linking]] — evaluates against a single gold ESCO title per
  mention and notes this underestimates performance where several links are valid; the same
  scoring trap applies to Iris's annotation protocol

## Current Working Answer
status: open — *method settled 2026-08-28, magnitude still empirical*

**Option 2, with option 4 as a by-product**, and the *how* is now settled on evidence
rather than principle.

[[dong-2023-out-of-kb-mention-discovery]] shows that treating out-of-vocabulary as an
**explicit prediction target** measurably beats the similarity-threshold approach that
would otherwise have been the default implementation. Option 3 (map to the nearest
in-vocabulary skill) is rejected outright: it fabricates matches and, in a curriculum
setting, would map *"ทฤษฎีการคำนวณ"* to whatever labour-market skill sits closest —
confidently and wrongly. See [[nil-entity-linking]].

Two techniques transfer directly and are adopted:

1. **Synonym enhancement** — BLINKout had to construct alternative surface forms; the
   national standard ships three per skill for free (Thai title, English title, Thai
   definition).
2. **KB Versioning as a cheap evaluation set** — hold out a random subset of the 4,376
   skills and check the linker declines to link courses that develop them. This produces
   out-of-vocabulary test cases with no extra annotation, and is added to the Sprint 4 gate.

## Remaining Uncertainty
- What proportion of a Thai CS curriculum falls outside the vocabulary? *(measurable in
  Sprint 3 — a headline number for the paper)*
- Is the residue concentrated in general education, or does it reach into major courses?
- Does the standard's digital industry cover academic CS adequately, or is it oriented
  towards industry job roles?
