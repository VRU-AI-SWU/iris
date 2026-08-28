# Literature Review Methodology — VRU-AI Standard

> Canonical instructions for building and maintaining a project's
> `02-literature-review/`. This is the lab-wide standard; each project copies
> this file into its own `02-literature-review/.claude/instruction.md` and may
> append a short project-specific section at the end. Do not fork the
> methodology per project — only the domain-specific additions differ.

---

## 1. Philosophy

A literature review is maintained as an **LLM-authored knowledge wiki** in
Obsidian-compatible Markdown. It is a knowledge *graph*, not a flat list: every
paper links to the concepts it discusses and the research questions it answers,
so the corpus stays navigable as it grows. The wiki is the single source of
truth that downstream phases (`03-solution-design/`, `05-reports/`) cite.

Two products come out of the same corpus:
- a **structured, queryable** layer (`papers/`, `concepts/`, `questions/`) for
  precise lookup and design-decision tracing, and
- a **narrative** layer (`literature_review/`) — continuous academic prose with
  inline citations, suitable for a paper's Background / Related Work section.

---

## 2. Folder Structure

```
02-literature-review/
├── .claude/
│   └── instruction.md          # this methodology (copied from the lab template)
├── raw/                        # original source PDFs + manifest.md
│   ├── manifest.md             # one row per paper note → PDF presence / provenance
│   └── *.pdf                   # the original papers
└── wiki/                       # all generated output
    ├── index.md                # table of contents + query entry point
    ├── papers/                 # one note per paper
    ├── concepts/               # semantic concept nodes (Obsidian graph)
    ├── questions/              # research-question synthesis notes
    └── literature_review/      # narrative academic review with citations
```

Folder names may vary per project only if a strong reason exists; the
**five wiki components and the three root subfolders are mandatory**.

---

## 3. `raw/` — Source Corpus

- `raw/` holds the original papers (mostly PDFs). Every paper that has a note in
  `wiki/papers/` should have its source archived here when obtainable.
- `raw/manifest.md` is the provenance ledger: one row per `wiki/papers/` note,
  recording the matching PDF filename (or **missing — to source** when the PDF
  is not yet archived) plus DOI/URL. Update it whenever a paper is added.
- Clinical-standard or institutional reference documents (e.g. a scoring
  guideline) are **not** review papers — keep those in the project's `domain/`,
  not in `raw/`.

---

## 4. `wiki/index.md` — Entry Point

The starting point for any query against the wiki. Contains:
- a one-paragraph scope statement,
- a **Papers** table grouped by theme: `File | Authors | Year | Venue | Relevance | One-line summary`,
- a **Questions** table: `File | Status | One-line answer`,
- a **Concepts** table: `File | One-line summary`,
- a link to `literature_review/` (the narrative synthesis),
- a short **Key Cross-Cutting Findings** section distilling the corpus into the
  decisions that feed Solution Design.

Keep it current: every new paper, concept, or question gets a row here.

---

## 5. `wiki/papers/` — Per-Paper Notes

One file per paper, named `{firstauthor}-{year}-{short-slug}.md` (kebab-case).

Frontmatter:
```yaml
---
type: paper
authors: [Lastname F., ...]
year: 2023
title: "Exact paper title"
venue: Journal or Conference
doi: 10.xxxx/xxxxx
relevance: high | medium | low      # to THIS project
questions: [q-slug, q-slug]         # questions this paper informs
---
```

Body sections (omit a heading only if genuinely not applicable):
1. **Research Question** — what the paper sets out to answer.
2. **Limitations of Existing Methods** — the gap it addresses.
3. **Contribution** — what is new.
4. **Proposed Method** — dataset, approach, key parameters.
5. **Key Findings** — results, with concrete numbers (use tables for metrics).
6. **Limitations of This Paper** — caveats relevant to reusing its findings.
7. **Concepts** — `[[concept-slug]]` links to every concept node it discusses.
8. **Questions Addressed** — `[[q-slug]]` links.
9. **Notes for the Project** — how the findings apply to *this* project's design.

Record concrete numbers (n, AUC, DSC, parameters), not vague claims — these
notes are cited verbatim in Solution Design.

---

## 6. `wiki/concepts/` — Concept Nodes

