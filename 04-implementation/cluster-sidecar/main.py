"""
HDBSCAN Cluster Sidecar
-----------------------
Accepts skill embeddings from the Rust worker and returns cluster labels.
Kept as a Python microservice because no production-ready HDBSCAN crate
exists for Rust as of 2026-05.

Endpoints:
  GET  /health       — liveness probe
  POST /cluster      — run HDBSCAN on provided embeddings
"""

from __future__ import annotations

import logging
from typing import List

import hdbscan
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("cluster-sidecar")

app = FastAPI(title="Iris Cluster Sidecar", version="0.1.0")


# ── Request / response models ─────────────────────────────────────────────────

class ClusterRequest(BaseModel):
    embeddings: List[List[float]] = Field(..., description="Embedding vectors (N × D)")
    min_cluster_size: int = Field(5, ge=2, description="HDBSCAN min_cluster_size")
    min_samples: int = Field(3, ge=1, description="HDBSCAN min_samples")


class ClusterResponse(BaseModel):
    labels: List[int] = Field(..., description="Cluster label per embedding (-1 = noise)")
    n_clusters: int = Field(..., description="Number of clusters found (excluding noise)")
    noise_fraction: float = Field(..., description="Fraction of points labelled as noise")


# ── Endpoints ─────────────────────────────────────────────────────────────────

@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/cluster", response_model=ClusterResponse)
def cluster(req: ClusterRequest) -> ClusterResponse:
    if len(req.embeddings) == 0:
        raise HTTPException(status_code=422, detail="embeddings must not be empty")

    X = np.array(req.embeddings, dtype=np.float32)
    if X.ndim != 2:
        raise HTTPException(status_code=422, detail="embeddings must be a 2-D array")

    n_points = X.shape[0]

    # HDBSCAN needs at least min_cluster_size points
    effective_min = min(req.min_cluster_size, max(2, n_points // 2))

    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=effective_min,
        min_samples=min(req.min_samples, effective_min),
        metric="euclidean",
        cluster_selection_method="eom",
    )
    labels = clusterer.fit_predict(X).tolist()

    n_clusters = len(set(l for l in labels if l >= 0))
    noise_count = labels.count(-1)
    noise_fraction = noise_count / n_points if n_points > 0 else 0.0

    log.info(
        "clustered %d points → %d clusters, %.1f%% noise",
        n_points,
        n_clusters,
        noise_fraction * 100,
    )

    return ClusterResponse(
        labels=labels,
        n_clusters=n_clusters,
        noise_fraction=noise_fraction,
    )
