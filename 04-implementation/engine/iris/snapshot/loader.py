"""Load a pinned snapshot of the national skill standard.

The snapshot is read-only reference data and the reproducibility anchor: an
analysis records which snapshot it used, and the engine **never** calls the live
API. See `data/skillmapping/fetch_snapshot.py` for how a snapshot is produced.

This module is also where the design's data-quality rules stop being prose and
become code. Two are applied on load and cannot be bypassed by a caller:

- career × skill entries with `count == 0` are dropped (168 in the 2026-08-27
  snapshot, including Python and Pandas for วิศวกรข้อมูล — obvious errors)
- careers with fewer than 10 skills are marked degenerate and excluded from
  analysis (3 in the digital industry)

Both are counted and reported rather than silently applied.
"""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass, replace
from functools import lru_cache
from pathlib import Path

from iris.config import get_settings
from iris.snapshot.models import (
    Career,
    Industry,
    Level,
    SeniorityPair,
    Skill,
    SkillDemand,
    SkillType,
)

# The standard's level names, in ascending order of depth.
LEVEL_ORDER = ("ระดับพื้นฐาน", "ระดับปานกลาง", "ระดับสูง")


@dataclass(frozen=True, slots=True)
class LoadReport:
    """What the loader kept, dropped, and flagged — reported, never silent."""

    snapshot_date: str
    api_version: str
    industries: int
    careers_loaded: int
    careers_degenerate: int
    skills_total: int
    skills_with_levels: int
    demand_pairs_kept: int
    demand_pairs_dropped_zero_count: int
    seniority_pairs: int

    def summary(self) -> str:
        return (
            f"snapshot {self.snapshot_date} (API {self.api_version}): "
            f"{self.skills_total:,} skills ({self.skills_with_levels:,} with levels), "
            f"{self.careers_loaded} careers ({self.careers_degenerate} degenerate), "
            f"{self.demand_pairs_kept:,} demand pairs "
            f"({self.demand_pairs_dropped_zero_count} zero-count dropped), "
            f"{self.seniority_pairs} seniority pairs"
        )


class Snapshot:
    """An immutable view over one pinned snapshot."""

    def __init__(
        self,
        *,
        industries: list[Industry],
        careers: list[Career],
        skills: list[Skill],
        report: LoadReport,
    ) -> None:
        self._industries = tuple(industries)
        self._careers = tuple(careers)
        self._skills = tuple(skills)
        self.report = report

        self._skill_by_id = {s.id: s for s in skills}
        self._skill_by_slug = {s.slug: s for s in skills}
        self._career_by_slug = {c.slug: c for c in careers}
        self._seniority_pairs = tuple(self._build_seniority_pairs())

    # ── Vocabulary ──────────────────────────────────────────────────────────

    @property
    def skills(self) -> tuple[Skill, ...]:
        """The full national vocabulary, including skills no career references."""
        return self._skills

    def skill(self, skill_id: str) -> Skill | None:
        return self._skill_by_id.get(skill_id)

    def skill_by_slug(self, slug: str) -> Skill | None:
        return self._skill_by_slug.get(slug)

    def skills_by_type(self, skill_type: SkillType) -> tuple[Skill, ...]:
        return tuple(s for s in self._skills if s.type is skill_type)

    # ── Careers ─────────────────────────────────────────────────────────────

    @property
    def industries(self) -> tuple[Industry, ...]:
        return self._industries

    def careers(self, *, include_degenerate: bool = False) -> tuple[Career, ...]:
        """Analysable careers. Degenerate ones are excluded unless asked for."""
        if include_degenerate:
            return self._careers
        return tuple(c for c in self._careers if not c.is_degenerate)

    def career(self, slug: str) -> Career | None:
        return self._career_by_slug.get(slug)

    # ── Seniority ladders ───────────────────────────────────────────────────

    @property
    def seniority_pairs(self) -> tuple[SeniorityPair, ...]:
        """Career pairs one rung apart — the demand-side depth signal.

        Only pairs where *both* rungs are analysable; a degenerate rung would
        produce a gradient computed over a handful of skills.
        """
        return self._seniority_pairs

    def seniority_pairs_for(self, slug: str) -> tuple[SeniorityPair, ...]:
        """Every ladder step this career participates in, either end."""
        return tuple(p for p in self._seniority_pairs if slug in (p.lower.slug, p.higher.slug))

    def _build_seniority_pairs(self) -> list[SeniorityPair]:
        pairs: list[SeniorityPair] = []
        for career in self._careers:
            rung_base = career.seniority()
            if rung_base is None:
                continue
            rung, base_slug = rung_base
            base = self._career_by_slug.get(base_slug)
            if base is None or base.is_degenerate or career.is_degenerate:
                continue
            pairs.append(SeniorityPair.from_rung(rung, prefixed=career, unprefixed=base))
        return sorted(pairs, key=lambda p: p.slug)


