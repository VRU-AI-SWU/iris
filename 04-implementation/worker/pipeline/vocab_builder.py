"""
Emergent skill vocabulary builder.

Clusters raw extracted skill terms using HDBSCAN on their embeddings.
Each cluster becomes one canonical skill label in the shared vocabulary.

Design decisions (from literature review):
- No fixed taxonomy imposed at this stage
- Bottom-up: vocabulary emerges from actual documents
- Optional post-hoc ESCO mapping (not implemented in v1)
"""
import json
import logging
from collections import defaultdict, Counter

import numpy as np
from hdbscan import HDBSCAN
from sklearn.preprocessing import normalize

from pipeline.skill_embedder import embed_skills

logger = logging.getLogger(__name__)


class VocabularyBuilder:
    def __init__(self, min_cluster_size: int = 3, min_samples: int = 1):
        self.min_cluster_size = min_cluster_size
        self.min_samples = min_samples
        self._clusterer: HDBSCAN | None = None
        self.cluster_labels: np.ndarray | None = None
        self.skill_terms: list[str] = []
        self.embeddings: np.ndarray | None = None
        # cluster_id → canonical label
        self.canonical: dict[int, str] = {}

    def fit(self, skill_terms: list[str]) -> dict[int, str]:
        """
        Fit vocabulary from a list of raw skill terms.
        Returns mapping of cluster_id → canonical label.
        """
        if not skill_terms:
            return {}

        # Deduplicate while preserving order
        unique_terms = list(dict.fromkeys(t.strip().lower() for t in skill_terms if t.strip()))
        logger.info("Building vocabulary from %d unique skill terms", len(unique_terms))

        embeddings = embed_skills(unique_terms)
        if embeddings.shape[0] == 0:
            logger.error("Embedding returned empty array")
            return {}

        # L2-normalise before clustering (cosine distance becomes euclidean distance)
        normed = normalize(embeddings, norm="l2")

        self._clusterer = HDBSCAN(
            min_cluster_size=self.min_cluster_size,
            min_samples=self.min_samples,
            metric="euclidean",
            cluster_selection_method="eom",
        )
        labels = self._clusterer.fit_predict(normed)

        self.skill_terms = unique_terms
        self.embeddings = embeddings
        self.cluster_labels = labels

        # Determine canonical label for each cluster: most frequent term in cluster
        cluster_terms: dict[int, list[str]] = defaultdict(list)
        for term, label in zip(unique_terms, labels):
            if label >= 0:  # -1 = noise (unclustered)
                cluster_terms[label].append(term)

        self.canonical = {}
        for cluster_id, terms in cluster_terms.items():
            # Pick the shortest term as canonical (tends to be the most generic)
            self.canonical[cluster_id] = min(terms, key=len)

        noise_count = int(np.sum(labels == -1))
        logger.info(
            "Vocabulary: %d clusters, %d noise points (unclustered)",
            len(self.canonical), noise_count,
        )
        return self.canonical

    def assign(self, skill_term: str) -> int | None:
        """
        Assign a raw skill term to a cluster ID.
        Returns None if the term cannot be assigned (noise or vocabulary not fitted).
        """
        if self._clusterer is None or self.embeddings is None:
            return None

        term_lower = skill_term.strip().lower()

        # Fast path: exact match in training set
        if term_lower in self.skill_terms:
            idx = self.skill_terms.index(term_lower)
            label = int(self.cluster_labels[idx])
            return label if label >= 0 else None

        # Slow path: embed and find nearest cluster centroid
        from pipeline.skill_embedder import embed_single
        from sklearn.preprocessing import normalize as sk_normalize

        vec = embed_single(term_lower)
        if vec.size == 0:
            return None

        vec_normed = sk_normalize(vec.reshape(1, -1))[0]

        # Compute centroid for each cluster and find nearest
        best_cluster, best_sim = None, -1.0
        for cluster_id in self.canonical:
            member_indices = [i for i, l in enumerate(self.cluster_labels) if l == cluster_id]
            centroid = normalize(self.embeddings[member_indices].mean(axis=0, keepdims=True))[0]
            sim = float(np.dot(vec_normed, centroid))
            if sim > best_sim:
                best_sim = sim
                best_cluster = cluster_id

        # Only assign if similarity is above threshold
        return best_cluster if best_sim > 0.7 else None

    def to_dict(self) -> dict:
        """Serialise vocabulary state for storage."""
        return {
            "canonical": {str(k): v for k, v in self.canonical.items()},
            "skill_terms": self.skill_terms,
            "cluster_labels": self.cluster_labels.tolist() if self.cluster_labels is not None else [],
        }

    @classmethod
    def from_dict(cls, data: dict) -> "VocabularyBuilder":
        vb = cls()
        vb.canonical = {int(k): v for k, v in data["canonical"].items()}
        vb.skill_terms = data["skill_terms"]
        if data["cluster_labels"]:
            vb.cluster_labels = np.array(data["cluster_labels"])
        return vb


def build_skill_distribution(
    course_skill_sets: list,
    vocab: VocabularyBuilder,
    scenario: str = "core",
) -> dict[int, float]:
    """
    Build a credit-weighted skill distribution vector for a programme.

    Returns dict mapping cluster_id → weighted frequency.

    Credit weights by category (from brainstorm decisions):
      major:    credits × 1.0
      general:  credits × 0.5
      elective: credits × 0.0 (excluded in 'core' scenario)
    """
    WEIGHTS = {"major": 1.0, "general": 0.5, "elective": 1.0}
    if scenario == "core":
        WEIGHTS["elective"] = 0.0

    distribution: Counter = Counter()

    for cs in course_skill_sets:
        weight = cs.credits * WEIGHTS.get(cs.category, 1.0)
        if weight == 0:
            continue
        for skill in cs.skills:
            cluster_id = vocab.assign(skill)
            if cluster_id is not None:
                distribution[cluster_id] += weight

    # Normalise to sum to 1
    total = sum(distribution.values())
    if total == 0:
        return {}
    return {k: v / total for k, v in distribution.items()}
