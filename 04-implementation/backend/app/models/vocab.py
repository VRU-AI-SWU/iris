from sqlalchemy import String, Integer, Text, Float, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class SkillCluster(Base):
    """Canonical skill in the emergent vocabulary."""
    __tablename__ = "skill_clusters"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    label: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    version: Mapped[int] = mapped_column(Integer, default=1)


class SkillToken(Base):
    """Raw extracted skill term mapped to a cluster."""
    __tablename__ = "skill_tokens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    raw_text: Mapped[str] = mapped_column(String(512), nullable=False)
    cluster_id: Mapped[int] = mapped_column(Integer, nullable=True)
    embedding_json: Mapped[str] = mapped_column(Text, nullable=True)  # JSON float array
