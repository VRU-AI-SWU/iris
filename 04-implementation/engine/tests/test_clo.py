"""Course learning outcomes and the verbs that carry their cognitive level."""

from __future__ import annotations

import pytest

from iris.ingest.clo import classify_verb, extract_learning_outcomes
from iris.ingest.pdf import repaired_lines
from tests.test_ingest import ALL, needs_corpus

needs_swu = pytest.mark.skipif(ALL["swu"] is None, reason="no corpus")


# ── The verb, which is the level signal ─────────────────────────────────────


@pytest.mark.parametrize(
    ("text", "band"),
    [
        ("อธิบายหลักการของอัลกอริทึม", "understand"),
        ("ออกแบบฐานข้อมูล", "create"),
        ("วิเคราะห์หาความต้องการระบบ", "analyse"),
        ("ประยุกต์ใช้วิธีการพัฒนาระบบ", "apply"),
        ("ประเมินคุณภาพของซอฟต์แวร์", "evaluate"),
        ("ระบุประเภทข้อมูล", "recall"),
    ],
)
def test_leading_verb_places_an_outcome_on_the_cognitive_scale(text, band):
    verb, found = classify_verb(text)
    assert found == band and verb


def test_modal_prefix_is_seen_through():
    """`สามารถออกแบบ…` is a design outcome, not an unclassifiable one."""
    assert classify_verb("สามารถออกแบบระบบฐานข้อมูล")[1] == "create"


def test_longer_verb_wins():
    """`เขียนโปรแกรม` must not be read as `เขียน`."""
    verb, band = classify_verb("เขียนโปรแกรมภาษาไพธอน")
    assert verb == "เขียนโปรแกรม" and band == "apply"


def test_unclassifiable_text_returns_nothing_rather_than_guessing():
    assert classify_verb("ระบบฐานข้อมูลเชิงสัมพันธ์") == (None, None)


# ── Reading the outcome table ───────────────────────────────────────────────


@needs_swu
def test_swu_outcomes_are_tied_to_courses():
    _, report = extract_learning_outcomes(ALL["swu"])
    assert report.outcomes > 100
    assert report.with_course / report.outcomes > 0.85, report.summary()
    assert report.courses > 30
    assert report.rotation == 90  # the outcome table is printed sideways


@needs_swu
def test_most_outcomes_yield_a_verb():
    """The verb is the level signal; if it is missing there is nothing to infer."""
    _, report = extract_learning_outcomes(ALL["swu"])
    assert report.with_verb / report.outcomes > 0.75, report.summary()
    # The scale must be exercised, not collapsed onto one band.
    assert len(report.verb_bands) >= 4


@needs_swu
def test_database_course_outcomes_read_correctly():
    """คพ242 verified by hand against the page: explain, then design."""
    outcomes, _ = extract_learning_outcomes(ALL["swu"])
    cp242 = [o for o in outcomes if o.course_code and "242" in o.course_code]
    assert cp242
    assert any(o.verb_band == "create" for o in cp242), [o.text for o in cp242]


@needs_swu
def test_repair_runs_but_leaves_course_codes_alone():
    """SWU's table maps `2` to `้`, which would turn คพ242 into คพ้4้.

    Substitution applies only where a character has Thai on both sides, so the
    digits in a course code survive while the damaged marks around them do not.
    """
    lines, table = repaired_lines(ALL["swu"])
    assert ("XKSPVT+THSarabunPSK", "2") in table or any(glyph == "2" for _, glyph in table)
    page = [line.text for line in lines if line.page == 124]
    assert any("คพ242" in text for text in page)
    assert not any("คพ้4้" in text for text in page)
    # And the repair did happen on this page.
    assert any("ข้อมูล" in text for text in page)


@needs_corpus
def test_documents_without_per_course_outcomes_say_so():
    """Only outcome-based มคอ.2 state CLOs per course. Absence is reported."""
    _, report = extract_learning_outcomes(ALL["ku"])
    assert report.outcomes == 0
    assert "no per-course learning outcomes" in report.summary()
