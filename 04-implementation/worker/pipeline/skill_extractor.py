"""
Skill extraction pipeline.

Extracts raw skill terms from course descriptions and job posting text
using gemma-4-31b-it via zero-shot prompting. Handles both Thai and
bilingual (Thai + English) text.
"""
import logging
from dataclasses import dataclass

from pipeline.llm_client import extract_skills
from pipeline.tqf_parser import ParsedCourse, preprocess_thai

logger = logging.getLogger(__name__)


@dataclass
class CourseSkillSet:
    course_code: str
    course_name_th: str
    course_name_en: str
    category: str
    credits: float
    skills: list[str]


def extract_from_course(course: ParsedCourse) -> CourseSkillSet:
    """
    Extract skill terms from a single TQF course.
    Uses bilingual description if available; falls back to Thai only.
    """
    text_parts = []

    # Prefer bilingual input — more vocabulary surface area for the LLM
    if course.description_en:
        text_parts.append(course.description_en)
    if course.description_th:
        preprocessed = preprocess_thai(course.description_th)
        text_parts.append(preprocessed)

    # Add course name as additional signal
    if course.name_en:
        text_parts.insert(0, course.name_en)
    elif course.name_th:
        text_parts.insert(0, course.name_th)

    combined = "\n".join(text_parts).strip()
    if not combined:
        logger.warning("Course %s has no description text", course.code or "(no code)")
        return CourseSkillSet(
            course_code=course.code,
            course_name_th=course.name_th,
            course_name_en=course.name_en,
            category=course.category,
            credits=course.credits,
            skills=[],
        )

    logger.debug("Extracting skills from course %s (%d chars)", course.code, len(combined))
    skills = extract_skills(combined)
    logger.info("Course %s → %d skills extracted", course.code or course.name_en, len(skills))

    return CourseSkillSet(
        course_code=course.code,
        course_name_th=course.name_th,
        course_name_en=course.name_en,
        category=course.category,
        credits=course.credits,
        skills=skills,
    )


def extract_from_job_posting(title: str, description: str, requirements: str) -> list[str]:
    """
    Extract skill terms from a job posting.
    Concatenates title + requirements (primary signal) + description (secondary).
    """
    parts = []
    if title:
        parts.append(f"Job title: {title}")
    if requirements:
        parts.append(requirements)
    if description:
        # Trim description to avoid exceeding context — first 500 chars
        parts.append(description[:500])

    text = "\n".join(parts).strip()
    if not text:
        return []

    skills = extract_skills(text)
    logger.debug("Job posting '%s' → %d skills", title or "(no title)", len(skills))
    return skills


def batch_extract_from_courses(courses: list[ParsedCourse]) -> list[CourseSkillSet]:
    """Extract skills from all courses in a programme."""
    results = []
    for course in courses:
        result = extract_from_course(course)
        results.append(result)
    return results
