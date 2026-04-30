"""
Skill embedding using text-embedding-embeddinggemma-300m via LM Studio / Ollama.
Produces 300-dimensional vectors for each skill term.
"""
import logging
import numpy as np
from typing import Iterator

from pipeline.llm_client import embed_texts

logger = logging.getLogger(__name__)

BATCH_SIZE = 64


def embed_skills(skill_terms: list[str]) -> np.ndarray:
    """
    Embed a list of skill term strings.
    Returns an (N, D) numpy array where N = number of terms, D = embedding dimension.
    """
    if not skill_terms:
        return np.empty((0,), dtype=np.float32)

    all_embeddings = []
    for batch in _batch(skill_terms, BATCH_SIZE):
        logger.debug("Embedding batch of %d skill terms", len(batch))
        vectors = embed_texts(batch)
        all_embeddings.extend(vectors)

    return np.array(all_embeddings, dtype=np.float32)


def embed_single(text: str) -> np.ndarray:
    """Embed a single text string. Returns a 1D array."""
    vectors = embed_texts([text])
    if not vectors:
        return np.array([], dtype=np.float32)
    return np.array(vectors[0], dtype=np.float32)


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Cosine similarity between two 1D vectors."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def _batch(items: list, size: int) -> Iterator[list]:
    for i in range(0, len(items), size):
        yield items[i : i + size]
