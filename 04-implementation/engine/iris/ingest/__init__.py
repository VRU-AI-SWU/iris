"""Document ingestion — the integrity gate, glyph repair, and PDF extraction."""

from iris.ingest.courses import (
    CourseEntry,
    ExtractionReport,
    extract_courses,
    learn_code_shape,
)
from iris.ingest.curriculum_map import (
    CurriculumMapReport,
    CurriculumMark,
    Responsibility,
    extract_curriculum_map,
)
from iris.ingest.integrity import (
    CLEAN_BASELINE,
    IntegrityReport,
    Verdict,
    diagnose,
    is_thai,
)
from iris.ingest.normalise import NormaliseResult, normalise, normalise_chars
from iris.ingest.pdf import ExtractedText, extract
from iris.ingest.repair import RepairResult, Rule, find_intrusions, learn_and_repair

__all__ = [
    "CLEAN_BASELINE",
    "CourseEntry",
    "CurriculumMapReport",
    "CurriculumMark",
    "ExtractedText",
    "ExtractionReport",
    "IntegrityReport",
    "NormaliseResult",
    "RepairResult",
    "Responsibility",
    "Rule",
    "Verdict",
    "diagnose",
    "extract",
    "extract_courses",
    "extract_curriculum_map",
    "find_intrusions",
    "is_thai",
    "learn_and_repair",
    "learn_code_shape",
    "normalise",
    "normalise_chars",
]
