# Iris Engine

<!-- lang-switch -->
**English** · [ภาษาไทย](README.th.md)

Reads a Thai TQF (มคอ.2) document, links each course to the **national Thailand
Skill Mapping vocabulary** at an inferred proficiency level, and measures the
result against the demand that standard publishes for a career.

Runs on `gpu-linux-server`. See [`../../tech_stack.md`](../../tech_stack.md) and
[`../../implementation_plan.md`](../../implementation_plan.md).

## Quick start

```bash
uv venv --python 3.13 .venv
uv pip install -e '.[dev]'

iris snapshot -v            # report on the pinned national standard
iris check <มคอ.2.pdf> -v   # Thai text-layer integrity gate + glyph repair
iris courses <มคอ.2.pdf>    # provenance-carrying course list
iris link <มคอ.2.pdf> -v    # course → skill links with verified evidence
pytest                      # 134 tests
uvicorn iris.api.main:app --reload
curl localhost:8000/health
```

## Layout

```
iris/
├── config.py          settings; defaults run with no environment set up
├── snapshot/          the pinned national standard, read-only
│   ├── models.py      Skill · Career · SkillDemand · SeniorityPair
│   └── loader.py      loading + the design's data-quality filters
├── ingest/            the text-layer integrity gate and course extraction
│   ├── integrity.py   Thai combining-mark diagnostic → clean/repairable/lossy/unusable
│   ├── repair.py      learns the substitution table *from the document*
│   ├── normalise.py   reverses structural sara-am breaks; no learned table needed
│   ├── pdf.py         per-character text with font attribution, repair applied
│   ├── courses.py     anchors on the credit spec; learns each document's code shape
│   ├── curriculum_map.py  reads ● ○ positionally, classified by rendered ink
│   └── clo.py         per-course learning outcomes and their cognitive-demand verbs
├── link/              retrieval and adjudication
│   ├── retrieval.py   BM25 over three surface forms + a consonant-skeleton channel
│   ├── provider.py    one provider-blind interface; quota exhaustion is not a retry
│   ├── adjudicate.py  constrained selection; evidence spans verified against the text
│   └── pipeline.py    a whole programme, one pinned provider
├── db/                SQLAlchemy schema and sessions
├── api/               FastAPI; /health only until Sprint 9
└── cli.py             `iris …` — how the pipeline is driven through Sprint 7
```

## Two decisions worth knowing

**SQLite in development, PostgreSQL in production.** Every model uses generic
SQLAlchemy types, so the same schema runs on both. Sprints 1–7 are ingestion and
evaluation work that should not require a database server; `DATABASE_URL` points
at PostgreSQL on the deployment host.

**The snapshot is read-only reference data, never the live API.** An analysis
records which snapshot it used. `iris snapshot` prints that provenance, and
`/health` returns it — an engine that cannot read its reference data is not ready.

## What the loader enforces

Data-quality rules from the solution design are applied on load and reported,
never silently:

- career × skill entries with `count = 0` are dropped — **168** in the current
  snapshot, including Python and Pandas for วิศวกรข้อมูล
- careers with fewer than 10 skills are degenerate and excluded — **3**
- seniority ladders are built only where both rungs survive those filters —
  13 pairs exist in the raw data, **12** are analysable

`tests/test_snapshot.py` asserts these figures against
[`data-feasibility.md`](../../03-solution-design/data-feasibility.md), so a
re-fetch that changes the upstream data fails loudly rather than shifting an
analysis under a published number.

## The integrity gate

Thai text from institutional PDFs is often corrupted in ways nothing raises an
error about. `iris check` classifies a document before anything downstream
touches it:

| Verdict | Meaning | Action |
|---|---|---|
| `clean` | mark rate near baseline, few intrusions | use the text layer |
| `repairable` | ASCII glyphs substituted for marks inside Thai words | learn a table, repair, re-run the gate |
| `lossy` | information gone (e.g. every `ำ` collapsed to `า`) | re-extract with a vision model, flag as vision-derived |
| `unusable` | too little Thai to judge | reject; ask for a better file |

**The repair table is learned from the document, not hard-coded** — a table from
one file would not transfer to another producer's output. A substituted glyph is
whichever combining mark turns the word it sits in into a real Thai word, with
the longest match winning and votes aggregated per `(font, glyph)`.

Measured on the two real documents:

```
CMU  148p  MS Word 2016        lossy → normalise → CLEAN 188.0
KU    28p  MS Word 2013        lossy → normalise → CLEAN 171.0
PSU  229p  macOS Quartz        repairable → 83%, 38 rules → CLEAN 175.7
SU   254p  Adobe Acrobat Pro   repairable → 96%, 14 rules → CLEAN 173.8
SWU  216p  Bullzip PDF Printer repairable → 92%, 13 rules → CLEAN 162.9
```

Against a clean-document baseline of 171.0 marks per 1,000 Thai characters. Three
unrelated damage alphabets across five producers, with no overlap between the learned
tables — and **every document reaches a usable text layer without a vision model**, which
takes the GPU off the ingestion path entirely.

## Status

**Sprints 0–3 complete and measured.** `iris link` runs a whole programme end to end.

Lexical retrieval measures **recall@10 75 %, @50 83 %** on a 6-course development set,
which fixes `k = 30`. Adjudication runs on `iris-adjudicator` (`qwen3:8b` at `num_ctx 8192`)
holding 6.6 GB, about 4.2 s per course.

⚠️ **No precision figure may be quoted yet.** Scoring against the development set gave 23 %,
and reading the source text showed the model right where the labels were narrow. Precision
waits for the Sprint 4 gate: two annotators, multiple correct links permitted, labels fixed
before any model output is seen.

Still open: the dense half of retrieval, the bilingual channel, and `EMBEDDING_MODEL` —
all of which land with the Sprint 4 ablations.
