# 04 — Implementation

<!-- lang-switch -->
**English** · [ภาษาไทย](README.th.md)

Two deployables. See [`../tech_stack.md`](../tech_stack.md) for the full stack and
[`../implementation_plan.md`](../implementation_plan.md) for the sprint order.

```
engine/      Python — ingestion, skill linking, alignment, FastAPI
             runs on gpu-linux-server (department office, 24/7)

annotation/  the annotator guideline for the Sprint 4 evaluation gate

web/         Astro — public results site + gated analysis app
             deploys to Cloudflare Workers at vru-ai.com/iris
```

The engine **publishes** versioned result documents; the web tier only reads published
results. Nothing on the public site touches the engine at request time.

## Status

**Sprints 1–3 built and measured.** `iris link <programme>` runs end to end: ingestion
across five PDF producers with no GPU, lexical retrieval at recall@10 75 %, and
adjudication on `iris-adjudicator` at 6.6 GB. Sprint 4 — the evaluation gate — is next,
and blocks everything after it.

The previous implementation (Rust/Axum backend, Python Celery backend, HDBSCAN sidecar,
job-board scrapers, Next.js scaffold) was removed on 2026-08-27: it was built around
scraping job boards and clustering an emergent skill vocabulary, and the pivot to the
national Skill Mapping standard deleted both. See
[`../03-solution-design/solution-proposal.md`](../03-solution-design/solution-proposal.md).

`web/` is created in Sprint 8.
