import logging
from celery_app import celery_app
from pipeline.tqf_parser import parse_tqf_pdf
from pipeline.skill_extractor import batch_extract_from_courses

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=2)
def extract_tqf(self, programme_id: int, pdf_path: str):
    """Parse TQF PDF → extract skills → store in DB."""
    from sqlalchemy.orm import Session
    from db import SessionLocal
    from models import Programme, Course, CourseSkill

    logger.info("Starting TQF extraction for programme %d: %s", programme_id, pdf_path)

    db: Session = SessionLocal()
    try:
        programme = db.query(Programme).filter(Programme.id == programme_id).first()
        if not programme:
            logger.error("Programme %d not found", programme_id)
            return

        programme.extraction_status = "running"
        db.commit()

        parsed = parse_tqf_pdf(pdf_path)
        skill_sets = batch_extract_from_courses(parsed.courses)

        for cs in skill_sets:
            course = Course(
                programme_id=programme_id,
                code=cs.course_code,
                name_th=cs.course_name_th,
                name_en=cs.course_name_en,
                category=cs.category,
                credits=cs.credits,
            )
            db.add(course)
            db.flush()

            for skill_text in cs.skills:
                db.add(CourseSkill(course_id=course.id, raw_skill=skill_text))

        programme.extraction_status = "completed"
        db.commit()
        logger.info("TQF extraction complete for programme %d — %d courses", programme_id, len(skill_sets))

    except Exception as exc:
        db.rollback()
        programme = db.query(Programme).filter(Programme.id == programme_id).first()
        if programme:
            programme.extraction_status = "failed"
            db.commit()
        logger.exception("TQF extraction failed for programme %d", programme_id)
        raise self.retry(exc=exc, countdown=30)
    finally:
        db.close()
