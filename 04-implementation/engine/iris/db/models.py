"""Persistent schema.

Generic SQLAlchemy types throughout, so the same models run on SQLite during
ingestion and evaluation work and on PostgreSQL in production. Nothing here uses
a PostgreSQL-specific column type.

The schema carries three commitments from the solution design:

- **Provenance end to end.** A link points to a course, a course points to a page,
  and a programme records how its text was extracted.
- **Levels are curriculum-side only.** `CourseSkillLink.level_ordinal` exists;
  there is no demanded-level column anywhere, because the demand side has none.
- **Zero links is an outcome, not a gap.** `Course.linked_at` distinguishes
  *processed and found nothing* from *not yet processed*.
"""

from __future__ import annotations

import enum
from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def _now() -> datetime:
    return datetime.now(UTC)


class Base(DeclarativeBase):
    pass


# ── Enumerations ────────────────────────────────────────────────────────────


class ExtractionMethod(enum.StrEnum):
    """How a document's text was obtained — carried into every report.

    A vision extraction is a model output, not a faithful reading, so anything
    traced back to it must say so.
    """

    NATIVE = "native"  # clean text layer
    REPAIRED = "repaired"  # deterministic glyph repair applied
    VISION = "vision"  # re-extracted with a vision-language model


class CourseCategory(enum.StrEnum):
    GENERAL_EDUCATION = "general-education"
    CORE = "core"
    MAJOR_REQUIRED = "major-required"
    MAJOR_ELECTIVE = "major-elective"
    FREE_ELECTIVE = "free-elective"
    UNKNOWN = "unknown"


class LinkStatus(enum.StrEnum):
    PROPOSED = "proposed"  # model output, not yet reviewed
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    LEVEL_ADJUSTED = "level-adjusted"


class ModelProvider(enum.StrEnum):
    """Where inference ran. Pinned per analysis run — never switched mid-run.

    A programme whose courses were linked by two different models is not a
    reproducible analysis, so quota exhaustion fails the run and requeues rather
    than falling back in place.
    """

    LOCAL = "local"  # OpenAI-compatible endpoint on gpu-linux-server
    WORKERS_AI = "workers-ai"  # Cloudflare Workers AI


