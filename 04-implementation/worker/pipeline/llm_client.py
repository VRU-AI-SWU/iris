"""
Single point of contact for all LLM and embedding calls.
Supports LM Studio (dev) and Ollama (prod) via the same OpenAI-compatible API.
"""
import json
import logging
import os
import time
from typing import Any

from openai import OpenAI, APIError

logger = logging.getLogger(__name__)

_client: OpenAI | None = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            base_url=os.getenv("MODEL_SERVER_URL", "http://host.docker.internal:1234/v1"),
            api_key=os.getenv("MODEL_API_KEY", "lm-studio"),
        )
    return _client


EXTRACTION_MODEL = os.getenv("EXTRACTION_MODEL", "gemma-4-31b-it")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "text-embedding-embeddinggemma-300m")


def extract_skills(text: str, retries: int = 3, delay: float = 2.0) -> list[str]:
    """
    Extract skill terms from text using zero-shot LLM prompt.
    Returns a list of skill strings.
    """
    prompt = (
        "You are a skill extraction assistant. "
        "Extract all technical skills, tools, programming languages, frameworks, "
        "methodologies, and domain knowledge areas mentioned in the following text. "
        "Return ONLY a JSON array of short skill strings (1–5 words each). "
        "Do not include soft skills. If no skills are found, return [].\n\n"
        f"Text:\n{text}\n\n"
        "Skills (JSON array):"
    )

    for attempt in range(retries):
        try:
            response = get_client().chat.completions.create(
                model=EXTRACTION_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0,
                max_tokens=512,
            )
            raw = response.choices[0].message.content.strip()
            # Strip markdown code fences if present
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            skills = json.loads(raw)
            if isinstance(skills, list):
                return [str(s).strip() for s in skills if s]
            return []
        except (json.JSONDecodeError, APIError) as e:
            logger.warning("Skill extraction attempt %d failed: %s", attempt + 1, e)
            if attempt < retries - 1:
                time.sleep(delay)
    logger.error("Skill extraction failed after %d attempts", retries)
    return []


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts using the embedding model."""
    if not texts:
        return []
    response = get_client().embeddings.create(
        model=EMBEDDING_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]


def generate_narrative(prompt: str, max_tokens: int = 800) -> str:
    """Generate a plain-language narrative from a structured prompt."""
    response = get_client().chat.completions.create(
        model=EXTRACTION_MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()
