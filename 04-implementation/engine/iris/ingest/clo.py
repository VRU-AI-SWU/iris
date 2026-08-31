"""Extract course learning outcomes (CLOs) and the verbs that carry their level.

An outcome-based มคอ.2 states, per course, what a student will be able to *do* —
`3. ออกแบบฐานข้อมูล`, `1. อธิบายขั้นตอนการพัฒนาระบบ`. The leading verb is the
signal: `อธิบาย` (explain) sits low on a cognitive scale, `ออกแบบ` (design) sits
high. This is the second of the three level-inference sources, alongside the
● ○ responsibility matrix and position in the curriculum.

It matters because of a measured result rather than an intuition.
[[kumar-2025-bloom-taxonomy-classification]] compared model families on the same
Bloom's-classification data and found **SVM over verb features at 94 % against
0.72–0.73 for zero-shot LLMs** — more than twenty points. Asking a language model
what level a course teaches at is the weaker method; reading the verb the
programme itself chose is the stronger one.

**Layout.** These outcomes live in a table whose columns are named in its own
header — `ชุดรายวิชา | คำอธิบายรายวิชา | CLOs | MLOs | ELOs` — so the column
boundaries are read from the document rather than assumed. SWU prints it sideways
at rotation 90. A CLO belongs to the course whose code sits in the leftmost column
of the same row band.

Only outcome-based documents carry per-course CLOs at all. Of the five in the
corpus, SWU states them fully and PSU partially; CMU, SU and KU do not, and the
extractor reports their absence rather than inventing something.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

#: Header labels that name the columns of the outcome table.
COLUMN_HEADERS = {
    "course": re.compile(r"ชุดรายวิชา|ชุดวิชา|รหัสวิชา"),
    "description": re.compile(r"คำอธิบายรายวิชา"),
    "clo": re.compile(r"CLOs?|ผลการเรียนรู้ที่คาดหวังรายวิชา|ผลลัพธ์การเรียนรู้.{0,8}รายวิชา"),
    "mlo": re.compile(r"MLOs?|ผลการเรียนรู้ที่คาดหวังของชุดวิชา"),
    "elo": re.compile(r"ELOs?|PLOs?"),
}

#: A numbered outcome statement: `3. ออกแบบฐานข้อมูล`.
NUMBERED_OUTCOME = re.compile(r"^\s*(\d{1,2})\s*[.)]\s*(.+)$")

#: Course codes in any of the corpus's five conventions.
COURSE_CODE = re.compile(r"[ก-ฮ]{2,4}\s?\d{3}|\b\d{6,8}\b|\d{3}[-\s]\d{2,3}")

#: How close two lines must be, along the row axis, to belong to the same row.
ROW_BAND = 26.0

#: Thai verbs that open a learning outcome, grouped by the cognitive demand they
#: signal. The grouping is **evidence for level inference, not a level** — the
#: mapping onto the national standard's `พื้นฐาน / ปานกลาง / สูง` is an open
#: question measured at the Sprint 4 gate, not decided here.
OUTCOME_VERBS: dict[str, tuple[str, ...]] = {
    "recall": ("บอก", "ระบุ", "จำ", "แสดง", "เขียนรายการ"),
    "understand": ("อธิบาย", "สรุป", "จำแนก", "เปรียบเทียบ", "ยกตัวอย่าง", "แปลความ"),
    "apply": ("ใช้", "ประยุกต์", "คำนวณ", "ดำเนินการ", "สาธิต", "ปฏิบัติ", "เขียนโปรแกรม"),
    "analyse": ("วิเคราะห์", "ตรวจสอบ", "ทดสอบ", "แยกแยะ", "วินิจฉัย"),
    "evaluate": ("ประเมิน", "ตัดสิน", "วิพากษ์", "เลือก", "ตรวจประเมิน"),
    "create": ("ออกแบบ", "พัฒนา", "สร้าง", "วางแผน", "ผลิต", "ประดิษฐ์", "บูรณาการ"),
}

#: Longest verbs first, so `เขียนโปรแกรม` is not matched as `เขียน`.
_VERB_LOOKUP: tuple[tuple[str, str], ...] = tuple(
    sorted(
        ((verb, band) for band, verbs in OUTCOME_VERBS.items() for verb in verbs),
        key=lambda pair: -len(pair[0]),
    )
)


@dataclass(frozen=True, slots=True)
class LearningOutcome:
    """One CLO, with the verb that signals its cognitive demand."""

    course_code: str | None
    number: int
    text: str
    verb: str | None = None
    verb_band: str | None = None
    page: int | None = None

    @property
    def has_verb(self) -> bool:
        return self.verb is not None


@dataclass(frozen=True, slots=True)
class CLOReport:
    pages: tuple[int, ...]
    outcomes: int
    with_course: int
    with_verb: int
    courses: int
    verb_bands: dict[str, int] = field(default_factory=dict)
    rotation: int = 0

    def summary(self) -> str:
        if not self.outcomes:
            return "no per-course learning outcomes found"
        bands = ", ".join(f"{b}={n}" for b, n in sorted(self.verb_bands.items()))
        return (
            f"{self.outcomes} learning outcomes ({self.with_course} tied to a course "
            f"across {self.courses} courses, {self.with_verb} with a leading verb) "
            f"on pages {', '.join(str(p) for p in self.pages)} "
            f"(rotation {self.rotation}; {bands})"
        )


def classify_verb(text: str) -> tuple[str | None, str | None]:
    """The leading action verb of an outcome, and the band it belongs to."""
    head = text.lstrip(" \t·-–")
    for verb, band in _VERB_LOOKUP:
        if head.startswith(verb):
            return verb, band
    # Some outcomes open with a modal — `สามารถออกแบบ…`.
    for prefix in ("สามารถ", "มีความสามารถในการ", "สามารถที่จะ"):
        if head.startswith(prefix):
            return classify_verb(head[len(prefix) :])
    return None, None


def _reading_axes(bbox, rotation: int, page_height: float) -> tuple[float, float]:
    """Map a bbox centre onto (across, down) in reading order."""
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    if rotation == 90:
        return page_height - y, x
    if rotation == 270:
        return y, -x
    return x, y


def _column_bounds(header: list[tuple[float, str]]) -> dict[str, tuple[float, float]]:
    """Turn header labels into `(start, end)` spans along the reading axis.

    A column runs from its own header to the next one, which is why the header
    row is what defines the table rather than any fixed geometry.
    """
    found: list[tuple[float, str]] = []
    for across, text in sorted(header):
        for name, pattern in COLUMN_HEADERS.items():
            if pattern.search(text) and name not in {n for _, n in found}:
                found.append((across, name))
                break
    bounds: dict[str, tuple[float, float]] = {}
    for index, (across, name) in enumerate(found):
        end = found[index + 1][0] if index + 1 < len(found) else float("inf")
        bounds[name] = (across - 20, end - 20)
    return bounds


def extract_learning_outcomes(
    path: Path | str,
) -> tuple[list[LearningOutcome], CLOReport]:
    """Read per-course learning outcomes out of an outcome-based มคอ.2.

    Reads through `repaired_lines`, so the verbs arrive as `ประยุกต์` rather than
    as `ประยุกต=`. Reading spans raw here cost 44 % of the verb matches until the
    repair was wired in.
    """
    import pymupdf

    from iris.ingest.pdf import repaired_lines

    outcomes: list[LearningOutcome] = []
    pages_used: list[int] = []
    courses: set[str] = set()
    rotation = 0

    all_lines, _ = repaired_lines(path)
    by_page: dict[int, list[tuple[float, float, str]]] = {}
    for line in all_lines:
        by_page.setdefault(line.page, []).append((line.across, line.down, line.text))

    with pymupdf.open(path) as doc:
        for number, page in enumerate(doc):
            lines = by_page.get(number + 1, [])
            if not lines:
                continue

            # The header row names the columns; without it this is not the table.
            header_row = min(lines, key=lambda entry: entry[1])[1]
            header = [(a, t) for a, d, t in lines if abs(d - header_row) < ROW_BAND]
            bounds = _column_bounds(header)
            if "clo" not in bounds or "course" not in bounds:
                continue

            clo_start, clo_end = bounds["clo"]
            course_start, course_end = bounds["course"]

            course_rows = sorted(
                (d, t)
                for a, d, t in lines
                if course_start <= a < course_end and COURSE_CODE.search(t)
            )
            clo_lines = [
                (d, t)
                for a, d, t in lines
                if clo_start <= a < clo_end and NUMBERED_OUTCOME.match(t)
            ]
            if not clo_lines:
                continue

            pages_used.append(number + 1)
            if page.rotation:
                rotation = page.rotation

            for down, text in clo_lines:
                match = NUMBERED_OUTCOME.match(text)
                if not match:
                    continue
                body = " ".join(match.group(2).split())
                # The course whose code sits at or above this outcome's row.
                above = [c for c in course_rows if c[0] <= down + ROW_BAND]
                code = None
                if above:
                    found = COURSE_CODE.search(above[-1][1])
                    if found:
                        code = " ".join(found.group().split())
                        courses.add(code)
                verb, band = classify_verb(body)
                outcomes.append(
                    LearningOutcome(
                        course_code=code,
                        number=int(match.group(1)),
                        text=body,
                        verb=verb,
                        verb_band=band,
                        page=number + 1,
                    )
                )

    bands: dict[str, int] = {}
    for outcome in outcomes:
        if outcome.verb_band:
            bands[outcome.verb_band] = bands.get(outcome.verb_band, 0) + 1

    return outcomes, CLOReport(
        pages=tuple(sorted(set(pages_used))),
        outcomes=len(outcomes),
        with_course=sum(1 for o in outcomes if o.course_code),
        with_verb=sum(1 for o in outcomes if o.has_verb),
        courses=len(courses),
        verb_bands=bands,
        rotation=rotation,
    )
