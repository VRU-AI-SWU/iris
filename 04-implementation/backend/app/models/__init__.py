from app.models.programme import Programme, Course, CourseSkill
from app.models.job import JobPosting, JobSkill
from app.models.vocab import SkillCluster, SkillToken
from app.models.analysis import GapAnalysis, GapResult

__all__ = [
    "Programme", "Course", "CourseSkill",
    "JobPosting", "JobSkill",
    "SkillCluster", "SkillToken",
    "GapAnalysis", "GapResult",
]
