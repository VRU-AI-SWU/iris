import logging
from celery_app import celery_app

logger = logging.getLogger(__name__)

SCRAPER_MAP = {
    "jobthai": "pipeline.scraper.jobthai.JobthaiScraper",
    "jobsdb": "pipeline.scraper.jobsdb.JobsdbScraper",
    "jobbkk": "pipeline.scraper.jobbkk.JobbkkScraper",
    "jobtopgun": "pipeline.scraper.jobtopgun.JobtopgunScraper",
}


@celery_app.task(bind=True, max_retries=2)
def scrape_jobs(self, career_path: str, sources: list[str]):
    """
    Scrape job postings from specified sources for a career path.
    Extracts skills from each posting and stores in DB.
    """
    from importlib import import_module
    from sqlalchemy.orm import Session
    from app.database import SessionLocal
    from app.models.job import JobPosting, JobSkill
    from pipeline.skill_extractor import extract_from_job_posting

    db: Session = SessionLocal()
    total_stored = 0

    try:
        for source_name in sources:
            if source_name not in SCRAPER_MAP:
                logger.warning("Unknown source: %s", source_name)
                continue

            module_path, class_name = SCRAPER_MAP[source_name].rsplit(".", 1)
            module = import_module(module_path)
            scraper_cls = getattr(module, class_name)
            scraper = scraper_cls()

            logger.info("Scraping %s for career_path=%s", source_name, career_path)
            postings = scraper.scrape(career_path)

            for posting_data in postings:
                existing = db.query(JobPosting).filter(JobPosting.id == posting_data["id"]).first()
                if existing:
                    continue

                posting = JobPosting(
                    id=posting_data["id"],
                    source=source_name,
                    title=posting_data.get("title"),
                    company=posting_data.get("company"),
                    description=posting_data.get("description"),
                    requirements=posting_data.get("requirements"),
                    career_path=career_path,
                    posted_date=posting_data.get("posted_date"),
                )
                db.add(posting)
                db.flush()

                skills = extract_from_job_posting(
                    posting_data.get("title", ""),
                    posting_data.get("description", ""),
                    posting_data.get("requirements", ""),
                )
                for skill_text in skills:
                    db.add(JobSkill(posting_id=posting.id, raw_skill=skill_text))

                total_stored += 1

            db.commit()
            logger.info("%s: stored %d new postings", source_name, total_stored)

    except Exception as exc:
        db.rollback()
        logger.exception("Job scraping failed for career_path=%s", career_path)
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()

    return {"career_path": career_path, "total_stored": total_stored}
