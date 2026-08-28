"""FastAPI application.

Sprint 0 exposes only readiness. The analysis endpoints arrive in Sprint 9, when
there is something for them to serve; until then the pipeline is driven from the
CLI, which is what the evaluation gate needs.
"""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from fastapi import FastAPI
from sqlalchemy import text

from iris import __version__
from iris.config import get_settings
from iris.db import get_engine
from iris.snapshot import get_snapshot

app = FastAPI(
    title="Iris Engine",
    version=__version__,
    description="Curriculum skill alignment against the Thailand Skill Mapping standard",
)


def _database_status() -> dict[str, Any]:
    try:
        with get_engine().connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"reachable": True}
    except Exception as exc:  # pragma: no cover - exercised only on a broken DB
        return {"reachable": False, "error": type(exc).__name__}


@app.get("/health")
def health() -> dict[str, Any]:
    """Readiness, not liveness.

    Reports whether the pinned snapshot loads and what it contains, because an
    engine that cannot read its reference data cannot do anything useful — and
    the load report is the same provenance every analysis records.
    """
    settings = get_settings()
    snapshot = get_snapshot()
    return {
        "status": "ok",
        "version": __version__,
        "snapshot": {
            "path": str(settings.skillmap_snapshot),
            **asdict(snapshot.report),
        },
        "database": _database_status(),
        "models": {
            "server": settings.model_server_url,
            "extraction": settings.extraction_model or None,
            "embedding": settings.embedding_model or None,
        },
    }
