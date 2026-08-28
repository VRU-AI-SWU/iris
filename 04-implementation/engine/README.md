# Iris Engine

Reads a Thai TQF (มคอ.2) document, links each course to the **national Thailand
Skill Mapping vocabulary** at an inferred proficiency level, and measures the
result against the demand that standard publishes for a career.

Runs on `gpu-linux-server`. See [`../../tech_stack.md`](../../tech_stack.md) and
[`../../implementation_plan.md`](../../implementation_plan.md).

## Quick start

```bash
uv venv --python 3.13 .venv
uv pip install -e '.[dev]'

iris snapshot -v          # report on the pinned national standard
pytest                    # 23 tests
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

## Status

**Sprint 0 complete.** Sprint 1 is the text-layer integrity gate and glyph repair.

Still open: the VRAM check on `gpu-linux-server` that selects the adjudication
and embedding models. `EXTRACTION_MODEL` and `EMBEDDING_MODEL` are deliberately
empty until then, and `/health` reports them as `null`.
