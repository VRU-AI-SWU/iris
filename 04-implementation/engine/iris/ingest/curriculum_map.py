"""Read the TQF curriculum-responsibility matrix.

Every มคอ.2 must publish **แผนที่แสดงการกระจายความรับผิดชอบมาตรฐานผลการเรียนรู้จาก
หลักสูตรสู่รายวิชา** — a grid marking, for each course against each programme
learning outcome, whether the course carries *ความรับผิดชอบหลัก* (primary
responsibility, ●) or *ความรับผิดชอบรอง* (secondary, ○).

It is the one place a programme states, under regulation, how central an outcome
is to a course. That makes it evidence for level inference — and only evidence:
[[zaki-2023-clo-plo-mapping-automation]] reconstructs this matrix at 83–88 %
agreement with domain experts, so it is hand-authored and noisy, not ground truth.

**The marks are invisible to text extraction.** They are drawn in Wingdings and
Symbol fonts whose glyphs have no `ToUnicode` mapping, so `pdftotext` and
`page.get_text()` return the row with the marks silently missing. They have to be
read positionally, from span coordinates.

Two things vary by document and are therefore measured rather than assumed:

- **Which glyph means which.** Each producer picks its own — SWU uses Wingdings2
  `\\x01` and Wingdings `\\uf0a1`, SU uses `\\uf098`, CMU `\\uf050`. Rather than
  carry a font table, the extractor **renders each glyph and measures its ink
  coverage**: a filled ● covers roughly twice the area of a hollow ○.
- **Page rotation.** SWU prints the matrix sideways (rotation 90), so reading
  order and coordinate axes do not coincide.
"""

from __future__ import annotations

import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

#: Fonts a producer might draw the marks in.
SYMBOL_FONTS = ("Wingding", "Symbol", "Webding", "ZapfD")

#: A page needs at least this many marks to be part of the matrix rather than a
#: stray bullet in prose.
MIN_MARKS_PER_PAGE = 20

#: Programme learning outcome labels: `1.1`, `2.4`, `5.3`.
OUTCOME_LABEL = re.compile(r"^\d\.\d$")

#: The same labels when a producer packs the whole header row into one span.
OUTCOME_LABEL_INLINE = re.compile(r"\b\d\.\d\b")

#: Course codes, in any of the five conventions the corpus uses.
COURSE_CODE = re.compile(r"[ก-ฮ]{2,4}\s?\d{3}|\b\d{6,8}\b|\d{3}[-\s]\d{2,3}")

#: How far a mark may sit from a row or column label and still belong to it.
ROW_TOLERANCE = 6.0
COLUMN_TOLERANCE = 12.0


class Responsibility:
    PRIMARY = "primary"  # ● ความรับผิดชอบหลัก
    SECONDARY = "secondary"  # ○ ความรับผิดชอบรอง


@dataclass(frozen=True, slots=True)
class CurriculumMark:
    """One cell of the matrix: this course carries this responsibility level."""

    course_code: str
    outcome: str  # e.g. "2.1"
    responsibility: str
    page: int

    @property
    def is_primary(self) -> bool:
        return self.responsibility == Responsibility.PRIMARY


@dataclass(frozen=True, slots=True)
class CurriculumMapReport:
    pages: tuple[int, ...]
    marks_found: int
    marks_assigned: int
    courses: int
    outcomes: tuple[str, ...]
    glyph_ink: dict[str, float] = field(default_factory=dict)
    rotation: int = 0

    def summary(self) -> str:
        if not self.pages:
            return "no curriculum-responsibility matrix found"
        glyphs = ", ".join(f"{g}={v:.3f}" for g, v in self.glyph_ink.items())
        return (
            f"{self.marks_assigned} of {self.marks_found} marks assigned across "
            f"{self.courses} courses × {len(self.outcomes)} outcomes "
            f"on pages {', '.join(str(p) for p in self.pages)} "
            f"(rotation {self.rotation}; glyph ink {glyphs})"
        )


def _reading_axes(bbox, rotation: int, page_height: float) -> tuple[float, float]:
    """Map a bbox centre onto (across, down) in *reading* order.

    A rotated page stores coordinates in the unrotated frame, so the axis that
    reads left-to-right is not x. This is the only place rotation is handled.
    """
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    if rotation == 90:
        return page_height - y, x
    if rotation == 270:
        return y, -x
    return x, y


def _cluster(values: list[float], tolerance: float) -> list[float]:
    """Group aligned positions into column centres."""
    if not values:
        return []
    centres: list[list[float]] = []
    for value in sorted(values):
        if centres and value - centres[-1][-1] <= tolerance:
            centres[-1].append(value)
        else:
            centres.append([value])
    return [sum(group) / len(group) for group in centres]


