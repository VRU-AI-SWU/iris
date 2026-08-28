"""Document ingestion — the integrity gate, glyph repair, and PDF extraction."""

from iris.ingest.courses import (
    CourseEntry,
    ExtractionReport,
    extract_courses,
    learn_code_shape,
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
    "ExtractedText",
    "ExtractionReport",
    "IntegrityReport",
    "NormaliseResult",
    "RepairResult",
    "Rule",
    "Verdict",
    "diagnose",
    "extract",
    "extract_courses",
    "find_intrusions",
    "is_thai",
    "learn_and_repair",
    "learn_code_shape",
    "normalise",
    "normalise_chars",
]
