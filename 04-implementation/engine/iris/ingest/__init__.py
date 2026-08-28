"""Document ingestion — the integrity gate, glyph repair, and PDF extraction."""

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
    "ExtractedText",
    "IntegrityReport",
    "NormaliseResult",
    "RepairResult",
    "Rule",
    "Verdict",
    "diagnose",
    "extract",
    "find_intrusions",
    "is_thai",
    "learn_and_repair",
    "normalise",
    "normalise_chars",
]
