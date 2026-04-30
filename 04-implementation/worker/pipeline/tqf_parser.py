"""
TQF (มคอ.2) PDF parser.

Extracts course list, descriptions, credit hours, and course category
(major / general education / free elective) from Thai TQF documents.

TQF structure (consistent across Thai universities):
  - หมวดวิชาเฉพาะ       = major-specific courses    → weight: 1.0
  - หมวดวิชาศึกษาทั่วไป  = general education courses → weight: 0.5
  - หมวดวิชาเลือกเสรี   = free elective courses     → weight: 0.0 (excluded in core scenario)
"""
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

import pdfplumber
import pythainlp

logger = logging.getLogger(__name__)

# Category markers in TQF text
_MAJOR_MARKERS = ["หมวดวิชาเฉพาะ", "วิชาเฉพาะ"]
_GENERAL_MARKERS = ["หมวดวิชาศึกษาทั่วไป", "วิชาศึกษาทั่วไป", "วิชาการศึกษาทั่วไป"]
_ELECTIVE_MARKERS = ["หมวดวิชาเลือกเสรี", "วิชาเลือกเสรี"]

# Thai credit pattern: e.g. "3(3-0-6)" or "3 หน่วยกิต"
_CREDIT_PATTERN = re.compile(r"\b(\d+)\s*(?:\(\d+[-–]\d+[-–]\d+\)|\s*หน่วยกิต)")

# Course code pattern: Thai universities typically use format like "CS101" or "01417101"
_CODE_PATTERN = re.compile(r"\b([A-Z]{2,4}\s?\d{3,6}|\d{7,8})\b")


@dataclass
class ParsedCourse:
    code: str = ""
    name_th: str = ""
    name_en: str = ""
    description_th: str = ""
    description_en: str = ""
    credits: float = 3.0
    category: str = "major"  # major | general | elective


@dataclass
class ParsedProgramme:
    courses: list[ParsedCourse] = field(default_factory=list)
    raw_text: str = ""


