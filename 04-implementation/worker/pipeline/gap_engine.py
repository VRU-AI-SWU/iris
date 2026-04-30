"""
Gap Analysis Engine.

Implements:
  - KL divergence D_KL(market ‖ programme) — primary aggregate metric
    Direction: market‖programme penalises what graduates lack.
  - RCA (Revealed Comparative Advantage) — skill weighting by career-path specificity
  - Set decomposition: common / programme-unique / market-unique skills
  - Cosine similarity: overall alignment score
  - Heatmap data: courses × skills matrix for visualisation

Literature basis:
  - KL divergence direction: sabet-2024
  - RCA for skill weighting: ahadi-2022
  - Heatmap primary visualisation: ahadi-2022, hilliger-2022
"""
import logging
import math
from typing import Optional

import numpy as np
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

EPSILON = 1e-9  # smoothing to avoid log(0)


# ── Distribution helpers ───────────────────────────────────────────────────────

def align_distributions(
    dist_a: dict[int, float],
    dist_b: dict[int, float],
) -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Align two sparse distributions over the union of their keys.
    Returns (array_a, array_b, ordered_keys) with zero-fill for missing skills.
    """
    all_keys = sorted(set(dist_a) | set(dist_b))
    arr_a = np.array([dist_a.get(k, 0.0) for k in all_keys], dtype=np.float64)
    arr_b = np.array([dist_b.get(k, 0.0) for k in all_keys], dtype=np.float64)
    return arr_a, arr_b, all_keys


# ── Primary metrics ────────────────────────────────────────────────────────────

def kl_divergence_market_programme(
    market: dict[int, float],
    programme: dict[int, float],
) -> float:
    """
    D_KL(market ‖ programme) — asymmetric.
    High value = programme is missing skills the market demands.
    """
    m_arr, p_arr, _ = align_distributions(market, programme)

    # Add epsilon smoothing to avoid division by zero / log(0)
    m_smooth = m_arr + EPSILON
    p_smooth = p_arr + EPSILON

    # Renormalise after smoothing
    m_smooth /= m_smooth.sum()
    p_smooth /= p_smooth.sum()

    kl = float(np.sum(m_smooth * np.log(m_smooth / p_smooth)))
    return round(kl, 6)


def cosine_similarity(
    dist_a: dict[int, float],
    dist_b: dict[int, float],
) -> float:
    """Overall alignment score between two distributions (0–1)."""
    a_arr, b_arr, _ = align_distributions(dist_a, dist_b)
    norm_a = np.linalg.norm(a_arr)
    norm_b = np.linalg.norm(b_arr)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return round(float(np.dot(a_arr, b_arr) / (norm_a * norm_b)), 4)


# ── RCA (Revealed Comparative Advantage) ──────────────────────────────────────

def compute_rca(
    career_path_distribution: dict[int, float],
    all_career_path_distributions: list[dict[int, float]],
) -> dict[int, float]:
    """
    RCA for each skill in a career path distribution.

    RCA_i = (demand_i / total_demand) / (avg_demand_i_across_all_paths / avg_total_all_paths)

    RCA > 1: skill is more demanded by this career path than average → career-discriminating
    RCA < 1: skill is common across all career paths → generic

    Based on ahadi-2022 approach adapted for skill distributions.
    """
    if not all_career_path_distributions:
        return {k: 1.0 for k in career_path_distribution}

    # Average demand across all career paths
    all_keys = set(career_path_distribution.keys())
    for d in all_career_path_distributions:
        all_keys |= set(d.keys())

    avg_dist: dict[int, float] = {}
    for k in all_keys:
        avg_dist[k] = np.mean([d.get(k, 0.0) for d in all_career_path_distributions])

    avg_total = sum(avg_dist.values()) or 1.0
    target_total = sum(career_path_distribution.values()) or 1.0

    rca: dict[int, float] = {}
    for skill_id in career_path_distribution:
        target_share = career_path_distribution[skill_id] / target_total
        avg_share = avg_dist.get(skill_id, EPSILON) / avg_total
        rca[skill_id] = round(target_share / avg_share, 4)

    return rca


# ── Ranked gap table ───────────────────────────────────────────────────────────

def rank_gaps(
    market: dict[int, float],
    programme: dict[int, float],
    rca: Optional[dict[int, float]] = None,
    canonical: Optional[dict[int, str]] = None,
) -> list[dict]:
    """
    Produce a ranked list of skill gaps.

    Each entry: {
        cluster_id, label, market_weight, programme_weight,
        gap_score, rca_weight, direction
    }

    direction:
      "deficit"  — market demands it; programme underrepresents
      "surplus"  — programme has it; market rarely demands
      "aligned"  — roughly balanced

    Sorted by abs(gap_score) × rca_weight descending.
    """
    _, _, all_keys = align_distributions(market, programme)

    rows = []
    for skill_id in all_keys:
        m_weight = market.get(skill_id, 0.0)
        p_weight = programme.get(skill_id, 0.0)
        gap = m_weight - p_weight
        rca_w = (rca or {}).get(skill_id, 1.0)
        label = (canonical or {}).get(skill_id, str(skill_id))

        if gap > 0.005:
            direction = "deficit"
        elif gap < -0.005:
            direction = "surplus"
        else:
            direction = "aligned"

        rows.append({
            "cluster_id": skill_id,
            "label": label,
            "market_weight": round(m_weight, 4),
            "programme_weight": round(p_weight, 4),
            "gap_score": round(gap, 4),
            "rca_weight": round(rca_w, 4),
            "weighted_gap": round(abs(gap) * rca_w, 4),
            "direction": direction,
        })

    rows.sort(key=lambda r: r["weighted_gap"], reverse=True)
    return rows


# ── Set decomposition ──────────────────────────────────────────────────────────

def decompose_skills(
    dist_a: dict[int, float],
    dist_b: dict[int, float],
    threshold: float = 0.005,
    canonical: Optional[dict[int, str]] = None,
) -> dict:
    """
    Decompose skills into: common, a_unique, b_unique.
    A skill is considered "present" if its weight exceeds threshold.
    """
    present_a = {k for k, v in dist_a.items() if v > threshold}
    present_b = {k for k, v in dist_b.items() if v > threshold}

    common = present_a & present_b
    a_unique = present_a - present_b
    b_unique = present_b - present_a

    def to_labels(ids: set) -> list[str]:
        if canonical:
            return sorted(canonical.get(i, str(i)) for i in ids)
        return sorted(str(i) for i in ids)

    return {
        "common": to_labels(common),
        "a_unique": to_labels(a_unique),
        "b_unique": to_labels(b_unique),
        "common_count": len(common),
        "a_unique_count": len(a_unique),
        "b_unique_count": len(b_unique),
    }


# ── Heatmap data ───────────────────────────────────────────────────────────────

def build_heatmap_data(
    course_skill_sets: list,
    vocab,
    top_n_skills: int = 30,
) -> dict:
    """
    Build courses × skills matrix for heatmap visualisation.

    Returns:
      {
        skills: [label, ...],          # top-N skill labels (columns)
        courses: [                     # rows
          {name, code, category, cells: [weight, ...]},
          ...
        ]
      }
    """
    from collections import Counter

    # Find top-N skills by total weight across all courses
    all_skill_counts: Counter = Counter()
    for cs in course_skill_sets:
        weight = cs.credits * (1.0 if cs.category == "major" else 0.5)
        for skill in cs.skills:
            cluster_id = vocab.assign(skill)
            if cluster_id is not None:
                all_skill_counts[cluster_id] += weight

    top_skills = [cluster_id for cluster_id, _ in all_skill_counts.most_common(top_n_skills)]
    skill_labels = [vocab.canonical.get(sid, str(sid)) for sid in top_skills]

    # Build matrix
    courses_data = []
    for cs in course_skill_sets:
        weight = cs.credits * (1.0 if cs.category == "major" else 0.5)
        if weight == 0:
            continue

        skill_weights: Counter = Counter()
        for skill in cs.skills:
            cluster_id = vocab.assign(skill)
            if cluster_id is not None:
                skill_weights[cluster_id] += weight

        cells = [round(skill_weights.get(sid, 0.0), 4) for sid in top_skills]
        if any(c > 0 for c in cells):
            courses_data.append({
                "code": cs.course_code,
                "name": cs.course_name_en or cs.course_name_th or cs.course_code,
                "category": cs.category,
                "credits": cs.credits,
                "cells": cells,
            })

    return {"skills": skill_labels, "courses": courses_data}


# ── Market distribution builder ────────────────────────────────────────────────

def build_market_distribution(db: Session, career_path: str) -> dict[int, float]:
    """
    Aggregate job skills for a career path into a normalised distribution.
    Only considers postings within the 12-month collection window.
    """
    import os
    from datetime import datetime, timedelta
    from sqlalchemy import func
    from app.models.job import JobPosting, JobSkill

    window_months = int(os.getenv("JOB_POSTING_WINDOW_MONTHS", "12"))
    cutoff = datetime.utcnow() - timedelta(days=window_months * 30)

    rows = (
        db.query(JobSkill.cluster_id, func.count(JobSkill.id).label("cnt"))
        .join(JobPosting, JobSkill.posting_id == JobPosting.id)
        .filter(JobPosting.career_path == career_path)
        .filter(JobPosting.scraped_at >= cutoff)
        .filter(JobSkill.cluster_id.isnot(None))
        .group_by(JobSkill.cluster_id)
        .all()
    )

    raw = {r.cluster_id: float(r.cnt) for r in rows}
    total = sum(raw.values()) or 1.0
    return {k: v / total for k, v in raw.items()}
