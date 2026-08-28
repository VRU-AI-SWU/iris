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

from iris.ingest import (
    Verdict,
    diagnose,
    extract,
    find_intrusions,
    learn_and_repair,
    normalise,
    normalise_chars,
)

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


def test_sara_am_truly_absent_is_lossy():
    """A ำ replaced outright, with no space or nikhahit left behind."""
    report = diagnose(CLEAN_THAI.replace("ำ", "า"))
    assert report.verdict is Verdict.LOSSY
    assert report.sara_am_count == 0


def test_normalise_composes_decomposed_sara_am():
    """Adobe's pattern: ำ written as ํ + า."""
    result = normalise("การดําเนินการ")
    assert result.text == "การดำเนินการ"
    assert result.composed == 1


def test_normalise_rejoins_split_sara_am():
    """Word's pattern: a space where ำ belongs. Safe — า cannot start a word."""
    result = normalise("ค าอธิบายรายวิชา")
    assert result.text == "คำอธิบายรายวิชา"
    assert result.rejoined == 1


def test_normalise_keeps_chars_and_fonts_aligned():
    chars = list("ค าอธิบาย")
    fonts = ["F"] * len(chars)
    out_chars, out_fonts, _ = normalise_chars(chars, fonts)
    assert "".join(out_chars) == "คำอธิบาย"
    assert len(out_chars) == len(out_fonts)


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


#: The corpus lives in `data/programmes/`, git-ignored because the documents are
#: institutional records. `IRIS_TQF_DIR` overrides the location.
def _corpus_root() -> Path:
    override = os.environ.get("IRIS_TQF_DIR")
    if override:
        return Path(override)
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "data" / "programmes"
        if candidate.is_dir():
            return candidate
    return Path("data/programmes")


def _tqf(university: str) -> Path | None:
    matches = sorted(_corpus_root().glob(f"{university}/*/*.pdf"))
    return matches[0] if matches else None


#: Five CS programmes, five different PDF producers — the generality check the
#: solution design asks for.
PRODUCERS = {
    "cmu": "MS Word 2016",
    "ku": "MS Word 2013",
    "psu": "macOS Quartz",
    "su": "Adobe Acrobat Pro",
    "swu": "Bullzip PDF Printer",
}

SWU = _tqf("swu")
KU = _tqf("ku")
ALL = {u: _tqf(u) for u in PRODUCERS}

needs_swu = pytest.mark.skipif(SWU is None, reason="no มคอ.2 corpus in data/programmes/")
needs_ku = pytest.mark.skipif(KU is None, reason="no มคอ.2 corpus in data/programmes/")
needs_corpus = pytest.mark.skipif(
    any(p is None for p in ALL.values()), reason="no มคอ.2 corpus in data/programmes/"
)


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
    chars, fonts, _ = normalise_chars(swu.chars, swu.fonts)
    after = diagnose(learn_and_repair(chars, fonts).text)
    assert after.usable  # what the design requires; the exact label may shift
    assert after.mark_rate > 160  # measured 162.9, against a 171.0 baseline


@needs_ku
def test_ku_sara_am_is_split_not_lost():
    """Word output writes `คำอธิบาย` as `ค าอธิบาย` — a space where ำ belongs.

    Read as raw text this looks lossy, and the feasibility study first recorded
    it as such. It is not: `า` is a dependent vowel and cannot follow a word
    boundary, so a space before it is always an artefact and always recoverable.
    """
    doc = extract(KU)
    assert diagnose(doc.text).verdict is Verdict.LOSSY  # before normalisation

    chars, _, result = normalise_chars(doc.chars, doc.fonts)
    assert result.rejoined > 100
    after = diagnose("".join(chars))
    assert after.verdict is Verdict.CLEAN
    assert "คำอธิบาย" in "".join(chars)


@needs_corpus
@pytest.mark.parametrize("university", sorted(PRODUCERS))
def test_every_producer_reaches_a_usable_text_layer(university):
    """Five universities, five PDF producers, three distinct damage patterns.

    This is the generality check: no hard-coded table, and every document ends
    usable — so none of them needs the vision fallback.
    """
    doc = extract(ALL[university])
    chars, fonts, _ = normalise_chars(doc.chars, doc.fonts)
    report = diagnose("".join(chars))
    if report.verdict is Verdict.REPAIRABLE:
        result = learn_and_repair(chars, fonts)
        assert result.rules, f"{university}: no rules learned"
        report = diagnose(result.text)
    assert report.usable, f"{university} ({PRODUCERS[university]}): {report.summary()}"
