from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class ProgrammeCreate(BaseModel):
    name: str
    university: str


class CourseOut(BaseModel):
    id: int
    code: Optional[str]
    name_th: Optional[str]
    name_en: Optional[str]
    credits: float
    category: str

    model_config = {"from_attributes": True}


class ProgrammeOut(BaseModel):
    id: int
    name: str
    university: str
    tqf_filename: Optional[str]
    extraction_status: str
    created_at: datetime
    courses: list[CourseOut] = []

    model_config = {"from_attributes": True}
