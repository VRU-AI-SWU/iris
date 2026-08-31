"""Skill linking — retrieve candidates from the national vocabulary, then adjudicate.

Two stages, kept separate because they fail differently. Retrieval is lexical and
cheap and its errors are *misses*; adjudication is a model call and its errors are
*false links*. Measuring them together would hide which half is weak.
"""

from iris.link.adjudicate import (
    DEFAULT_K,
    Adjudication,
    AdjudicationReport,
    SkillLink,
    adjudicate,
    build_prompt,
    verify_evidence,
)
from iris.link.pipeline import CourseText, link_courses, link_programme, read_courses
from iris.link.provider import (
    Completion,
    OpenAICompatible,
    Provider,
    ProviderError,
    QuotaExhausted,
    RecordingProvider,
    WorkersAI,
    get_provider,
)
from iris.link.retrieval import Candidate, SkillIndex, get_index, skeleton, tokenize

__all__ = [
    "DEFAULT_K",
    "Adjudication",
    "AdjudicationReport",
    "Candidate",
    "Completion",
    "CourseText",
    "OpenAICompatible",
    "Provider",
    "ProviderError",
    "QuotaExhausted",
    "RecordingProvider",
    "SkillIndex",
    "SkillLink",
    "WorkersAI",
    "adjudicate",
    "build_prompt",
    "get_index",
    "get_provider",
    "link_courses",
    "link_programme",
    "read_courses",
    "skeleton",
    "tokenize",
    "verify_evidence",
]