class JobState(enum.StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


# ── Curriculum ──────────────────────────────────────────────────────────────


class Programme(Base):
    __tablename__ = "programme"

    id: Mapped[int] = mapped_column(primary_key=True)
    name_th: Mapped[str] = mapped_column(String(300))
    name_en: Mapped[str | None] = mapped_column(String(300))
    university: Mapped[str] = mapped_column(String(200))
    year_be: Mapped[int | None] = mapped_column(Integer)  # พ.ศ. of the revision

    source_filename: Mapped[str] = mapped_column(String(500))
    source_pages: Mapped[int | None] = mapped_column(Integer)
    extraction_method: Mapped[ExtractionMethod] = mapped_column(Enum(ExtractionMethod))
    #: Thai combining marks per 1,000 Thai characters, after any repair.
    #: The integrity-gate statistic; ~171 is the clean-document baseline.
    mark_rate: Mapped[float | None] = mapped_column(Float)
    integrity_report: Mapped[dict | None] = mapped_column(JSON)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    courses: Mapped[list[Course]] = relationship(
        back_populates="programme", cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("university", "name_th", "year_be", name="uq_programme_identity"),
    )


class Course(Base):
    __tablename__ = "course"

    id: Mapped[int] = mapped_column(primary_key=True)
    programme_id: Mapped[int] = mapped_column(
        ForeignKey("programme.id", ondelete="CASCADE"), index=True
    )

    code: Mapped[str] = mapped_column(String(20))
    title_th: Mapped[str] = mapped_column(String(300))
    title_en: Mapped[str | None] = mapped_column(String(300))
    credits: Mapped[float | None] = mapped_column(Float)
    credit_spec: Mapped[str | None] = mapped_column(String(40))  # e.g. "3(2-2-5)"
    category: Mapped[CourseCategory] = mapped_column(
        Enum(CourseCategory), default=CourseCategory.UNKNOWN
    )
    year_of_study: Mapped[int | None] = mapped_column(Integer)

    description_th: Mapped[str | None] = mapped_column(Text)
    description_en: Mapped[str | None] = mapped_column(Text)
    #: Course learning outcomes, where the document states them per course.
    clos: Mapped[list | None] = mapped_column(JSON)
    #: Curriculum-map marks: [{"outcome": "2.1", "responsibility": "primary"}, …]
    responsibility_map: Mapped[list | None] = mapped_column(JSON)

    source_page: Mapped[int | None] = mapped_column(Integer)

    #: Set when linking has run. NULL means *not yet processed*; set with no
    #: links means *processed and this course develops nothing in the standard*,
    #: which is a valid outcome for general-education courses.
    linked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    programme: Mapped[Programme] = relationship(back_populates="courses")
    links: Mapped[list[CourseSkillLink]] = relationship(
        back_populates="course", cascade="all, delete-orphan"
    )

    __table_args__ = (UniqueConstraint("programme_id", "code", name="uq_course_code"),)


class CourseSkillLink(Base):
    """One course → one national skill, at an inferred level, with evidence."""

    __tablename__ = "course_skill_link"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), index=True)

    #: National vocabulary skill id. Not a foreign key: the vocabulary is
    #: snapshot reference data on disk, not a table.
    skill_id: Mapped[str] = mapped_column(String(40), index=True)
    snapshot_date: Mapped[str] = mapped_column(String(10))

    #: 0 foundational · 1 intermediate · 2 advanced. Curriculum-side only —
    #: there is deliberately no demanded-level column anywhere in this schema.
    level_ordinal: Mapped[int | None] = mapped_column(Integer)
    #: Per-source level evidence and any disagreement between sources, e.g.
    #: {"clo": 2, "responsibility_map": 2, "position": 1, "agree": false}
    level_sources: Mapped[dict | None] = mapped_column(JSON)

    #: The span of course text that justifies this link.
    evidence_span: Mapped[str | None] = mapped_column(Text)
    evidence_channel: Mapped[str | None] = mapped_column(String(10))  # th | en
    retrieval_rank: Mapped[int | None] = mapped_column(Integer)
    confidence: Mapped[float | None] = mapped_column(Float)
    #: Whether the Thai and English channels agreed, where both exist.
    channels_agree: Mapped[bool | None] = mapped_column()

    status: Mapped[LinkStatus] = mapped_column(Enum(LinkStatus), default=LinkStatus.PROPOSED)
    reviewed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    reviewed_by: Mapped[str | None] = mapped_column(String(200))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    course: Mapped[Course] = relationship(back_populates="links")

    __table_args__ = (
        UniqueConstraint("course_id", "skill_id", name="uq_course_skill"),
        CheckConstraint(
            "level_ordinal IS NULL OR level_ordinal BETWEEN 0 AND 2",
            name="ck_level_ordinal_range",
        ),
        Index("ix_link_status", "status"),
    )


class OutOfVocabularySkill(Base):
    """A capability a course develops that the national vocabulary does not name.

    Recorded, never scored. Accumulated across programmes this becomes a coverage
    report back to สป.อว./KMITL on what the standard does not yet contain.
    """

    __tablename__ = "out_of_vocabulary_skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("course.id", ondelete="CASCADE"), index=True)
    term: Mapped[str] = mapped_column(String(300))
    evidence_span: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


# ── Analysis ────────────────────────────────────────────────────────────────


class AnalysisRun(Base):
    """One programme measured against one career, under one pinned snapshot."""

    __tablename__ = "analysis_run"

    id: Mapped[int] = mapped_column(primary_key=True)
    programme_id: Mapped[int] = mapped_column(
        ForeignKey("programme.id", ondelete="CASCADE"), index=True
    )
    career_slug: Mapped[str] = mapped_column(String(120))
    snapshot_date: Mapped[str] = mapped_column(String(10))

    #: Provider, model and prompt identity — required to reproduce the run.
    #: Pinned for the whole run; a quota exhaustion requeues rather than switches.
    provider: Mapped[ModelProvider | None] = mapped_column(Enum(ModelProvider))
    extraction_model: Mapped[str | None] = mapped_column(String(200))
    embedding_model: Mapped[str | None] = mapped_column(String(200))

    #: True only when every link on the programme has been reviewed. A comparison
    #: may not mix reviewed and unreviewed profiles.
    links_reviewed: Mapped[bool] = mapped_column(default=False)

    results: Mapped[dict | None] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)


class Job(Base):
    """A unit of long-running work. A table and a worker, not a queue server."""

    __tablename__ = "job"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(40), index=True)
    state: Mapped[JobState] = mapped_column(Enum(JobState), default=JobState.QUEUED, index=True)
    payload: Mapped[dict | None] = mapped_column(JSON)
    progress: Mapped[dict | None] = mapped_column(JSON)  # e.g. {"done": 34, "total": 78}
    error: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    started_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
