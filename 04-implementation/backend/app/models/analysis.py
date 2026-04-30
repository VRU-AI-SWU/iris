from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class GapAnalysis(Base):
    __tablename__ = "gap_analyses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"), nullable=False)
    # For programme-to-market: career_path is set; compare_programme_id is null
    # For programme-to-programme: compare_programme_id is set; career_path is null
    career_path: Mapped[str] = mapped_column(String(64), nullable=True)
    compare_programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"), nullable=True)
    scenario: Mapped[str] = mapped_column(String(64), default="core")  # core | core_electives | hypothetical
    status: Mapped[str] = mapped_column(String(50), default="pending")
    celery_task_id: Mapped[str] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    result: Mapped["GapResult"] = relationship(back_populates="analysis", uselist=False, cascade="all, delete-orphan")


class GapResult(Base):
    __tablename__ = "gap_results"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    analysis_id: Mapped[int] = mapped_column(ForeignKey("gap_analyses.id"), nullable=False, unique=True)
    kl_divergence: Mapped[float] = mapped_column(Float, nullable=True)
    cosine_similarity: Mapped[float] = mapped_column(Float, nullable=True)
    # JSON: list of {skill, gap_score, rca_weight, direction: "deficit"|"surplus"|"common"}
    ranked_gaps: Mapped[dict] = mapped_column(JSON, nullable=True)
    # JSON: {common: [...], programme_unique: [...], market_unique: [...]}
    skill_decomposition: Mapped[dict] = mapped_column(JSON, nullable=True)
    # JSON: courses × skills matrix for heatmap
    heatmap_data: Mapped[dict] = mapped_column(JSON, nullable=True)
    narrative_summary: Mapped[str] = mapped_column(Text, nullable=True)
    pdf_path: Mapped[str] = mapped_column(String(512), nullable=True)

    analysis: Mapped["GapAnalysis"] = relationship(back_populates="result")
