"""Engine configuration.

Everything the engine needs to locate its inputs and its database. Defaults are
chosen so the pipeline runs with no environment set up at all — which matters for
Sprints 1–7, where the work is ingestion and evaluation rather than serving.
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _repo_root() -> Path:
    """Walk up until the directory holding `data/skillmapping` is found."""
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "data" / "skillmapping").is_dir():
            return parent
    # Installed outside the repo: fall back to the working directory.
    return Path.cwd()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    # ── National standard snapshot (pinned; never the live API) ──────────────
    skillmap_snapshot: Path = _repo_root() / "data" / "skillmapping" / "2026-08-27"

    # ── Database ────────────────────────────────────────────────────────────
    # SQLite by default so ingestion and evaluation need no database server.
    # Production on linux-gpu-server sets DATABASE_URL to PostgreSQL.
    database_url: str = f"sqlite:///{_repo_root() / 'data' / 'iris.db'}"

    # ── Model server (OpenAI-compatible); unused until Sprint 3 ─────────────
    model_server_url: str = "http://localhost:1234/v1"
    extraction_model: str = ""
    embedding_model: str = ""

    debug: bool = True

    @property
    def snapshot_date(self) -> str:
        """The snapshot directory name — recorded with every analysis."""
        return self.skillmap_snapshot.name


@lru_cache
def get_settings() -> Settings:
    return Settings()
