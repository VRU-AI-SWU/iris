import logging
import os
from celery_app import celery_app

logger = logging.getLogger(__name__)

REPORT_DIR = "/app/data/reports"


@celery_app.task(bind=True, max_retries=1)
def generate_gap_report(self, analysis_id: int):
    """Generate narrative summary and PDF report for a completed analysis."""
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models.analysis import GapAnalysis
    from pipeline.report_generator import generate_narrative, render_pdf

    db: Session = SessionLocal()
    try:
        analysis = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
        if not analysis or not analysis.result:
            logger.error("Analysis %d has no result", analysis_id)
            return

        result = analysis.result
        ranked_gaps = result.ranked_gaps or []
        top_deficits = [r for r in ranked_gaps if r["direction"] == "deficit"][:5]
        top_surpluses = [r for r in ranked_gaps if r["direction"] == "surplus"][:3]

        narrative = generate_narrative(
            programme_name=analysis.programme.name if hasattr(analysis, "programme") else f"Programme {analysis.programme_id}",
            career_path=analysis.career_path,
            kl_divergence=result.kl_divergence,
            cosine_similarity=result.cosine_similarity,
            top_deficits=top_deficits,
            top_surpluses=top_surpluses,
            skill_decomposition=result.skill_decomposition,
        )
        result.narrative_summary = narrative

        os.makedirs(REPORT_DIR, exist_ok=True)
        pdf_path = os.path.join(REPORT_DIR, f"report_{analysis_id}.pdf")
        render_pdf(
            output_path=pdf_path,
            analysis_id=analysis_id,
            narrative=narrative,
            heatmap_data=result.heatmap_data,
            ranked_gaps=ranked_gaps,
            kl_divergence=result.kl_divergence,
            cosine_similarity=result.cosine_similarity,
        )
        result.pdf_path = pdf_path

        db.commit()
        logger.info("Report generated for analysis %d → %s", analysis_id, pdf_path)

    except Exception as exc:
        db.rollback()
        logger.exception("Report generation failed for analysis %d", analysis_id)
        raise self.retry(exc=exc, countdown=10)
    finally:
        db.close()