def parse_tqf_pdf(pdf_path: str | Path) -> ParsedProgramme:
    """
    Extract all courses and their descriptions from a TQF PDF.
    Returns a ParsedProgramme with a list of ParsedCourse objects.
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"TQF PDF not found: {pdf_path}")

    logger.info("Parsing TQF PDF: %s", path.name)

    full_text = _extract_text(path)
    courses = _extract_courses(full_text)

    logger.info("Extracted %d courses from %s", len(courses), path.name)
    return ParsedProgramme(courses=courses, raw_text=full_text)


def _extract_text(path: Path) -> str:
    """Extract full text from PDF preserving page structure."""
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text(x_tolerance=3, y_tolerance=3)
            if text:
                pages.append(text)
    return "\n\n".join(pages)


def _extract_courses(text: str) -> list[ParsedCourse]:
    """
    Parse course descriptions from TQF full text.

    Strategy:
    1. Split text into sections by category markers
    2. Within each section, locate course description blocks
    3. Extract code, name (Thai + English), credits, description
    """
    courses: list[ParsedCourse] = []

    sections = _split_by_category(text)
    for category, section_text in sections.items():
        section_courses = _parse_course_descriptions(section_text, category)
        courses.extend(section_courses)

    return courses


def _split_by_category(text: str) -> dict[str, str]:
    """
    Split TQF text into sections by course category.
    Returns dict mapping category name to section text.
    """
    sections: dict[str, str] = {}
    lines = text.split("\n")
    current_category = "major"
    current_lines: list[str] = []

    for line in lines:
        line_stripped = line.strip()

        if any(marker in line_stripped for marker in _MAJOR_MARKERS):
            if current_lines:
                sections[current_category] = "\n".join(current_lines)
            current_category = "major"
            current_lines = [line]
        elif any(marker in line_stripped for marker in _GENERAL_MARKERS):
            if current_lines:
                sections[current_category] = "\n".join(current_lines)
            current_category = "general"
            current_lines = [line]
        elif any(marker in line_stripped for marker in _ELECTIVE_MARKERS):
            if current_lines:
                sections[current_category] = "\n".join(current_lines)
            current_category = "elective"
            current_lines = [line]
        else:
            current_lines.append(line)

    if current_lines:
        sections[current_category] = "\n".join(current_lines)

    # Fallback: if no category markers found, treat everything as major
    if not sections:
        sections["major"] = text

    return sections


def _parse_course_descriptions(text: str, category: str) -> list[ParsedCourse]:
    """
    Extract individual course descriptions from a category section.

    TQF course descriptions follow a consistent pattern:
      [course code]  [course name in Thai]  [credits]
      [course name in English]
      [description in Thai and/or English]
    """
    courses: list[ParsedCourse] = []

    # Split on course code boundaries — each code starts a new course block
    # Look for lines that start with a course code pattern
    code_pattern = re.compile(r"^(\d{7,8}|[A-Z]{2,4}\s?\d{3,6})\s+(.+)$", re.MULTILINE)
    matches = list(code_pattern.finditer(text))

    if not matches:
        # Fallback: try to find description blocks by Thai description header keywords
        return _parse_by_description_headers(text, category)

    for i, match in enumerate(matches):
        # Block is from this match to the next match (or end of text)
        block_start = match.start()
        block_end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[block_start:block_end].strip()

        course = _parse_single_course_block(block, category)
        if course.description_th or course.description_en:
            courses.append(course)

    return courses


def _parse_single_course_block(block: str, category: str) -> ParsedCourse:
    """Parse a single course text block into a ParsedCourse."""
    lines = [l.strip() for l in block.split("\n") if l.strip()]
    course = ParsedCourse(category=category)

    if not lines:
        return course

    first_line = lines[0]

    # Extract course code
    code_match = _CODE_PATTERN.search(first_line)
    if code_match:
        course.code = code_match.group(0).replace(" ", "")

    # Extract credits
    credit_match = _CREDIT_PATTERN.search(block)
    if credit_match:
        try:
            course.credits = float(credit_match.group(1))
        except ValueError:
            pass

    # Separate Thai and English text
    thai_lines, english_lines = [], []
    for line in lines[1:]:
        if _is_thai(line):
            thai_lines.append(line)
        elif line.strip():
            english_lines.append(line)

    # First Thai line is usually the course name
    if thai_lines:
        course.name_th = thai_lines[0]
        course.description_th = " ".join(thai_lines[1:])

    # First English line is usually the course name
    if english_lines:
        # Skip lines that look like credit notation
        non_credit_en = [l for l in english_lines if not _CREDIT_PATTERN.match(l)]
        if non_credit_en:
            course.name_en = non_credit_en[0]
            course.description_en = " ".join(non_credit_en[1:])

    return course


def _parse_by_description_headers(text: str, category: str) -> list[ParsedCourse]:
    """
    Fallback parser: split by 'คำอธิบายรายวิชา' (course description) keyword.
    Used when course codes are not in a parseable format.
    """
    courses: list[ParsedCourse] = []
    description_header = "คำอธิบายรายวิชา"
    blocks = text.split(description_header)

    for block in blocks[1:]:  # first block is pre-header text
        block = block.strip()
        if not block:
            continue
        course = ParsedCourse(category=category)
        thai_lines = [l.strip() for l in block.split("\n") if l.strip() and _is_thai(l)]
        course.description_th = " ".join(thai_lines[:10])  # cap at 10 lines
        if course.description_th:
            courses.append(course)

    return courses


def _is_thai(text: str) -> bool:
    """Return True if the text contains a meaningful proportion of Thai characters."""
    if not text:
        return False
    thai_chars = sum(1 for c in text if "฀" <= c <= "๿")
    return thai_chars / max(len(text), 1) > 0.2


def preprocess_thai(text: str) -> str:
    """
    Tokenise and clean Thai text using PyThaiNLP.
    Used to prepare course description text before LLM extraction.
    """
    if not text or not _is_thai(text):
        return text
    tokens = pythainlp.tokenize.word_tokenize(text, engine="newmm", keep_whitespace=False)
    stopwords = set(pythainlp.corpus.thai_stopwords())
    cleaned = [t for t in tokens if t not in stopwords and len(t) > 1]
    return " ".join(cleaned)
