from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.job import JobPosting, CareerPath
from app.schemas.job_posting import JobPostingOut, ScrapeRequest, ScrapeStatus

router = APIRouter()


@router.post("/scrape", status_code=202)
def trigger_scrape(req: ScrapeRequest):
    from worker.tasks.job_tasks import scrape_jobs
    task = scrape_jobs.delay(req.career_path, req.sources)
    return {"task_id": task.id, "status": "queued"}


@router.get("/scrape/{task_id}", response_model=ScrapeStatus)
def scrape_status(task_id: str):
    from worker.celery_app import celery_app
    result = celery_app.AsyncResult(task_id)
    return {"task_id": task_id, "status": result.status, "info": str(result.info or "")}


@router.get("/", response_model=list[JobPostingOut])
def list_postings(
    career_path: Optional[CareerPath] = Query(None),
    source: Optional[str] = Query(None),
    limit: int = Query(50, le=500),
    offset: int = Query(0),
    db: Session = Depends(get_db),
):
    q = db.query(JobPosting)
    if career_path:
        q = q.filter(JobPosting.career_path == career_path)
    if source:
        q = q.filter(JobPosting.source == source)
    return q.offset(offset).limit(limit).all()


@router.get("/distributions")
def get_distributions(
    career_path: CareerPath = Query(...),
    db: Session = Depends(get_db),
):
    from worker.pipeline.gap_engine import build_market_distribution
    dist = build_market_distribution(db, career_path)
    return {"career_path": career_path, "distribution": dist}
