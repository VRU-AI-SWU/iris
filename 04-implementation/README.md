# 04 — Implementation

Two deployables. See [`../tech_stack.md`](../tech_stack.md) for the full stack and
[`../implementation_plan.md`](../implementation_plan.md) for the sprint order.

```
engine/    Python — ingestion, skill linking, alignment, FastAPI
           runs on gpu-linux-server (department office, 24/7)

web/       Astro — public results site + gated analysis app
           deploys to Cloudflare Workers at vru-ai.com/iris
```

The engine **publishes** versioned result documents; the web tier only reads published
results. Nothing on the public site touches the engine at request time.

## Status

Sprint 0 — ground clearing. The previous implementation (Rust/Axum backend, Python
Celery backend, HDBSCAN sidecar, job-board scrapers, Next.js scaffold) was removed on
2026-08-27: it was built around scraping job boards and clustering an emergent skill
vocabulary, and the pivot to the national Skill Mapping standard deleted both. See
[`../03-solution-design/solution-proposal.md`](../03-solution-design/solution-proposal.md).

`engine/` and `web/` are created in Sprint 0.
