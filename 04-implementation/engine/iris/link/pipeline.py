"""Link a whole programme: ingest, retrieve, adjudicate, report.

This is where the provider pinning of `provider.py` has teeth. The provider is
resolved **once**, before the first course, and a `QuotaExhausted` anywhere in the
loop aborts the whole run rather than finishing on the other backend. A programme
whose 78 courses were linked by two different models is not a reproducible
analysis, and the comparison between programmes that Iris exists to make would be
comparing models as much as curricula.

The stages stay visibly separate — retrieval reports its own numbers, adjudication
reports its own — because they fail differently and the Sprint 4 gate has to
attribute error to one of them.
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from iris.link.adjudicate import DEFAULT_K, Adjudication, AdjudicationReport, adjudicate
from iris.link.provider import Provider, QuotaExhausted
from iris.link.retrieval import get_index


@dataclass(frozen=True, slots=True)
class CourseText:
    """A course reduced to what linking needs, with its provenance intact."""

    code: str
    text: str
    page: int | None = None
    title: str = ""


def read_courses(pdf: Path | str) -> list[CourseText]:
    """Ingest a TQF and return its courses that carry a description.

    Runs the full Sprint 1–2 chain — normalise, diagnose, repair, extract — rather
    than a shortcut, because the repair is what makes the text retrievable at all.
    """
    from iris.ingest import (
        Verdict,
        diagnose,
        extract,
        extract_courses,
        learn_and_repair,
        normalise_chars,
    )

    document = extract(pdf)
    chars, fonts, _ = normalise_chars(document.chars, document.fonts)
    if diagnose("".join(chars)).verdict is Verdict.REPAIRABLE:
        chars = list(learn_and_repair(chars, fonts).text)
    courses, _ = extract_courses("".join(chars), document.page_of)

    return [
        CourseText(
            code=course.code,
            text=f"{course.title_th or ''} {course.title_en or ''} {course.description_th}".strip(),
            page=course.page,
            title=course.title_th or course.title_en or "",
        )
        for course in courses
        if course.description_th
    ]


def link_courses(
    courses: list[CourseText],
    provider: Provider,
    *,
    k: int = DEFAULT_K,
) -> Iterator[Adjudication]:
    """Link each course, yielding as it goes.

    A generator so a long run reports progress rather than going silent for
    minutes — and so a `QuotaExhausted` surfaces to the caller at the course it
    happened on, with everything before it already in hand.
    """
    index = get_index()
    for course in courses:
        candidates = index.search(course.text, k=k)
        yield adjudicate(
            course.text,
            candidates,
            provider,
            course_code=course.code,
            page=course.page,
        )


def link_programme(
    pdf: Path | str,
    provider: Provider,
    *,
    k: int = DEFAULT_K,
    limit: int | None = None,
    on_course=None,
) -> tuple[list[Adjudication], AdjudicationReport]:
    """Link a whole programme with one pinned provider.

    🔴 A quota exhaustion **aborts**. The partial results are returned alongside a
    report that says so, so the caller can requeue on the other provider from the
    start — never resume mid-programme.
    """
    courses = read_courses(pdf)
    if limit:
        courses = courses[:limit]

    report = AdjudicationReport(courses=len(courses))
    results: list[Adjudication] = []
    started = time.monotonic()

    try:
        for result in link_courses(courses, provider, k=k):
            results.append(result)
            _tally(report, result)
            if on_course:
                on_course(result)
    except QuotaExhausted as exhausted:
        report.notes.append(
            f"ABORTED after {len(results)} of {len(courses)} courses: {exhausted}. "
            "Requeue on the other provider from the start — a programme linked by "
            "two models is not comparable with one linked by a single model."
        )

    report.seconds = time.monotonic() - started
    report.courses = len(courses)
    return results, report


def _tally(report: AdjudicationReport, result: Adjudication) -> None:
    if result.links:
        report.linked += 1
    elif result.failed:
        report.failed += 1
    else:
        report.zero_link += 1
    report.links += len(result.links)
    report.verified += sum(1 for link in result.links if link.evidence_verified)
    report.rejected += len(result.rejected)
    report.out_of_vocabulary += len(result.out_of_vocabulary)
    if result.completion:
        report.prompt_tokens += result.completion.prompt_tokens
