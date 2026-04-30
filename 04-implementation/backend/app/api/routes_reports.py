from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.analysis import GapAnalysis

router = APIRouter()


@router.post("/generate/{analysis_id}", status_code=202)
def generate_report(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Analysis not found")
    if a.status != "completed":
        raise HTTPException(status_code=400, detail="Analysis not yet completed")

    from worker.tasks.report_tasks import generate_gap_report
    task = generate_gap_report.delay(analysis_id)
    return {"task_id": task.id, "status": "queued"}


@router.get("/{analysis_id}")
def get_report(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
    if not a or not a.result:
        raise HTTPException(status_code=404, detail="Report not found")
    return {
        "analysis_id": analysis_id,
        "narrative_summary": a.result.narrative_summary,
        "heatmap_data": a.result.heatmap_data,
        "ranked_gaps": a.result.ranked_gaps,
    }


@router.get("/{analysis_id}/pdf")
def download_pdf(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(GapAnalysis).filter(GapAnalysis.id == analysis_id).first()
    if not a or not a.result or not a.result.pdf_path:
        raise HTTPException(status_code=404, detail="PDF not yet generated")
    return FileResponse(a.result.pdf_path, media_type="application/pdf", filename=f"iris-report-{analysis_id}.pdf")
