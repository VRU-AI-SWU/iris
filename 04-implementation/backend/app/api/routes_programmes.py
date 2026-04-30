from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
import shutil, os, uuid

from app.database import get_db
from app.models.programme import Programme
from app.schemas.programme import ProgrammeCreate, ProgrammeOut

router = APIRouter()

UPLOAD_DIR = "/app/data/tqf"


@router.post("/", response_model=ProgrammeOut, status_code=201)
async def upload_programme(
    name: str,
    university: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files accepted")

    os.makedirs(UPLOAD_DIR, exist_ok=True)
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)

    programme = Programme(name=name, university=university, tqf_filename=filename)
    db.add(programme)
    db.commit()
    db.refresh(programme)

    # Enqueue extraction task
    from worker.tasks.tqf_tasks import extract_tqf
    extract_tqf.delay(programme.id, filepath)

    return programme


@router.get("/", response_model=list[ProgrammeOut])
def list_programmes(db: Session = Depends(get_db)):
    return db.query(Programme).all()


@router.get("/{programme_id}", response_model=ProgrammeOut)
def get_programme(programme_id: int, db: Session = Depends(get_db)):
    p = db.query(Programme).filter(Programme.id == programme_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Programme not found")
    return p


@router.delete("/{programme_id}", status_code=204)
def delete_programme(programme_id: int, db: Session = Depends(get_db)):
    p = db.query(Programme).filter(Programme.id == programme_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Programme not found")
    db.delete(p)
    db.commit()