def _ink(page, bbox, dpi: int = 300) -> float | None:
    """Fraction of a glyph's box covered in ink.

    Font-agnostic: a filled circle covers about twice the area of a hollow one,
    whatever font the producer chose to draw it in.
    """
    import pymupdf

    rect = pymupdf.Rect(bbox)
    if rect.is_empty or rect.width < 0.5 or rect.height < 0.5:
        return None
    pixmap = page.get_pixmap(clip=rect, dpi=dpi, colorspace=pymupdf.csGRAY)
    if not pixmap.width or not pixmap.height:
        return None
    dark = sum(1 for value in pixmap.samples if value < 128)
    return dark / (pixmap.width * pixmap.height)


def extract_curriculum_map(
    path: Path | str,
) -> tuple[list[CurriculumMark], CurriculumMapReport]:
    """Read the responsibility matrix out of a มคอ.2."""
    import pymupdf

    marks: list[CurriculumMark] = []
    pages_used: list[int] = []
    glyph_ink: dict[str, float] = {}
    courses: set[str] = set()
    outcomes: set[str] = set()
    total_symbols = 0
    rotation = 0

    with pymupdf.open(path) as doc:
        # Which pages carry the matrix: those dense in symbol-font glyphs.
        density: Counter = Counter()
        for number, page in enumerate(doc):
            count = sum(
                len(span["text"].strip())
                for block in page.get_text("dict")["blocks"]
                for line in block.get("lines", [])
                for span in line["spans"]
                if any(f in span["font"] for f in SYMBOL_FONTS) and span["text"].strip()
            )
            if count >= MIN_MARKS_PER_PAGE:
                density[number] = count
        if not density:
            return [], CurriculumMapReport((), 0, 0, 0, ())

        # Learn what each glyph means, once, from ink coverage across the matrix.
        samples: dict[str, list] = defaultdict(list)
        for number in density:
            page = doc[number]
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if any(f in span["font"] for f in SYMBOL_FONTS) and text:
                            key = f"{span['font'].split('+')[-1]}|{text}"
                            if len(samples[key]) < 8:
                                samples[key].append((number, span["bbox"]))

        for key, places in samples.items():
            values = [v for v in (_ink(doc[n], b) for n, b in places) if v is not None]
            if values:
                glyph_ink[key] = sum(values) / len(values)
        if not glyph_ink:
            return [], CurriculumMapReport(tuple(sorted(density)), 0, 0, 0, ())

        # The most-inked glyph is ●; anything materially lighter is ○.
        heaviest = max(glyph_ink.values())
        primary_glyphs = {k for k, v in glyph_ink.items() if v >= heaviest * 0.75}

        for number in sorted(density):
            page = doc[number]
            if page.rotation:
                rotation = page.rotation
            height = page.rect.height
            symbols: list[tuple[float, float, str]] = []
            labels: list[tuple[float, float, str]] = []

            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if not text:
                            continue
                        across, down = _reading_axes(span["bbox"], rotation, height)
                        if any(f in span["font"] for f in SYMBOL_FONTS):
                            key = f"{span['font'].split('+')[-1]}|{text}"
                            symbols.append((across, down, key))
                        else:
                            labels.append((across, down, text))

            total_symbols += len(symbols)

            # Outcome labels usually arrive as ONE span holding the whole header
            # row — `1.1 1.2 1.3 … 5.3` — so per-column positions cannot come
            # from them. The marks themselves align into columns; cluster those,
            # then label the clusters left to right from the header.
            header: list[str] = []
            for _, _, text in labels:
                found = OUTCOME_LABEL_INLINE.findall(text)
                if len(found) > len(header):
                    header = found
            singles = sorted(
                ((a, t) for a, _, t in labels if OUTCOME_LABEL.match(t)),
                key=lambda c: c[0],
            )
            if len(singles) > len(header):
                header = [t for _, t in singles]

            rows = [(d, t) for _, d, t in labels if COURSE_CODE.search(t)]
            if not symbols or not rows:
                continue

            columns = _cluster([a for a, _, _ in symbols], COLUMN_TOLERANCE)
            if not columns:
                continue
            pages_used.append(number + 1)

            for across, down, key in symbols:
                index = min(range(len(columns)), key=lambda i: abs(columns[i] - across))
                if abs(columns[index] - across) > COLUMN_TOLERANCE:
                    continue
                row = min(rows, key=lambda r: abs(r[0] - down))
                if abs(row[0] - down) > ROW_TOLERANCE:
                    continue
                code = COURSE_CODE.search(row[1])
                if not code:
                    continue
                outcome = header[index] if index < len(header) else f"col{index + 1}"
                code_text = " ".join(code.group().split())
                courses.add(code_text)
                outcomes.add(outcome)
                marks.append(
                    CurriculumMark(
                        course_code=code_text,
                        outcome=outcome,
                        responsibility=(
                            Responsibility.PRIMARY
                            if key in primary_glyphs
                            else Responsibility.SECONDARY
                        ),
                        page=number + 1,
                    )
                )

    return marks, CurriculumMapReport(
        pages=tuple(sorted(set(pages_used))),
        marks_found=total_symbols,
        marks_assigned=len(marks),
        courses=len(courses),
        outcomes=tuple(sorted(outcomes)),
        glyph_ink=glyph_ink,
        rotation=rotation,
    )
