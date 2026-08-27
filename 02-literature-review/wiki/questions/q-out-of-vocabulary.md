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

## Current Working Answer
status: open

Leaning to **option 2 with option 4 as a by-product**: record out-of-vocabulary skills,
report them separately, never let them enter a score, and let the accumulated residue
inform a coverage report back to the standard's maintainers. Option 3 is rejected —
mapping to a near neighbour would contaminate the alignment metric with fabricated matches.

## Remaining Uncertainty
- What proportion of a Thai CS curriculum falls outside the vocabulary? *(measurable in
  Sprint 3 — a headline number for the paper)*
- Is the residue concentrated in general education, or does it reach into major courses?
- Does the standard's digital industry cover academic CS adequately, or is it oriented
  towards industry job roles?
