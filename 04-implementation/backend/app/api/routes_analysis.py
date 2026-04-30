from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.analysis import GapAnalysis
from app.schemas.gap_analysis import AnalysisRequest, AnalysisOut, AnalysisStatus

router = APIRouter()


@router.post("/run", response_model=AnalysisOut, status_code=202)
def run_analysis(req: AnalysisRequest, db: Session = Depends(get_db)):
    analysis = GapAnalysis(
        programme_id=req.programme_id,
        career_path=req.career_path,
        compare_programme_id=req.compare_programme_id,
        scenario=req.scenario,
    )
    db.add(analysis)
    db.commit()
    db.refresh(analysis)

    from worker.tasks.analysis_tasks import run_gap_analysis
    task = run_gap_analysis.delay(analysis.id)
    analysis.celery_task_id = task.id
    db.commit()

    return analysis


@router.get("/{analysis_id}", response_model=AnalysisOut)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return a


@router.get("/{analysis_id}/status", response_model=AnalysisStatus)
def analysis_status(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return {"analysis_id": analysis_id, "status": a.status, "celery_task_id": a.celery_task_id}


@router.get("/", response_model=list[AnalysisOut])
def list_analyses(db: Session = Depends(get_db)):
    return db.query(GapAnalysis).order_by(GapAnalysis.created_at.desc()).all()
