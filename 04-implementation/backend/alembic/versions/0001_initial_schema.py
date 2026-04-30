"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-30
"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "programmes",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("university", sa.String(255), nullable=False),
        sa.Column("degree", sa.String(100), nullable=True),
        sa.Column("tqf_filename", sa.String(512), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("extraction_status", sa.String(50), nullable=False, server_default="pending"),
    )

    op.create_table(
        "skill_clusters",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("label", sa.String(512), nullable=False, unique=True),
        sa.Column("version", sa.Integer, nullable=False, server_default="1"),
    )

    op.create_table(
        "skill_tokens",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("raw_text", sa.String(512), nullable=False),
        sa.Column("cluster_id", sa.Integer, sa.ForeignKey("skill_clusters.id"), nullable=True),
        sa.Column("embedding_json", sa.Text, nullable=True),
    )

    op.create_table(
        "courses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("programme_id", sa.Integer, sa.ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("code", sa.String(20), nullable=True),
        sa.Column("name_th", sa.String(512), nullable=True),
        sa.Column("name_en", sa.String(512), nullable=True),
        sa.Column("description_th", sa.Text, nullable=True),
        sa.Column("description_en", sa.Text, nullable=True),
        sa.Column("credits", sa.Float, nullable=False, server_default="3.0"),
        sa.Column("category", sa.String(20), nullable=False, server_default="major"),
    )

    op.create_table(
        "course_skills",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("course_id", sa.Integer, sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_skill", sa.String(512), nullable=False),
        sa.Column("cluster_id", sa.Integer, sa.ForeignKey("skill_clusters.id"), nullable=True),
    )

    op.create_table(
        "job_postings",
        sa.Column("id", sa.String(128), primary_key=True),
        sa.Column("source", sa.String(64), nullable=False),
        sa.Column("title", sa.String(512), nullable=True),
        sa.Column("company", sa.String(512), nullable=True),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("requirements", sa.Text, nullable=True),
        sa.Column("career_path", sa.String(64), nullable=True),
        sa.Column("posted_date", sa.Date, nullable=True),
        sa.Column("scraped_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
    )

    op.create_table(
        "job_skills",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("posting_id", sa.String(128), sa.ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("raw_skill", sa.String(512), nullable=False),
        sa.Column("cluster_id", sa.Integer, sa.ForeignKey("skill_clusters.id"), nullable=True),
    )

    op.create_table(
        "gap_analyses",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("programme_id", sa.Integer, sa.ForeignKey("programmes.id", ondelete="CASCADE"), nullable=False),
        sa.Column("career_path", sa.String(64), nullable=True),
        sa.Column("compare_programme_id", sa.Integer, sa.ForeignKey("programmes.id"), nullable=True),
        sa.Column("scenario", sa.String(64), nullable=False, server_default="core"),
        sa.Column("status", sa.String(50), nullable=False, server_default="pending"),
        sa.Column("celery_task_id", sa.String(255), nullable=True),
        sa.Column("created_at", sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column("completed_at", sa.DateTime, nullable=True),
    )

    op.create_table(
        "gap_results",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("analysis_id", sa.Integer, sa.ForeignKey("gap_analyses.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("kl_divergence", sa.Float, nullable=True),
        sa.Column("cosine_similarity", sa.Float, nullable=True),
        sa.Column("ranked_gaps", sa.JSON, nullable=True),
        sa.Column("skill_decomposition", sa.JSON, nullable=True),
        sa.Column("heatmap_data", sa.JSON, nullable=True),
        sa.Column("narrative_summary", sa.Text, nullable=True),
        sa.Column("pdf_path", sa.String(512), nullable=True),
    )

    # Indexes for common query patterns
    op.create_index("ix_courses_programme_id", "courses", ["programme_id"])
    op.create_index("ix_course_skills_course_id", "course_skills", ["course_id"])
    op.create_index("ix_course_skills_cluster_id", "course_skills", ["cluster_id"])
    op.create_index("ix_job_postings_career_path", "job_postings", ["career_path"])
    op.create_index("ix_job_postings_scraped_at", "job_postings", ["scraped_at"])
    op.create_index("ix_job_skills_posting_id", "job_skills", ["posting_id"])
    op.create_index("ix_job_skills_cluster_id", "job_skills", ["cluster_id"])
    op.create_index("ix_gap_analyses_programme_id", "gap_analyses", ["programme_id"])


def downgrade() -> None:
    op.drop_table("gap_results")
    op.drop_table("gap_analyses")
    op.drop_table("job_skills")
    op.drop_table("job_postings")
    op.drop_table("course_skills")
    op.drop_table("courses")
    op.drop_table("skill_tokens")
    op.drop_table("skill_clusters")
    op.drop_table("programmes")
