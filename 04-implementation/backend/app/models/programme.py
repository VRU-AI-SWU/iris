from datetime import datetime
from sqlalchemy import String, Integer, Float, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class CourseCategory(str, enum.Enum):
    major = "major"           # หมวดวิชาเฉพาะ
    general = "general"       # หมวดวิชาศึกษาทั่วไป
    elective = "elective"     # หมวดวิชาเลือกเสรี


class Programme(Base):
    __tablename__ = "programmes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    university: Mapped[str] = mapped_column(String(255), nullable=False)
    degree: Mapped[str] = mapped_column(String(100), nullable=True)
    tqf_filename: Mapped[str] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    extraction_status: Mapped[str] = mapped_column(String(50), default="pending")

    courses: Mapped[list["Course"]] = relationship(back_populates="programme", cascade="all, delete-orphan")


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    programme_id: Mapped[int] = mapped_column(ForeignKey("programmes.id"), nullable=False)
    code: Mapped[str] = mapped_column(String(20), nullable=True)
    name_th: Mapped[str] = mapped_column(String(512), nullable=True)
    name_en: Mapped[str] = mapped_column(String(512), nullable=True)
    description_th: Mapped[str] = mapped_column(Text, nullable=True)
    description_en: Mapped[str] = mapped_column(Text, nullable=True)
    credits: Mapped[float] = mapped_column(Float, default=3.0)
    category: Mapped[CourseCategory] = mapped_column(Enum(CourseCategory), default=CourseCategory.major)

    programme: Mapped["Programme"] = relationship(back_populates="courses")
    skills: Mapped[list["CourseSkill"]] = relationship(back_populates="course", cascade="all, delete-orphan")

    @property
    def credit_weight(self) -> float:
        weights = {CourseCategory.major: 1.0, CourseCategory.general: 0.5, CourseCategory.elective: 0.0}
        return self.credits * weights.get(self.category, 1.0)


class CourseSkill(Base):
    __tablename__ = "course_skills"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"), nullable=False)
    raw_skill: Mapped[str] = mapped_column(String(512), nullable=False)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("skill_clusters.id"), nullable=True)

    course: Mapped["Course"] = relationship(back_populates="skills")
