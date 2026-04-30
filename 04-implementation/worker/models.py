from sqlalchemy import String, Integer, Float, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from db import Base


class CourseCategory(str, enum.Enum):
    major = "major"
    general = "general"
    elective = "elective"


class Programme(Base):
    __tablename__ = "programmes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    extraction_status: Mapped[str] = mapped_column(String(50), default="pending")
    courses: Mapped[list["Course"]] = relationship(back_populates="programme", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=True)
    name_th: Mapped[str] = mapped_column(String(512), nullable=True)
    name_en: Mapped[str] = mapped_column(String(512), nullable=True)
    credits: Mapped[float] = mapped_column(Float, default=3.0)
    category: Mapped[CourseCategory] = mapped_column(Enum(CourseCategory), default=CourseCategory.major)

    programme: Mapped["Programme"] = relationship(back_populates="courses")
    skills: Mapped[list["CourseSkill"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class CourseSkill(Base):
    __tablename__ = "course_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    raw_skill: Mapped[str] = mapped_column(String(512), nullable=False)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("skill_clusters.id"), nullable=True)

    course: Mapped["Course"] = relationship(back_populates="skills")