# ── Loading ─────────────────────────────────────────────────────────────────


def _read(path: Path) -> object:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def _levels(raw: list[dict] | None) -> tuple[Level, ...]:
    if not raw:
        return ()
    out = []
    for entry in raw:
        name = entry.get("level", "")
        ordinal = LEVEL_ORDER.index(name) if name in LEVEL_ORDER else len(out)
        criteria = tuple(c["criteria"] for c in entry.get("criteria", []) if c.get("criteria"))
        out.append(Level(name=name, criteria=criteria, ordinal=ordinal))
    return tuple(sorted(out, key=lambda level: level.ordinal))


def load_snapshot(path: Path | None = None) -> Snapshot:
    """Read a snapshot directory into an immutable in-memory view."""
    root = Path(path) if path else get_settings().skillmap_snapshot
    if not root.is_dir():
        raise FileNotFoundError(
            f"snapshot directory not found: {root}\n"
            "Run data/skillmapping/fetch_snapshot.py, or set SKILLMAP_SNAPSHOT."
        )

    manifest = _read(root / "manifest.json")
    raw_industries = _read(root / "industries.json")
    raw_careers = _read(root / "careers.json")
    raw_index = _read(root / "skills-index.json")
    raw_detail = _read(root / "skills-detail.json")

    detail_by_id = {d["id"]: d for d in raw_detail}

    skills = [
        Skill(
            id=s["id"],
            slug=s["slug"],
            title_th=s["title"],
            title_en=s.get("title_en"),
            type=SkillType(s["type"]),
            definition=(detail_by_id.get(s["id"]) or {}).get("definition"),
            levels=_levels((detail_by_id.get(s["id"]) or {}).get("levels")),
        )
        for s in raw_index
    ]

    industries = [
        Industry(id=i["id"], slug=i["slug"], title_th=i["title"], title_en=i.get("title_en"))
        for i in raw_industries
    ]

    dropped = Counter()
    careers: list[Career] = []
    for c in raw_careers:
        demand = []
        for entry in c.get("skills", []):
            item = SkillDemand(
                skill_id=entry["skill"]["id"],
                count=entry["count"],
                prevalence=entry["percentage"],
            )
            if item.is_degenerate:
                dropped["zero_count"] += 1
                continue
            demand.append(item)
        careers.append(
            Career(
                id=c["id"],
                slug=c["slug"],
                title_th=c["title"],
                industry_slug=c.get("industry_slug", ""),
                description=c.get("description"),
                demand=tuple(demand),
                growth={
                    g["skill"]["id"]: g["growth"]
                    for g in (c.get("skillsGrowth") or [])
                    if g.get("skill")
                },
            )
        )

    report_stub = LoadReport(
        snapshot_date=manifest.get("snapshot_date", root.name),
        api_version=manifest.get("api_version", "unknown"),
        industries=len(industries),
        careers_loaded=len(careers),
        careers_degenerate=sum(1 for c in careers if c.is_degenerate),
        skills_total=len(skills),
        skills_with_levels=sum(1 for s in skills if s.has_levels),
        demand_pairs_kept=sum(len(c.demand) for c in careers),
        demand_pairs_dropped_zero_count=dropped["zero_count"],
        seniority_pairs=0,  # filled below, once pairing has run
    )

    snapshot = Snapshot(industries=industries, careers=careers, skills=skills, report=report_stub)
    # Pairing needs the built indexes, so the count is filled once they exist.
    snapshot.report = replace(report_stub, seniority_pairs=len(snapshot.seniority_pairs))
    return snapshot


@lru_cache(maxsize=1)
def get_snapshot() -> Snapshot:
    """The process-wide snapshot. Loaded once; ~14 MB of JSON."""
    return load_snapshot()