Semantic nodes that define domain terms and connect the graph. One file per
concept, `{concept-slug}.md`.

Frontmatter: `type: concept`. Body:
- **Definition** — concise, authoritative.
- **Papers That Discuss This** — `[[paper-slug]]` backlinks.
- **Related Concepts** — `[[concept-slug]]` links.
- **Relevance to the Project** — why it matters here.

**Maintenance rule:** when a new paper introduces or leans on a concept that has
no node yet, create the node; if the concept exists, add the paper to its
backlinks. Concepts are updated as part of adding a paper, never left stale.

---

## 7. `wiki/questions/` — Research-Question Synthesis

The bridge from literature to design decisions. Each note tracks one open
research question that the review must resolve. One file per question,
`q-{slug}.md`.

Frontmatter:
```yaml
---
type: question
owner: [Role, ...]            # lab role(s) responsible
status: open | resolved
---
```

Body:
- **Question** — the precise question.
- **Why This Matters** — the decision that hinges on it.
- **Initial Hypothesis** — the prior, before reading.
- **Papers Addressing This** — `[[paper-slug]]` links, each with the one finding
  that bears on the question.
- **Current Working Answer** — the synthesized answer; the locked decision once
  `status: resolved`.
- **Remaining Uncertainty** — what is still open (empty/"none" when resolved).

Questions are the decision log of the review. When all are `resolved`, the phase
is ready to feed Solution Design.

---

## 8. `wiki/literature_review/` — Narrative Review

A continuous academic-prose synthesis of the whole corpus, with **inline
citations** in `(Author Year)` form, **each rendered as a Markdown link to its
`papers/` note** so every claim points the reader to its supporting evidence.
Organized thematically (typically mirroring the project's pipeline stages or
research questions), not paper-by-paper. This is the artifact that becomes a
publication's Background / Related Work section.

It **ends with a `## References` section** — an author-date list of every cited
paper (authors, year, title, venue, DOI), each entry linked back to its
`papers/` note — so the inline `(Author Year)` markers resolve to full
bibliographic entries. A narrative without a reference list is incomplete.

**Regeneration rule:** the narrative is kept in sync with the corpus. When a
paper is added (or a question resolved), update the relevant narrative
subsection *and* add its entry to the References list — the narrative is never
allowed to fall behind `papers/`.

---

## 9. Workflow — Adding a Paper

1. Place the PDF in `raw/` and add or update its row in `raw/manifest.md`.
2. Create `wiki/papers/{firstauthor}-{year}-{slug}.md` from the §5 template.
3. Create or update the `wiki/concepts/` nodes it touches (§6).
4. Link it into every relevant `wiki/questions/` note and update the working
   answer if the evidence shifts (§7).
5. Update the matching subsection of `wiki/literature_review/` (§8).
6. Add rows to `wiki/index.md` (papers / concepts / questions tables) (§4).

Adding a paper is not done until all six steps are complete — that is what keeps
the graph consistent.

---

## 10. Conventions

- **Filenames** kebab-case; paper slugs `{firstauthor}-{year}-{topic}`.
- **Links** use Obsidian `[[slug]]` (no `.md`) for intra-wiki graph edges;
  use relative Markdown links in `index.md` tables for clickability.
- **Citations** in the narrative use `(Author Year)`, each hyperlinked to its
  `papers/` note; the note is the authoritative source of the exact reference.
- **Numbers over adjectives** — always prefer the reported metric to a vague
  qualifier.

---

## 11. Project-Specific Additions (Iris — Curriculum Skill Alignment)

These extend — do not replace — the lab standard above.
*Rewritten 2026-08-28 after the pivot to the national skill standard.*

- **Map every paper to the research questions.** Iris's review is organised around the
  questions in `wiki/questions/` (currently 16, listed in the ingestion prompt below). Each
  paper note's `questions:` frontmatter and *Questions Addressed* section must link the
  `q-*` notes it informs; the narrative is structured by these questions.
- **Thai-context tagging.** Note whether a paper's evidence is Thai-specific or imported
  from another labour market or language. The Thai subset is the project's distinctive
  contribution and its scarcest evidence.
