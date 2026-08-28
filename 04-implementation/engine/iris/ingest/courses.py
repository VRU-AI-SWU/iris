"""Extract courses from a มคอ.2, without depending on how it is formatted.

The five universities in the corpus number their courses five different ways —
`ว.คพ. 232 (204232)`, `01418221`, `968-140`, `517 493`, `คพ252 / CP252` — and
head the course-description section differently too, CMU calling courses
`กระบวนวิชา` where the others say `รายวิชา`. Anchoring on a heading or on one
code format would work for one document and fail on the next.

So the extractor anchors on the thing TQF actually regulates: the **credit
specification**, `x(y-z-w)` — lecture, practical, self-study hours. Every course
in every document carries one, it is language-independent, and PSU's
`3((2)-2-5)` variant is the only formatting difference across the corpus.

From that anchor:

1. **Learn the document's course-code shape.** Six candidate shapes are scored by
   how often each appears just before a credit spec; the document's own usage
   picks the winner. Same principle as the glyph repair table in `repair.py` —
   learn the convention from the document rather than shipping one.
2. Walk back from each anchor for the code and titles, forward for the description.
3. **Deduplicate.** A course appears several times — in the structure tables, the
   study plan, and the description section. The entry carrying a description is
   the one worth keeping.

Every entry records its source page, because a curriculum committee will
challenge specific assignments and the answer has to be one click away.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass, field

#: The TQF credit specification. PSU writes the lecture slot as `(2)`, hence the
#: optional inner parentheses. The lookbehind keeps `2.1(3-0-6)` from matching a
#: section number as a credit count.
CREDIT_SPEC = re.compile(
    r"(?<![\d.])(\d{1,2})\s*\(\s*\(?(\d+)\)?\s*-\s*\(?(\d+)\)?\s*-\s*\(?(\d+)\)?\s*\)"
)

#: Candidate course-code shapes, most specific first — an 8-digit KU code
#: contains a 6-digit substring, so ordering decides ties.
CODE_SHAPES: dict[str, str] = {
    "digits-8": r"\d{8}",
    "digits-6": r"\d{6}",
    "hyphen-3-3": r"\d{3}-\d{2,3}",
    "spaced-3-3": r"\d{3}\s\d{3}",
    "thai-prefix": r"[ก-ฮ]{2,4}\s?\d{3}",
    "latin-prefix": r"[A-Z]{2,4}\s?\d{3}",
}

#: How far back from a credit spec a course code may sit.
LOOKBACK = 90

#: How far forward a description may run before the next course starts.
MAX_DESCRIPTION = 1200

_THAI_TITLE = re.compile(r"[ก-๙][ก-๙\s\-–()/.,]{3,}")
_LATIN_TITLE = re.compile(r"[A-Za-z][A-Za-z\s\-–()/.,'&]{5,}")


@dataclass(frozen=True, slots=True)
class CourseEntry:
    """One course as it appears in the document, with its provenance."""

    code: str
    credits: float
    credit_spec: str
    title_th: str | None = None
    title_en: str | None = None
    description_th: str | None = None
    description_en: str | None = None
    page: int | None = None
    offset: int = 0  # character offset, for ordering and debugging

    @property
    def has_description(self) -> bool:
        return bool(self.description_th or self.description_en)


@dataclass(frozen=True, slots=True)
class ExtractionReport:
    """What was found, and how confident the extractor is in the shape it used."""

    code_shape: str
    shape_coverage: float  # fraction of anchors with a code in the lookback
    anchors: int
    courses: int
    with_description: int
    shape_scores: dict[str, int] = field(default_factory=dict)

    def summary(self) -> str:
        return (
            f"{self.courses} courses ({self.with_description} with a description) "
            f"from {self.anchors} credit specs · code shape {self.code_shape!r} "
            f"matched {self.shape_coverage:.0%} of anchors"
        )


def learn_code_shape(text: str, anchors: list[re.Match]) -> tuple[str, dict[str, int]]:
    """Pick the course-code shape this document uses.

    Scored by how many credit specs have a code of that shape just before them.
    Ties break toward the more specific shape, which is why `CODE_SHAPES` is
    ordered — every 8-digit code contains a 6-digit one.
    """
    scores: dict[str, int] = {}
    for name, pattern in CODE_SHAPES.items():
        rx = re.compile(pattern)
        scores[name] = sum(
            1 for m in anchors if rx.search(text[max(0, m.start() - LOOKBACK) : m.start()])
        )
    best = max(CODE_SHAPES, key=lambda name: (scores[name], -list(CODE_SHAPES).index(name)))
    return best, scores


def _clean(fragment: str | None) -> str | None:
    if not fragment:
        return None
    text = " ".join(fragment.split()).strip(" -–·:.,()")
    return text or None


def _titles(fragment: str) -> tuple[str | None, str | None]:
    """Thai and English titles from the text between a code and its credit spec."""
    thai = _THAI_TITLE.search(fragment)
    latin = _LATIN_TITLE.search(fragment)
    return _clean(thai.group() if thai else None), _clean(latin.group() if latin else None)


#: An English course title at the head of the body, which is where CMU, KU and
#: SU put it — after the credit spec rather than beside the Thai title. Either
#: parenthesised, or a short Latin run before the Thai prose begins.
_LEADING_EN_TITLE = re.compile(
    # Title case with lowercase joining words — "Introduction to Data Science"
    # breaks if every word is required to start with a capital.
    r"^[\s:·\-–]*(?:\(\s*)?"
    r"([A-Z][A-Za-z0-9&/,.\-']*(?:\s+(?:[A-Za-z0-9&/,.\-']+|[IVX]+)){0,9})"
    r"\s*\)?"
)


def _take_leading_en_title(body: str) -> tuple[str | None, str]:
    """Split a leading English title off the body, if one is there.

    Only a *short* leading Latin run counts. English prose that runs on is the
    document's English description, not its title, and belongs to the body.
    """
    match = _LEADING_EN_TITLE.match(body)
    if not match:
        return None, body
    candidate = _clean(match.group(1))
    if not candidate or len(candidate) > 90 or len(candidate.split()) > 10:
        return None, body
    rest = body[match.end() :]
    # A title is followed by more content; if nothing follows, it was the body.
    if len(rest.strip()) < 20:
        return None, body
    return candidate, rest


def _split_description(fragment: str) -> tuple[str | None, str | None]:
    """Thai and English halves of a description.

    Documents that give both run the Thai first and the English after; the split
    is the first long run of Latin text.
    """
    match = re.search(r"[A-Z][A-Za-z][^฀-๿]{40,}$", fragment)
    if match and match.start() > 20:
        return _clean(fragment[: match.start()]), _clean(match.group())
    latin = sum(1 for c in fragment if c.isascii() and c.isalpha())
    thai = sum(1 for c in fragment if "฀" <= c <= "๿")
    if thai == 0 and latin > 40:
        return None, _clean(fragment)
    return _clean(fragment), None


def extract_courses(
    text: str, page_of: Callable[[int], int] | None = None
) -> tuple[list[CourseEntry], ExtractionReport]:
    """Find every course in a มคอ.2, deduplicated, with descriptions where present."""
    anchors = list(CREDIT_SPEC.finditer(text))
    if not anchors:
        return [], ExtractionReport("none", 0.0, 0, 0, 0, {})

    shape, scores = learn_code_shape(text, anchors)
    code_rx = re.compile(CODE_SHAPES[shape])

    found: list[CourseEntry] = []
    for index, anchor in enumerate(anchors):
        window = text[max(0, anchor.start() - LOOKBACK) : anchor.start()]
        codes = list(code_rx.finditer(window))
        if not codes:
            continue
        last = codes[-1]
        code = " ".join(last.group().split())

        title_th, title_en = _titles(window[last.end() :])

        # The description runs from the credit spec to the next course, or to the
        # cap — whichever comes first.
        stop = anchors[index + 1].start() if index + 1 < len(anchors) else len(text)
        stop = min(stop, anchor.end() + MAX_DESCRIPTION)
        body = text[anchor.end() : stop]
        # Trim a trailing code belonging to the next course.
        trailing = list(code_rx.finditer(body))
        if trailing:
            body = body[: trailing[-1].start()]
        leading_en, body = _take_leading_en_title(body)
        if leading_en and not title_en:
            title_en = leading_en
        description_th, description_en = _split_description(body)

        found.append(
            CourseEntry(
                code=code,
                credits=float(anchor.group(1)),
                credit_spec=" ".join(anchor.group().split()),
                title_th=title_th,
                title_en=title_en,
                description_th=description_th,
                description_en=description_en,
                page=page_of(anchor.start()) if page_of else None,
                offset=anchor.start(),
            )
        )

    courses = _deduplicate(found)
    return courses, ExtractionReport(
        code_shape=shape,
        shape_coverage=len(found) / len(anchors),
        anchors=len(anchors),
        courses=len(courses),
        with_description=sum(1 for c in courses if c.has_description),
        shape_scores=scores,
    )


def _prose_score(text: str | None) -> int:
    """How much of this reads as prose rather than as a table row.

    A course description is mostly Thai words. A structure-table row that happens
    to sit near a credit spec is digits, dashes and fragments — and it can be
    *longer* than the real description, so length alone picks the wrong one.
    """
    if not text:
        return 0
    thai = sum(1 for c in text if "฀" <= c <= "๿")
    latin_words = len(re.findall(r"[A-Za-z]{3,}", text))
    digits = sum(1 for c in text if c.isdigit())
    return thai + latin_words * 3 - digits * 4


def _deduplicate(entries: list[CourseEntry]) -> list[CourseEntry]:
    """One entry per code — the occurrence carrying real prose wins.

    A course shows up in the structure tables, the study plan and the description
    section. Only the last carries prose, so entries are ranked by how much of
    their body reads as prose rather than by how long it is.
    """

    def richness(entry: CourseEntry) -> tuple[int, int, int]:
        prose = _prose_score(entry.description_th) + _prose_score(entry.description_en)
        titles = bool(entry.title_th) + bool(entry.title_en)
        return (prose, titles, -entry.offset)

    best: dict[str, CourseEntry] = {}
    for entry in entries:
        key = entry.code.replace(" ", "")
        if key not in best or richness(entry) > richness(best[key]):
            best[key] = entry
    return sorted(best.values(), key=lambda c: c.offset)
