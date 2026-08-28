"""Course extraction across five universities.

The extractor never sees a format hint: it anchors on the TQF credit spec and
learns each document's course-code convention from the document itself. These
tests hold that claim to measured numbers.
"""

from __future__ import annotations

import re

import pytest

from iris.ingest import (
    Verdict,
    diagnose,
    extract,
    extract_courses,
    learn_and_repair,
    normalise_chars,
)
from iris.ingest.courses import CREDIT_SPEC, learn_code_shape
from tests.test_ingest import ALL, PRODUCERS, needs_corpus


def _clean_text(pdf):
    doc = extract(pdf)
    chars, fonts, _ = normalise_chars(doc.chars, doc.fonts)
    if diagnose("".join(chars)).verdict is Verdict.REPAIRABLE:
        chars = list(learn_and_repair(chars, fonts).text)
    return "".join(chars), doc.page_of


# ── The anchor ──────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    ("spec", "credits"),
    [("3(3-0-6)", 3), ("1 (0-2-1)", 1), ("3((2)-2-5)", 3), ("2((2)-0-4)", 2)],
)
def test_credit_spec_matches_every_variant_in_the_corpus(spec, credits):
    match = CREDIT_SPEC.search(spec)
    assert match and int(match.group(1)) == credits


def test_credit_spec_ignores_section_numbering():
    """`2.1(3-0-6)` is a section number followed by a range, not a credit spec.

    The lookbehind rejects a digit preceded by a digit or a dot, so neither the
    `2` nor the `1` anchors a course here.
    """
    assert CREDIT_SPEC.search("ข้อ 2.1(3-0-6)") is None


# ── Learned code shapes ─────────────────────────────────────────────────────

EXPECTED_SHAPE = {
    "cmu": "digits-6",
    "ku": "digits-8",
    "psu": "hyphen-3-3",
    "su": "spaced-3-3",
    "swu": "thai-prefix",
}


@needs_corpus
@pytest.mark.parametrize("university", sorted(PRODUCERS))
def test_code_shape_is_learned_from_the_document(university):
    """Five universities, five numbering conventions, none hard-coded."""
    text, _ = _clean_text(ALL[university])
    shape, _ = learn_code_shape(text, list(CREDIT_SPEC.finditer(text)))
    assert shape == EXPECTED_SHAPE[university]


def test_code_shape_prefers_the_more_specific_pattern():
    """An 8-digit code contains a 6-digit one; the longer shape must win."""
    text = "01418221 ระบบฐานข้อมูล 3(3-0-6) 01418232 การออกแบบ 3(3-0-6) 01418236 ระบบ 3(3-0-6)"
    shape, _ = learn_code_shape(text, list(CREDIT_SPEC.finditer(text)))
    assert shape == "digits-8"


# ── Extraction ──────────────────────────────────────────────────────────────

#: Courses whose description is real Thai prose, measured 2026-08-28. Held as
#: lower bounds so a refinement raises them and a regression fails.
MIN_PROSE_COURSES = {"cmu": 80, "ku": 60, "psu": 30, "su": 85, "swu": 68}


def _prose(course) -> int:
    return sum(1 for c in (course.description_th or "") if "฀" <= c <= "๿")


@needs_corpus
@pytest.mark.parametrize("university", sorted(PRODUCERS))
def test_courses_extracted_with_descriptions(university):
    text, page_of = _clean_text(ALL[university])
    courses, report = extract_courses(text, page_of)

    assert report.courses >= 60, report.summary()
    with_prose = [c for c in courses if _prose(c) > 60]
    assert len(with_prose) >= MIN_PROSE_COURSES[university], (
        f"{university}: {len(with_prose)} courses with Thai prose — {report.summary()}"
    )


@needs_corpus
@pytest.mark.parametrize("university", sorted(PRODUCERS))
def test_every_course_records_its_source_page(university):
    """Provenance is a deliverable — a committee will challenge assignments."""
    text, page_of = _clean_text(ALL[university])
    courses, _ = extract_courses(text, page_of)
    assert all(c.page and c.page >= 1 for c in courses)


@needs_corpus
@pytest.mark.parametrize("university", sorted(PRODUCERS))
def test_course_codes_are_unique(university):
    text, page_of = _clean_text(ALL[university])
    courses, _ = extract_courses(text, page_of)
    keys = [c.code.replace(" ", "") for c in courses]
    assert len(keys) == len(set(keys))


@needs_corpus
def test_swu_database_course_is_extracted_correctly():
    """A course verified by hand against the PDF, end to end."""
    text, page_of = _clean_text(ALL["swu"])
    courses, _ = extract_courses(text, page_of)
    cp242 = next(c for c in courses if c.code.replace(" ", "") == "คพ242")
    assert "ฐานข้อมูล" in cp242.title_th
    assert cp242.credits == 3
    assert "เอสคิวแอล" in cp242.description_th  # SQL, the linking target in §3
    assert cp242.page


@needs_corpus
def test_titles_survive_a_line_break():
    """`Introduction to Data Science` must not truncate at the lowercase word."""
    text, page_of = _clean_text(ALL["ku"])
    courses, _ = extract_courses(text, page_of)
    titles = [c.title_en for c in courses if c.title_en]
    assert any(len(t.split()) >= 3 for t in titles)
    assert not any(re.fullmatch(r"[A-Z][a-z]+ (to|of|and|in|for)", t) for t in titles)
