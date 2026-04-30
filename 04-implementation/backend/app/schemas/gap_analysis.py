from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class AnalysisRequest(BaseModel):
    programme_id: int
    # Programme-to-market: set career_path
    career_path: Optional[str] = None
    # Programme-to-programme: set compare_programme_id
    compare_programme_id: Optional[int] = None
    scenario: str = "core"  # core | core_electives | hypothetical


class AnalysisStatus(BaseModel):
    analysis_id: int
    status: str
    celery_task_id: Optional[str]


class AnalysisOut(BaseModel):
    id: int
    programme_id: int
    career_path: Optional[str]
    compare_programme_id: Optional[int]
    scenario: str
    status: str
    celery_task_id: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    model_config = {"from_attributes": True}
