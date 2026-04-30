from datetime import datetime, date
from pydantic import BaseModel
from typing import Optional


class ScrapeRequest(BaseModel):
    career_path: str
    sources: list[str] = ["jobthai", "jobsdb", "jobbkk", "jobtopgun"]


class ScrapeStatus(BaseModel):
    task_id: str
    status: str
    info: str = ""


class JobPostingOut(BaseModel):
    id: str
    source: str
    title: Optional[str]
    company: Optional[str]
    career_path: Optional[str]
    posted_date: Optional[date]
    scraped_at: datetime

    model_config = {"from_attributes": True}