- **Decision discipline.** A `q-*` note reaches `status: answered` only when the literature
  settles it; questions deferred to Phase 4 empirical validation stay `open` with the
  deferral noted. If a new paper changes a working answer, update the question note *and*
  the narrative section.
- **Superseded questions are retained, not deleted.** When the project's direction changes,
  mark the affected `q-*` note `closed` / `superseded` / `revised` with a banner explaining
  why, and keep the original reasoning below it. The decision log is only useful if it
  records decisions that were later reversed.
- **Search beyond journals for infrastructure questions.** ⚠️ The April 2026 round
  concluded "no Thai skill ontology exists" and missed a สป.อว. open-data standard that had
  been public for nine months, because the standard has no accompanying paper. For any
  question of the form *does this dataset / ontology / registry / API exist?*, search
  ministry sites, government open-data portals, and platform documentation directly — a
  literature search is structurally incapable of answering it.
- **Record concrete performance numbers.** Where a paper reports accuracy, F1, Acc@k or
  agreement, the note carries the figure and the conditions it was measured under. These
  are what calibrate the project's own evaluation targets, and vague summaries cannot.

### LLM Ingestion Prompt

Copy everything in the block below, append the paper text, and send to the LLM; it fills
the `papers/` note template (§5). Keep each section to 3–5 sentences.

```
You are a research assistant helping with a project called IRIS. IRIS expresses a Thai
university curriculum in the vocabulary of the national Thailand Skill Mapping standard
(สป.อว. / KMITL): it reads a TQF (มคอ.2) document, links each course to the 4,376-skill
national vocabulary at a stated proficiency level, and compares the resulting programme
profile against the skill demand that standard publishes for each career.

We are conducting a literature review to answer these open research questions:

LIVE
Q1  [q-skill-taxonomy]      What controlled vocabulary should we link to, and what does
                            adopting a fixed national standard cost us?
Q2  [q-thai-ontology]       Does a Thai skill vocabulary exist at the granularity we need?
                            (ANSWERED — yes, since July 2025)
Q3  [q-level-inference]     How do we infer a proficiency level for a course-skill link
                            from a TQF document, and how reliable is each signal?
Q4  [q-out-of-vocabulary]   What happens to skills a course develops that the national
                            vocabulary does not contain?
Q5  [q-prevalence-metrics]  Which alignment metrics are valid on prevalence data that is
                            truncated at ~100 skills per career?
Q6  [q-implied-skills]      How well can we link skills a course develops without naming
                            them? (recall in skill entity linking)
Q7  [q-thai-nlp]            How do we process Thai curriculum text — including detecting
                            and repairing corrupted PDF text layers?
Q8  [q-gap-direction]       Should the gap be symmetric or directional?
Q9  [q-temporal-drift]      How do we use the standard's per-skill growth rates?
Q10 [q-visualisation]       What output format is actionable for a curriculum committee?
Q11 [q-credit-weighting]    Should course credit hours weight the skill contribution?

CLOSED BY THE PIVOT — do not link papers to these
Q12 [q-job-posting-sources] · Q13 [q-sample-size] · Q14 [q-segment-taxonomy]
Q15 [q-segment-inference]   · Q16 [q-registry-lookup]

Read the paper below and fill in the papers/ note template exactly.
- For "Concepts", suggest 2–5 lowercase-hyphenated slugs (e.g. [[skill-entity-linking]]).
- For "Questions Addressed", list only slugs for questions this paper addresses.
- ALWAYS record concrete reported numbers (accuracy, F1, Acc@k, dataset size, agreement)
  and the conditions they were measured under. Numbers over adjectives.
- In "Notes for the Project", say what the paper changes about Iris's design — including
  when it changes nothing, and when it rules an approach out.
- Keep each section concise — 3 to 5 sentences maximum.

[PASTE PAPER TEXT HERE]
```

### Obsidian Graph Tips

- Tag questions `#question`, papers `#paper`, concepts `#concept`; colour them differently
  in Graph View.
- An isolated question node (no paper links) is a genuine research gap — prioritise it.
  Three such gaps are currently confirmed and are contributions rather than oversights:
  NLP on Thai TQF documents, PDF text-layer corruption in Thai, and grading curriculum
  skill depth against a published competency scale.
- A concept linked by many papers is well-established and safe to rely on in Solution
  Design.
