"""Read the programme structure — which category each course belongs to.

The course catalogue says what a course *is*; it does not say whether the
programme treats it as core, elective, or general education. That distinction
lives in a different part of the มคอ.2 — the numbered course listing under
`โครงสร้างหลักสูตร` — and Sprint 4's stratified annotation sample cannot be drawn
without it.

**Two levels, learned differently.** The top-level divisions are named by
regulation and appear verbatim in all five documents in the corpus:
`หมวดวิชาศึกษาทั่วไป`, `หมวดวิชาเฉพาะ`, `หมวดวิชาเลือกเสรี`. The subdivisions
underneath are *not* regulated — SWU uses แกน/บังคับ/เลือก/โท, CMU adds กลุ่มวิชา
and วิชาเอก, PSU leans on วิชาชีพ — so they are read from whatever the document
writes rather than matched against a fixed list.

**The document validates the extraction.** Each heading states its own credit
requirement (`รวม 48 หน่วยกิต`, `ไม่น้อยกว่า 6 หน่วยกิต`). Summing the credits of the
courses assigned to a heading and comparing against that figure is a check the
document itself supplies — a required category should match exactly, and an
`ไม่น้อยกว่า` category should meet or exceed. `StructureReport` reports the
comparison rather than asserting it, because a mismatch is a finding about the
document as often as a bug in the reader.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

#: Top-level divisions, named by TQF regulation. Present in all five producers.
TOP_LEVEL = {
    "ศึกษาทั่วไป": "general-education",
    "เลือกเสรี": "free-elective",
    "เฉพาะ": "major",
}

#: Intra-line whitespace. ⚠️ Not `[ \t]`: repaired Thai text carries separator
#: control characters (`\x1f`) where a producer broke a word, and Python's `\s`
#: counts those as whitespace while `[ \t]` does not — a heading matched with
#: `[ \t]` stops at the first break and loses the credit figure after it.
INLINE = r"[^\S\r\n]"

#: A numbered heading: `1. หมวดวิชาศึกษาทั่วไป …` or `2.2 วิชาบังคับ …`.
#: The number is what separates a heading from a passing mention in prose.
HEADING = re.compile(
    rf"^{INLINE}*(\d(?:\.\d){{0,2}}){INLINE}*\.?{INLINE}*"
    rf"((?:หมวด)?วิชา\S*(?:{INLINE}+\S+){{0,14}})",
    re.M,
)

#: `รวม 48 หน่วยกิต` / `ไม่น้อยกว่า 6 หน่วยกิต` — the document's own statement of what
#: a category requires, and therefore the check on whether it was read correctly.
CREDIT_CLAIM = re.compile(r"(\d{1,3})\s*หน\s?[่ ]?วยกิต")

#: `ไม่น้อยกว่า` marks a floor rather than an exact requirement.
AT_LEAST = re.compile(r"ไม\s?[่ ]?น้อยกว\s?[่ ]?า")

#: Courses a block must contain before it counts as a listing rather than a credit
#: table. Low, because a small programme's listing is still a listing.
MIN_BLOCK_COURSES = 5

#: Headings a block must contain. A numbered outline has structure; a lone heading a
#: hundred pages later does not. This is what separates the real listing from the
#: appendix comparison table, where SWU repeats `3. หมวดวิชาเลือกเสรี` above a table of
#: old-versus-new courses — a block of one heading that was claiming 11 courses.
MIN_BLOCK_HEADINGS = 2

#: Course codes in any of the corpus's five conventions.
COURSE_CODE = re.compile(r"[ก-ฮ]{2,4}\s?\d{3}|\b\d{6,8}\b|\d{3}[-\s]\d{2,3}")

#: The TQF credit specification, `3(2-2-5)`, borrowed from the course extractor.
#: PSU writes `3((2)-2-5)`; the inner parentheses are the only variant in the corpus.
CREDIT_SPEC = re.compile(r"(?<![\d.])\d{1,2}\s*\(\s*\(?\d+\)?\s*-\s*\(?\d+\)?\s*-\s*\(?\d+\)?\s*\)")

#: How far after a course code its credit specification may sit and still belong to it.
#: A catalogue row is `code · Thai title · English title · 3(2-2-5)`, so the span covers
#: two titles.
SPEC_LOOKAHEAD = 220

#: Hard ceiling on how far below a heading a course may be claimed. Only a backstop;
#: the run rule below almost always stops first.
MAX_SPAN = 9_000

#: A listing is *dense*: heading, then codes, one after another. So a heading's courses
#: are the unbroken run beneath it, and the run ends at the first gap wider than this.
#:
#: ⚠️ This replaces a fixed-span rule that was measurably wrong. SWU's
#: `3. หมวดวิชาเลือกเสรี` lists **no** courses — it says to choose any course in the
#: university — and a fixed span let it swallow the study plan two pages later,
#: labelling 42 of 57 courses as free electives. A heading with nothing directly
#: beneath it must govern nothing.
GAP_LIMIT = 1_500

#: Words that mark a subdivision as elective rather than required. Learned terms
#: are classified by these rather than by an enumerated list of subdivision names,
#: because the subdivision vocabulary is not regulated.
ELECTIVE_WORDS = ("เลือก", "โท")


@dataclass(frozen=True, slots=True)
class Category:
    """One numbered heading in the course listing."""

    number: str  # "2.2"
    label: str  # "วิชาบังคับ"
    division: str  # general-education | major | free-elective
    stratum: str  # core | elective | general-education
    claimed_credits: float | None
    at_least: bool  # the claim is a floor, not an exact figure
    page: int
    offset: int

    def __str__(self) -> str:
        credits = f"{self.claimed_credits:g}" if self.claimed_credits else "—"
        floor = "≥" if self.at_least else " "
        return f"{self.number:5} {self.label:24} {floor}{credits:>4}  [{self.stratum}]"


@dataclass(frozen=True, slots=True)
class StructureReport:
    categories: tuple[Category, ...]
    assigned: int
    unassigned: int
    credits_by_category: dict[str, float] = field(default_factory=dict)

    @property
    def strata(self) -> dict[str, int]:
        return {}

    def summary(self) -> str:
        if not self.categories:
            return "no programme structure found"
        return (
            f"{len(self.categories)} categories, {self.assigned} courses assigned, "
            f"{self.unassigned} unplaced"
        )

    def credit_check(self) -> list[str]:
        """Compare extracted credits against what each heading claims.

        ⚠️ Reported, never enforced. A required category that comes up short may
        mean the reader missed courses — or it may mean the document lists a
        module (`ชุดวิชา`) whose components are enumerated elsewhere. Both are
        worth seeing.
        """
        lines = []
        for category in self.categories:
            if category.claimed_credits is None:
                continue
            found = self.credits_by_category.get(category.number, 0.0)
            if category.at_least:
                ok = found >= category.claimed_credits
                relation = "≥"
            else:
                ok = abs(found - category.claimed_credits) < 0.5
                relation = "="
            mark = "✓" if ok else "✗"
            lines.append(
                f"  {mark} {category.number:5} {category.label[:22]:24} "
                f"claims {relation}{category.claimed_credits:g}, found {found:g}"
            )
        return lines


def classify(number: str, label: str, division: str) -> str:
    """Which annotation stratum a heading belongs to.

    Three strata, following the Sprint 4 sampling plan: `general-education`,
    `core`, `elective`. The mapping is deliberately coarse — a course is either
    something every graduate takes, something only some take, or general
    education — because that is the distinction the sample needs to balance.
    """
    if division == "general-education":
        return "general-education"
    if division == "free-elective":
        return "elective"
    # Inside หมวดวิชาเฉพาะ the subdivision decides, and its vocabulary varies by
    # document, so it is read rather than matched.
    if any(word in label for word in ELECTIVE_WORDS):
        return "elective"
    return "core"


def extract_structure(
    path: Path | str,
) -> tuple[dict[str, Category], StructureReport]:
    """Map each course code to the category the programme files it under."""
    from iris.ingest.courses import extract_courses
    from iris.ingest.integrity import Verdict, diagnose
    from iris.ingest.normalise import normalise_chars
    from iris.ingest.pdf import extract
    from iris.ingest.repair import learn_and_repair

    document = extract(path)
    chars, fonts, _ = normalise_chars(document.chars, document.fonts)
    if diagnose("".join(chars)).verdict is Verdict.REPAIRABLE:
        chars = list(learn_and_repair(chars, fonts).text)
    text = "".join(chars)

    categories = _read_headings(text, document.page_of)
    if not categories:
        return {}, StructureReport((), 0, 0)

    courses, _ = extract_courses(text, document.page_of)
    credits_of = {c.code.replace(" ", ""): c.credits for c in courses}

    # Walk the text and hand each course-code occurrence to the heading above it.
    # A code appears several times — the listing, the study plan, the description
    # block — so votes are collected and the most-supported category wins.
    # One vote per (heading occurrence, course). A มคอ.2 states its listing more than
    # once and an appendix comparison table lists the old and new curriculum side by
    # side, so a course can appear twice under the *same* heading — which would let one
    # appendix table outvote two genuine listings. Presence is what counts, not repetition.
    seen_here: set[tuple[int, str]] = set()
    votes: dict[str, dict[str, int]] = {}
    for category, code in _courses_under(categories, text):
        if (category.offset, code) in seen_here:
            continue
        seen_here.add((category.offset, code))
        votes.setdefault(code, {}).setdefault(category.number, 0)
        votes[code][category.number] += 1

    # Several listings may state the same category. Keep one per number for the
    # report, preferring an occurrence that states its credit requirement — that is
    # the one the credit check can be run against.
    by_number: dict[str, Category] = {}
    for category in categories:
        current = by_number.get(category.number)
        if current is None or (current.claimed_credits is None and category.claimed_credits):
            by_number[category.number] = category
    placed: dict[str, Category] = {}
    credits_by_category: dict[str, float] = {}
    depth = {c.number: c.number.count(".") for c in categories}
    for code, tally in votes.items():
        # Most listings wins; ties go to the more specific heading, because
        # `2.2 วิชาบังคับ` says more than the `2. หมวดวิชาเฉพาะ` that contains it.
        number = max(tally, key=lambda n: (tally[n], depth.get(n, 0)))
        placed[code] = by_number[number]
        credits_by_category[number] = credits_by_category.get(number, 0.0) + credits_of.get(
            code, 0.0
        )

    known = {c.code.replace(" ", "") for c in courses}
    return placed, StructureReport(
        categories=tuple(sorted(by_number.values(), key=lambda c: c.offset)),
        assigned=len(known & placed.keys()),
        unassigned=len(known - placed.keys()),
        credits_by_category=credits_by_category,
    )


def _read_headings(text: str, page_of) -> list[Category]:
    """Numbered category headings, in document order.

    A heading only counts if its top-level division can be identified — either
    from its own text (`หมวดวิชาเฉพาะ`) or, for a subdivision like `2.2 วิชาบังคับ`,
    inherited from the most recent top-level heading. That inheritance is what
    lets the subdivision vocabulary stay unenumerated.
    """
    found: list[Category] = []
    division = ""
    for match in HEADING.finditer(text):
        number, raw = match.group(1), " ".join(match.group(2).split())
        own = next((d for key, d in TOP_LEVEL.items() if key in raw), "")
        if own:
            division = own
        elif not division or "." not in number:
            # A numbered `วิชา…` line with no division above it is prose, not a heading.
            continue
        label = raw.split(" กำหนด")[0].split(" ไม")[0].strip() or raw
        claim = CREDIT_CLAIM.search(raw)
        found.append(
            Category(
                number=number,
                label=label[:40],
                division=division,
                stratum=classify(number, label, division),
                claimed_credits=float(claim.group(1)) if claim else None,
                at_least=bool(AT_LEAST.search(raw)),
                page=page_of(match.start()),
                offset=match.start(),
            )
        )
    return _listing_headings(found, text)


def _listing_headings(headings: list[Category], text: str) -> list[Category]:
    """Keep the heading occurrences that actually govern a course listing.

    A มคอ.2 states its structure more than once, and telling the statements apart
    took three attempts on real text:

    - *Most room below the heading* picks the credit table's **last** row, which has
      the rest of the page under it and no courses at all.
    - *Most courses below the heading, per number independently*, scatters the result
      across unrelated sections — SWU's `2.2` came from page 30 and `2.1.1` from page
      136, so codes were assigned to headings that never governed them.
    - *One contiguous block* merges the credit table into the listing that follows it,
      because they sit a few hundred characters apart.

    What separates them is measured, not guessed: **the credit table is a block in
    which every row has zero course codes before the next row.** A listing has
    container rows at zero too (`2. หมวดวิชาเฉพาะ` before `2.1`), but its leaves carry
    courses.

    So blocks are cut at a numbering restart or a large gap, blocks with no courses
    are dropped, and **every surviving block is kept**. SWU states its listing twice —
    once under `รายวิชา` and once as the module breakdown — and keeping both turns that
    redundancy into agreement: each course votes once per listing it appears in.
    """
    if not headings:
        return []

    def key(heading: Category) -> tuple[int, ...]:
        return tuple(int(part) for part in heading.number.split("."))

    blocks: list[list[Category]] = [[headings[0]]]
    for heading in headings[1:]:
        previous = blocks[-1][-1]
        restarted = key(heading) <= key(previous)
        far = heading.offset - previous.offset > MAX_SPAN
        (blocks.append([heading]) if restarted or far else blocks[-1].append(heading))

    # Score with the same rule the assignment uses, and stop at the next heading
    # *anywhere* in the document rather than the next one in this block — otherwise
    # the credit table's last row reaches into the listing below it and the table
    # scores as a listing.
    offsets = sorted(h.offset for h in headings)

    def rows_under(heading: Category) -> int:
        later = [o for o in offsets if o > heading.offset]
        stop = min(later[0] if later else len(text), heading.offset + MAX_SPAN)
        return sum(
            1
            for m in COURSE_CODE.finditer(text, heading.offset, stop)
            if _is_catalogue_row(text, m)
        )

    kept: list[Category] = []
    for block in blocks:
        if len(block) < MIN_BLOCK_HEADINGS:
            continue
        if sum(rows_under(h) for h in block) >= MIN_BLOCK_COURSES:
            kept.extend(block)
    return kept


def _is_catalogue_row(text: str, match: re.Match[str]) -> bool:
    """Whether a course code is a catalogue entry rather than a passing mention.

    ⚠️ The distinction is load-bearing and was learned the hard way. Counting every
    code occurrence gave SWU's `3. หมวดวิชาเลือกเสรี` — a category that lists no courses
    at all, saying instead to choose any course in the university — **64 courses**,
    swallowed from the course-code legend and the study plan that follow it. 42 of 57
    courses came out labelled free electives.

    A catalogue row carries the regulated credit specification `3(2-2-5)` after the
    code. The legend and the study plan do not. That is the same anchor the course
    extractor uses, and it is a property of the document rather than of this reader.
    """
    window = text[match.end() : match.end() + SPEC_LOOKAHEAD]
    return bool(CREDIT_SPEC.search(window))


def _courses_under(categories: list[Category], text: str):
    """Yield `(category, code)` for the unbroken run of courses beneath each heading.

    The run rather than a fixed window, because a listing is dense and the space
    after it is not. A heading whose first catalogue row is already past `GAP_LIMIT`
    governs nothing — the correct reading of a category that names no courses.
    """
    offsets = sorted(c.offset for c in categories)
    for category in categories:
        later = [o for o in offsets if o > category.offset]
        stop = min(later[0] if later else len(text), category.offset + MAX_SPAN)
        cursor = category.offset
        for match in COURSE_CODE.finditer(text, category.offset, stop):
            if not _is_catalogue_row(text, match):
                continue
            if match.start() - cursor > GAP_LIMIT:
                break
            cursor = match.end()
            yield category, " ".join(match.group().split()).replace(" ", "")
