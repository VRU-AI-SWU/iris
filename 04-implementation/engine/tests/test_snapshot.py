"""Snapshot loader tests.

These double as a **regression check on the snapshot itself**. The figures are
taken from `03-solution-design/data-feasibility.md`; if a re-fetch changes the
upstream data, these fail loudly rather than letting an analysis silently shift
under a paper's published numbers.
"""

from __future__ import annotations

import pytest

from iris.snapshot import SkillType, load_snapshot
from iris.snapshot.models import MIN_SKILLS_PER_CAREER


@pytest.fixture(scope="module")
def snap():
    return load_snapshot()


# ── Vocabulary ──────────────────────────────────────────────────────────────


def test_vocabulary_size_matches_feasibility_study(snap):
    assert len(snap.skills) == 4376


def test_skill_type_distribution(snap):
    assert len(snap.skills_by_type(SkillType.HARD)) == 2911
    assert len(snap.skills_by_type(SkillType.TOOLS)) == 912
    assert len(snap.skills_by_type(SkillType.SOFT)) == 553


def test_referenced_skills_all_carry_three_levels(snap):
    """2,043 skills are referenced by digital careers; every one has all three."""
    with_levels = [s for s in snap.skills if s.has_levels]
    assert len(with_levels) == 2043
    assert all(len(s.levels) == 3 for s in with_levels)


def test_levels_are_ordered_foundational_to_advanced(snap):
    sql = snap.skill_by_slug("sql")
    assert sql is not None
    assert [level.ordinal for level in sql.levels] == [0, 1, 2]
    assert sql.levels[0].name == "ระดับพื้นฐาน"
    assert sql.levels[2].name == "ระดับสูง"
    assert all(level.criteria for level in sql.levels)


def test_bilingual_coverage_is_complete(snap):
    assert all(s.title_en for s in snap.skills)


def test_surface_forms_give_synonym_enhancement(snap):
    """Three matchable forms per referenced skill, supplied by the standard."""
    sql = snap.skill_by_slug("sql")
    forms = sql.surface_forms()
    assert sql.title_th in forms and sql.title_en in forms
    assert len(forms) == 3  # Thai title, English title, Thai definition


# ── Demand side ─────────────────────────────────────────────────────────────


def test_zero_count_demand_pairs_are_dropped_and_counted(snap):
    assert snap.report.demand_pairs_dropped_zero_count == 168
    assert all(d.count > 0 for c in snap.careers(include_degenerate=True) for d in c.demand)


def test_python_is_not_a_data_engineer_skill_after_filtering(snap):
    """The clearest zero-count error in the upstream data."""
    de = snap.career("data-engineer")
    python = snap.skill_by_slug("python")
    assert python.id not in {d.skill_id for d in de.demand}


def test_degenerate_careers_are_excluded_by_default(snap):
    assert len(snap.careers(include_degenerate=True)) == 138
    assert len(snap.careers()) == 135
    assert all(len(c.demand) >= MIN_SKILLS_PER_CAREER for c in snap.careers())


def test_prevalence_does_not_sum_to_one_hundred(snap):
    """Prevalence is not a distribution — the fact the metric design turns on."""
    de = snap.career("data-engineer")
    assert sum(d.prevalence for d in de.demand) > 100


def test_posting_totals_span_four_orders_of_magnitude(snap):
    """The unresolved corpus-provenance question, asserted so it stays visible."""
    totals = [c.posting_total for c in snap.careers() if c.posting_total]
    assert min(totals) < 1_000
    assert max(totals) > 1_000_000


def test_demand_entries_carry_no_level(snap):
    """The demand side has no proficiency level. The type must not grow one."""
    de = snap.career("data-engineer")
    assert not hasattr(de.demand[0], "level")


# ── Seniority ladders ───────────────────────────────────────────────────────


def test_analysable_seniority_pairs(snap):
    """13 pairs exist in the raw data; 12 survive the degenerate-career filter.

    `senior-frontend-developer` has 5 skills, so its gradient would be computed
    over a handful of entries. See data-feasibility.md.
    """
    assert len(snap.seniority_pairs) == 12
    assert "frontend-developer" not in {p.higher.slug for p in snap.seniority_pairs}


def test_data_scientist_ladder_has_three_steps(snap):
    """base → senior, base → lead, base → chief."""
    steps = snap.seniority_pairs_for("data-scientist")
    assert {p.rung for p in steps} == {"senior", "lead", "chief"}


def test_junior_rung_points_downward(snap):
    """`junior-X` sits *below* X — the one ladder whose direction inverts."""
    (step,) = [p for p in snap.seniority_pairs if p.rung == "junior"]
    assert step.lower.slug == "junior-software-engineer"
    assert step.higher.slug == "software-engineer"


def test_seniority_gradient_ranks_deeper_skills_higher(snap):
    """Data Scientist → Senior: modelling and statistics gain, tooling does not."""
    (step,) = [
        p
        for p in snap.seniority_pairs_for("data-scientist")
        if p.higher.slug == "senior-data-scientist"
    ]
    gradient = step.gradient()
    top = [snap.skill(sid).title_en for sid, _ in gradient[:5]]
    assert "Predictive Modeling" in top
    assert gradient[0][1] > 10  # top mover gains more than 10 percentage points
    assert gradient[0][1] > gradient[-1][1]


# ── Provenance ──────────────────────────────────────────────────────────────


def test_report_pins_the_snapshot_identity(snap):
    assert snap.report.snapshot_date == "2026-08-27"
    assert snap.report.api_version == "0.8.1-beta-public"


def test_missing_snapshot_fails_loudly(tmp_path):
    with pytest.raises(FileNotFoundError, match="snapshot directory not found"):
        load_snapshot(tmp_path / "nope")
