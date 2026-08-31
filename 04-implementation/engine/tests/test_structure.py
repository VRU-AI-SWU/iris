"""Reading the programme structure, and drawing the annotation sample.

The structure reader answers one question — is this course core, elective, or
general education — and it took four attempts to get right on real text. These tests
pin the failures so they cannot come back.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from iris.annotation import STRATA, draw_sample
from iris.annotation.sample import MIN_PER_STRATUM, fingerprint
from iris.ingest.structure import CREDIT_SPEC, HEADING, classify, extract_structure

SWU = Path(
    "/Users/rucci/VRU-AI/projects/iris/data/programmes/swu/faculty-of-science/TQF-Com-Sci-2022.pdf"
)
pytestmark = pytest.mark.skipif(not SWU.exists(), reason="institutional document, not committed")


@pytest.fixture(scope="module")
def swu():
    return extract_structure(SWU)


# ── Reading the headings ────────────────────────────────────────────────────


def test_a_numbered_heading_is_recognised():
    match = HEADING.search("2.2 วิชาบังคับ กำหนดให้เรียน รวม 48 หน่วยกิต")
    assert match and match.group(1) == "2.2"


def test_a_heading_keeps_its_credit_figure_across_a_damaged_word():
    """Repaired Thai carries separator control characters where a producer broke a
    word. Matching intra-line space as `[ \\t]` stops at the break and loses the
    figure after it — which is how every credit check came back empty."""
    damaged = "2.2 วิชาบังคับ กำหนดให้เรียน รวม 48 หน\x1fวยกิต"
    match = HEADING.search(damaged)
    assert match and "48" in match.group(2)


def test_an_unnumbered_mention_is_not_a_heading():
    assert HEADING.search("นิสิตต้องเรียนวิชาบังคับให้ครบตามที่กำหนด") is None


# ── The three strata ────────────────────────────────────────────────────────


def test_general_education_is_its_own_stratum():
    assert classify("1.1", "วิชาบังคับ", "general-education") == "general-education"


def test_a_required_major_subdivision_is_core():
    assert classify("2.2", "วิชาบังคับ", "major") == "core"
    assert classify("2.1", "วิชาแกน", "major") == "core"


def test_an_elective_subdivision_is_elective_whatever_it_is_called():
    """The subdivision vocabulary is not regulated, so it is read rather than
    enumerated — `วิชาโท` and `วิชาเลือก` are both elective by their wording."""
    assert classify("2.3", "วิชาเลือก", "major") == "elective"
    assert classify("2.4", "วิชาโท", "major") == "elective"
    assert classify("3", "หมวดวิชาเลือกเสรี", "free-elective") == "elective"


# ── What the document says about itself ─────────────────────────────────────


def test_the_listing_is_read_not_the_credit_table(swu):
    """A มคอ.2 states its structure twice — a credit table with no courses, then the
    listing. Three earlier rules picked the table: most room below the heading, most
    courses per number independently, and one contiguous block."""
    _, report = swu
    assert {c.number for c in report.categories} >= {"1.1", "2.1", "2.2", "2.3"}
    listing_pages = {c.page for c in report.categories}
    assert min(listing_pages) >= 18, "page 17 is the credit table, not the listing"


def test_core_credits_match_what_the_document_claims(swu):
    """`2.1 วิชาแกน` claims 12 credits. Reading exactly 12 is the check that the
    required categories are listed exhaustively — which is what licenses treating a
    described course absent from them as not-core."""
    _, report = swu
    core = next(c for c in report.categories if c.number == "2.1")
    assert core.claimed_credits == 12
    assert report.credits_by_category["2.1"] == 12


def test_a_category_that_lists_no_courses_claims_none(swu):
    """SWU's `3. หมวดวิชาเลือกเสรี` says to choose any course in the university and
    names none. A fixed-span rule let it swallow the study plan two pages later and
    label 42 of 57 courses free electives."""
    _, report = swu
    assert report.credits_by_category.get("3", 0) == 0


def test_required_courses_land_in_the_required_category(swu):
    placed, _ = swu
    for code in ("คพ241", "คพ242", "คพ231", "คพ222"):
        assert placed[code].stratum == "core", f"{code} → {placed[code]}"


def test_general_education_courses_are_recognised(swu):
    placed, _ = swu
    assert placed["มศว191"].stratum == "general-education"
    assert placed["มศว291"].stratum == "general-education"


def test_a_mention_without_a_credit_spec_is_not_a_catalogue_row():
    assert CREDIT_SPEC.search("คพ 494 ที่มีการฝึกงานไม่น้อยกว่า 120 ชั่วโมง") is None
    assert CREDIT_SPEC.search("คพ242 CP242 ระบบฐานข้อมูล 3(2-2-5)") is not None


# ── The sample ──────────────────────────────────────────────────────────────


def test_the_sample_is_reproducible():
    """A gold standard that shifts between runs cannot anchor a published number."""
    first, _ = draw_sample(SWU)
    second, _ = draw_sample(SWU)
    assert fingerprint(first) == fingerprint(second)
    assert [c.code for c in first] == [c.code for c in second]


def test_a_different_seed_draws_a_different_sample():
    a, _ = draw_sample(SWU, seed=1)
    b, _ = draw_sample(SWU, seed=2)
    assert fingerprint(a) != fingerprint(b)


def test_every_stratum_is_represented():
    courses, report = draw_sample(SWU)
    for stratum in STRATA:
        assert report.drawn[stratum] > 0, f"{stratum} is empty"
    assert len(courses) <= 50


def test_an_under_powered_stratum_is_reported_not_padded():
    """SWU describes 6 general-education courses against a floor of 8. Taking all 6
    and saying so is honest; quietly redistributing the shortfall is not."""
    _, report = draw_sample(SWU)
    small = [s for s in STRATA if report.population[s] < MIN_PER_STRATUM]
    for stratum in small:
        assert report.drawn[stratum] == report.population[stratum]
        assert any(stratum in note for note in report.notes)


def test_courses_categorised_by_elimination_are_flagged():
    """A label the document states and a label inferred from its absence are not the
    same evidence, and an annotator can see which is which."""
    courses, report = draw_sample(SWU)
    assert report.by_elimination > 0
    inferred = [c for c in courses if c.by_elimination]
    assert all(c.category == "—" for c in inferred)


def test_every_sampled_course_carries_its_description_and_page():
    courses, _ = draw_sample(SWU)
    assert all(c.description for c in courses)
    assert all(c.page for c in courses)
