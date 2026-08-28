"""Types for the national skill standard.

These mirror the Thailand Skill Mapping API's shape, with the project's hard
constraints expressed in the types themselves rather than left to convention.

The most important of those: **there is no proficiency level on the demand side.**
`SkillDemand` carries a count and a prevalence and nothing else, because that is
all a career × skill entry contains. Levels live on `Skill`, where they describe
what foundational / intermediate / advanced *mean* for that skill — not what any
career requires. A type that cannot express a demanded level cannot accidentally
report one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

# Career slug prefixes that denote a rung on a seniority ladder.
SENIORITY_PREFIXES = ("junior", "senior", "lead", "principal", "chief")

# Careers with fewer skills than this are degenerate and excluded from analysis.
MIN_SKILLS_PER_CAREER = 10


class SkillType(StrEnum):
    HARD = "hard-skill"
    SOFT = "soft-skill"
    TOOLS = "tools"


@dataclass(frozen=True, slots=True)
class Level:
    """One of a skill's three proficiency levels, with its observable criteria."""

    name: str  # ระดับพื้นฐาน / ระดับปานกลาง / ระดับสูง
    criteria: tuple[str, ...]
    ordinal: int  # 0 = foundational, 1 = intermediate, 2 = advanced


@dataclass(frozen=True, slots=True)
class Skill:
    """An entry in the national vocabulary."""

    id: str
    slug: str
    title_th: str
    title_en: str | None
    type: SkillType
    definition: str | None = None
    levels: tuple[Level, ...] = ()

    @property
    def has_levels(self) -> bool:
        return len(self.levels) == 3

    def surface_forms(self) -> tuple[str, ...]:
        """Every string this skill can be matched against.

        Three forms per entry, supplied free by the standard — the *synonym
        enhancement* that BLINKout (dong-2023) had to construct by hand.
        """
        return tuple(f for f in (self.title_th, self.title_en, self.definition) if f)


@dataclass(frozen=True, slots=True)
class SkillDemand:
    """One career × skill demand entry.

    `prevalence` is the share of that career's postings mentioning the skill —
    **not** a share of a distribution. Prevalences across a career sum to well
    over 100. There is deliberately no `level` field.
    """

    skill_id: str
    count: int
    prevalence: float  # percentage points, 0–100

    @property
    def is_degenerate(self) -> bool:
        """A skill listed for a career with no supporting evidence."""
        return self.count == 0


@dataclass(frozen=True, slots=True)
class Career:
    id: str
    slug: str
    title_th: str
    industry_slug: str
    description: str | None
    demand: tuple[SkillDemand, ...]
    growth: dict[str, float] = field(default_factory=dict)  # skill_id -> growth %

    @property
    def is_degenerate(self) -> bool:
        return len(self.demand) < MIN_SKILLS_PER_CAREER

    @property
    def posting_total(self) -> float | None:
        """`N` for this career, derived as count / prevalence × 100.

        Constant across the career's entries, so any non-zero one recovers it.
        Range across the digital industry is 203 to 6,291,725 — implausible for
        Thailand alone, which is why the corpus provenance is an open question
        and why RCA uses a career-equal denominator.
        """
        for d in self.demand:
            if d.prevalence > 0:
                return d.count / d.prevalence * 100
        return None

    def seniority(self) -> tuple[str, str] | None:
        """`(rung, base_slug)` if this career's slug names a seniority rung."""
        for prefix in SENIORITY_PREFIXES:
            if self.slug.startswith(f"{prefix}-"):
                return prefix, self.slug[len(prefix) + 1 :]
        return None


@dataclass(frozen=True, slots=True)
class Industry:
    id: str
    slug: str
    title_th: str
    title_en: str | None


# Rungs whose prefix names a level *below* the unprefixed career.
BELOW_BASE_RUNGS = frozenset({"junior"})


@dataclass(frozen=True, slots=True)
class SeniorityPair:
    """Two rungs of one career ladder, the demand-side depth signal.

    Not a proficiency requirement. It measures which skills gain prominence with
    experience, which is a different and weaker claim — and the only one the data
    supports.

    ⚠️ Direction is not uniform. `senior-`, `lead-`, `principal-` and `chief-`
    sit *above* the unprefixed career; `junior-` sits *below* it. The fields are
    named `lower` and `higher` rather than base/senior so the ladder direction is
    resolved once, here, instead of at every call site.
    """

    lower: Career
    higher: Career
    rung: str  # junior | senior | lead | principal | chief

    @classmethod
    def from_rung(cls, rung: str, prefixed: Career, unprefixed: Career) -> SeniorityPair:
        if rung in BELOW_BASE_RUNGS:
            return cls(lower=prefixed, higher=unprefixed, rung=rung)
        return cls(lower=unprefixed, higher=prefixed, rung=rung)

    @property
    def slug(self) -> str:
        return f"{self.lower.slug}→{self.higher.slug}"

    def gradient(self) -> list[tuple[str, float]]:
        """`(skill_id, Δ prevalence)` over skills present at both rungs.

        Positive means the skill is more prevalent higher up the ladder. Sorted
        descending, so the head of the list is what gains most with seniority.
        Degenerate (`count == 0`) entries are excluded from both sides.
        """
        lo = {d.skill_id: d.prevalence for d in self.lower.demand if not d.is_degenerate}
        hi = {d.skill_id: d.prevalence for d in self.higher.demand if not d.is_degenerate}
        return sorted(((s, hi[s] - lo[s]) for s in lo.keys() & hi.keys()), key=lambda x: -x[1])
