from datetime import datetime, date
from sqlalchemy import String, Text, ForeignKey, DateTime, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base

# chaiaroon-2025 validated 20-role Thai digital taxonomy
class CareerPath(str, enum.Enum):
    dotnet_dev = "dotnet-dev"
    backend_dev = "backend-dev"
    business_analyst = "business-analyst"
    cloud = "cloud"
    data_analyst = "data-analyst"
    data_engineer = "data-engineer"
    database_admin = "database-admin"
    devops = "devops"
    frontend_dev = "frontend-dev"
    fullstack_dev = "fullstack-dev"
    information_security = "information-security"
    it_support = "it-support"
    java_dev = "java-dev"
    mobile_dev = "mobile-dev"
    network_engineer = "network-engineer"
    project_manager = "project-manager"
    software_engineer = "software-engineer"
    tester = "tester"
    ux_ui_designer = "ux-ui-designer"
    web_developer = "web-developer"


class JobPosting(Base):
    __tablename__ = "job_postings"

    id: Mapped[int] = mapped_column(String(128), primary_key=True)
    source: Mapped[str] = mapped_column(String(64), nullable=False)
    title: Mapped[str] = mapped_column(String(512), nullable=True)
    company: Mapped[str] = mapped_column(String(512), nullable=True)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    requirements: Mapped[str] = mapped_column(Text, nullable=True)
    career_path: Mapped[CareerPath] = mapped_column(Enum(CareerPath), nullable=True)
    posted_date: Mapped[date] = mapped_column(Date, nullable=True)
    scraped_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    skills: Mapped[list["JobSkill"]] = relationship(back_populates="posting", cascade="all, delete-orphan")


class JobSkill(Base):
    __tablename__ = "job_skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    posting_id: Mapped[str] = mapped_column(ForeignKey("job_postings.id"), nullable=False)
    raw_skill: Mapped[str] = mapped_column(String(512), nullable=False)
    cluster_id: Mapped[int] = mapped_column(ForeignKey("skill_clusters.id"), nullable=True)

    posting: Mapped["JobPosting"] = relationship(back_populates="skills")
