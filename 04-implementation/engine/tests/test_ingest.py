"""Integrity gate and glyph repair.

Two layers. The synthetic tests always run and pin the gate's logic. The
document tests run against the real มคอ.2 files and are skipped when they are
not present — they live outside the repository because they are institutional
documents, so `IRIS_TQF_DIR` points at wherever they are kept.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from iris.ingest import Verdict, diagnose, extract, find_intrusions, learn_and_repair

# ── Synthetic: the gate's logic, independent of any document ────────────────

CLEAN_THAI = (
    "หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ ระบบฐานข้อมูล "
    "การสร้างแบบจำลองและออกแบบฐานข้อมูลเชิงสัมพันธ์ ภาษาเอสคิวแอล "
    "การรักษาความปลอดภัยฐานข้อมูล ผลการเรียนรู้ที่คาดหวัง จำนวนหน่วยกิต "
) * 40  # long enough for the sara-am threshold (5,000 Thai chars)


def test_clean_thai_passes():
    report = diagnose(CLEAN_THAI)
    assert report.verdict is Verdict.CLEAN
    assert report.usable


def test_substitution_damage_is_flagged_repairable():
    """The SWU failure mode: marks replaced by ASCII inside Thai words."""
    damaged = CLEAN_THAI.replace("้", "2").replace("์", "=")
    report = diagnose(damaged)
    assert report.verdict is Verdict.REPAIRABLE
    assert not report.usable
    assert report.intrusion_glyphs.get("2", 0) > 0


def test_sara_am_collapse_is_lossy_not_repairable():
    """The KU failure mode. No table can recover it — route to vision."""
    report = diagnose(CLEAN_THAI.replace("ำ", "า"))
    assert report.verdict is Verdict.LOSSY
    assert report.sara_am_count == 0
    assert any("sara am" in note for note in report.notes)


def test_too_little_thai_is_unusable():
    """What a scanned PDF with no text layer looks like."""
    report = diagnose("Faculty of Science " * 40)
    assert report.verdict is Verdict.UNUSABLE


def test_verdict_ignores_vocabulary_driven_rate_differences():
    """Per-mark rates vary with content; the verdict must not turn on them.

    Text with unusually heavy karan is clean, not damaged — this is the failure
    the first version of the gate had.
    """
    karan_heavy = "คอมพิวเตอร์ ซอฟต์แวร์ อิเล็กทรอนิกส์ วิศวกรรมศาสตร์ " * 40
    # Deliberately contains no ำ — the gate must not read that as collapse in a
    # passage this short. This case is why SARA_AM_MIN_THAI exists.
    assert diagnose(karan_heavy).verdict is Verdict.CLEAN


def test_intrusions_require_thai_on_both_sides():
    chars = list("ข2อมูล A ทั่วไป")
    assert [chars[i] for i in find_intrusions(chars)] == ["2"]


def test_repair_recovers_a_known_substitution():
    damaged = CLEAN_THAI.replace("้", "2")
    result = learn_and_repair(list(damaged))
    assert result.repaired > 0
    assert any(rule.glyph == "2" and rule.mark == "้" for rule in result.rules)
    assert "ข้อมูล" in result.text


def test_repair_rejects_mismatched_inputs():
    with pytest.raises(ValueError, match="same length"):
        learn_and_repair(list("ข2อ"), ["a"])


# ── Real documents ─────────────────────────────────────────────────────────


def _tqf(*parts: str) -> Path | None:
    root = os.environ.get("IRIS_TQF_DIR")
    if not root:
        return None
    path = Path(root).joinpath(*parts)
    return path if path.is_file() else None


SWU = _tqf("swu", "cs", "computer_science", "tqf", "swu-tqf-cs-2022.pdf")
KU = _tqf("ku", "cs", "computer_science", "tqf", "ku_tqf_cs_2022.pdf")

needs_swu = pytest.mark.skipif(SWU is None, reason="set IRIS_TQF_DIR to the มคอ.2 directory")
needs_ku = pytest.mark.skipif(KU is None, reason="set IRIS_TQF_DIR to the มคอ.2 directory")


@pytest.fixture(scope="module")
def swu():
    return extract(SWU)


@needs_swu
def test_swu_diagnoses_repairable(swu):
    """216 pages, WinAnsi-encoded THSarabunPSK — the substitution case."""
    report = diagnose(swu.text)
    assert report.verdict is Verdict.REPAIRABLE
    assert report.thai_chars > 130_000
    assert 130 < report.mark_rate < 140  # measured 134.5
    assert report.intrusions > 4_000


@needs_swu
def test_swu_repair_learns_rules_without_hardcoding(swu):
    """No table is supplied; every rule is inferred from the document."""
    result = learn_and_repair(swu.chars, swu.fonts)
    learned = {(rule.glyph, rule.mark) for rule in result.rules}
    # The highest-frequency substitutions, verified by hand against the PDF.
    assert ("2", "้") in learned
    assert ("=", "์") in learned
    assert ("?", "็") in learned
    assert result.repaired / result.intrusions_before > 0.85


@needs_swu
def test_swu_repair_restores_real_words(swu):
    """The check that matters: words a reader can verify against the page."""
    text = learn_and_repair(swu.chars, swu.fonts).text
    for word in ("ข้อมูล", "คอมพิวเตอร์", "ผลการเรียนรู้", "หน่วยกิต", "เป็น", "วิเคราะห์"):
        assert word in text, f"{word} not recovered"


@needs_swu
def test_swu_passes_the_gate_after_repair(swu):
    """Repairable in, usable out — the gate must be re-run, and must pass."""
    after = diagnose(learn_and_repair(swu.chars, swu.fonts).text)
    assert after.verdict is Verdict.REPAIRED
    assert after.usable
    assert after.mark_rate > 160  # measured 162.9, against a 171.0 baseline


@needs_ku
def test_ku_is_lossy_and_routed_to_vision():
    """Word 2013 output: every ำ collapsed to า. Not repairable from text."""
    report = diagnose(extract(KU).text)
    assert report.verdict is Verdict.LOSSY
    assert report.sara_am_count == 0
    assert not report.usable
