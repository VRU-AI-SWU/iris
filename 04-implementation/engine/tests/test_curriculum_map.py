"""The TQF curriculum-responsibility matrix (แผนที่แสดงการกระจายความรับผิดชอบ).

The marks are drawn in Wingdings and Symbol fonts with no `ToUnicode` mapping,
so text extraction returns the rows with the marks silently missing. They are
read positionally instead, and classified by rendering each glyph and measuring
its ink coverage rather than by consulting a font table.
"""

from __future__ import annotations

from collections import Counter

import pytest

from iris.ingest.curriculum_map import (
    Responsibility,
    _cluster,
    _reading_axes,
    extract_curriculum_map,
)
from tests.test_ingest import ALL, needs_corpus

needs_swu_map = pytest.mark.skipif(ALL["swu"] is None, reason="no corpus")


def test_cluster_groups_aligned_positions():
    assert _cluster([10.0, 10.4, 40.0, 40.3, 70.0], tolerance=2.0) == pytest.approx(
        [10.2, 40.15, 70.0]
    )


def test_cluster_of_nothing_is_nothing():
    assert _cluster([], tolerance=2.0) == []


def test_reading_axes_are_identity_on_an_upright_page():
    assert _reading_axes((10, 20, 30, 40), rotation=0, page_height=800) == (20.0, 30.0)


def test_reading_axes_swap_on_a_rotated_page():
    """SWU prints the matrix sideways, so the reading axis is not x."""
    across, down = _reading_axes((10, 20, 30, 40), rotation=90, page_height=800)
    assert (across, down) == (770.0, 20.0)


@needs_swu_map
def test_swu_matrix_is_read_from_glyph_positions():
    _, report = extract_curriculum_map(ALL["swu"])

    assert report.rotation == 90  # the matrix is printed sideways
    assert report.marks_assigned / report.marks_found > 0.85, report.summary()
    assert report.courses > 40
    # TQF's five outcome domains, sub-numbered
    assert {"1.1", "2.1", "3.1", "4.1", "5.1"} <= set(report.outcomes)


@needs_swu_map
def test_swu_marks_distinguish_primary_from_secondary():
    """The distinction level inference depends on: ● หลัก versus ○ รอง."""
    marks, report = extract_curriculum_map(ALL["swu"])
    counts = Counter(m.responsibility for m in marks)
    assert counts[Responsibility.PRIMARY] > 100
    assert counts[Responsibility.SECONDARY] > 100

    # Classification is by measured ink, and the two glyphs must separate.
    inks = sorted(report.glyph_ink.values(), reverse=True)
    assert inks[0] > inks[-1] * 1.3


@needs_swu_map
def test_every_mark_carries_its_page():
    marks, _ = extract_curriculum_map(ALL["swu"])
    assert all(m.page >= 1 for m in marks)
    assert all(m.course_code and m.outcome for m in marks)


@needs_corpus
def test_documents_without_a_matrix_report_so_rather_than_guessing():
    """KU is a 28-page excerpt with no matrix. Absence must be explicit."""
    marks, report = extract_curriculum_map(ALL["ku"])
    assert marks == []
    assert "no curriculum-responsibility matrix" in report.summary()
