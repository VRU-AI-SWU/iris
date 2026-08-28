"""API tests."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from iris.api.main import app


@pytest.fixture(scope="module")
def client():
    return TestClient(app)


def test_health_reports_ok(client):
    body = client.get("/health").json()
    assert body["status"] == "ok"


def test_health_proves_the_snapshot_loaded(client):
    """An engine that cannot read its reference data is not ready."""
    snap = client.get("/health").json()["snapshot"]
    assert snap["snapshot_date"] == "2026-08-27"
    assert snap["skills_total"] == 4376
    assert snap["seniority_pairs"] == 12


def test_health_reports_the_filters_it_applied(client):
    """Data-quality filtering is disclosed, never silent."""
    snap = client.get("/health").json()["snapshot"]
    assert snap["demand_pairs_dropped_zero_count"] == 168
    assert snap["careers_degenerate"] == 3


def test_health_reports_database_reachability(client):
    assert client.get("/health").json()["database"]["reachable"] is True


def test_model_selection_is_still_pending(client):
    """Sprint 0 leaves these empty; a VRAM check on gpu-linux-server decides them."""
    models = client.get("/health").json()["models"]
    assert models["extraction"] is None
    assert models["embedding"] is None
