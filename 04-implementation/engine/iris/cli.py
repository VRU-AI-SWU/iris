"""Command-line entry point.

The pipeline is driven from here through Sprint 7: the evaluation gate needs a
reproducible command, not a web request.
"""

from __future__ import annotations

import argparse
import pathlib
import sys

from iris import __version__
from iris.config import get_settings
from iris.snapshot import load_snapshot


def _cmd_snapshot(args: argparse.Namespace) -> int:
    snapshot = load_snapshot()
    print(snapshot.report.summary())
    if args.verbose:
        print("\nSeniority ladders (demand-side depth signal):")
        for pair in snapshot.seniority_pairs:
            gradient = pair.gradient()
            top = snapshot.skill(gradient[0][0]) if gradient else None
            head = f"{top.title_en} +{gradient[0][1]:.1f}pp" if top else "—"
            print(f"  {pair.slug:52} {len(gradient):3} shared · top rise: {head}")
    return 0


def _cmd_check(args: argparse.Namespace) -> int:
    """Run the integrity gate on a PDF, and the repair if it is repairable."""
    from iris.ingest import Verdict, diagnose, extract, learn_and_repair, normalise_chars

    doc = extract(args.pdf)
    print(f"{args.pdf}  ·  {doc.page_count} pages, {len(doc.chars):,} characters\n")

    chars, fonts, norm = normalise_chars(doc.chars, doc.fonts)
    if norm.total:
        print(f"── normalise ──\n{norm.summary()}\n")

    report = diagnose("".join(chars))
    print(report.summary())

    if report.verdict is not Verdict.REPAIRABLE:
        print(
            "\n→ "
            + {
                Verdict.CLEAN: "text layer is usable as-is.",
                Verdict.REPAIRED: "text layer is usable.",
                Verdict.LOSSY: "re-extract with a vision model; flag as vision-derived.",
                Verdict.UNUSABLE: "reject — ask for a better source file.",
            }[report.verdict]
        )
        return 0 if report.usable else 1

    print("\n── repair ──")
    result = learn_and_repair(chars, fonts)
    print(result.summary())
    if args.verbose:
        for rule in result.rules:
            for before, after in rule.examples[:1]:
                print(f"      {before[:36]!r} → {after[:36]!r}")

    print("\n── gate, re-run after repair ──")
    after = diagnose(result.text)
    print(after.summary())

    if args.out:
        pathlib.Path(args.out).write_text(result.text, encoding="utf-8")
        print(f"\nrepaired text → {args.out}")
    return 0 if after.usable else 1


def _cmd_courses(args: argparse.Namespace) -> int:
    """Extract courses from a TQF PDF: gate, normalise, repair, then parse."""
    from iris.ingest import (
        Verdict,
        diagnose,
        extract,
        extract_courses,
        learn_and_repair,
        normalise_chars,
    )

    doc = extract(args.pdf)
    chars, fonts, _ = normalise_chars(doc.chars, doc.fonts)
    report = diagnose("".join(chars))
    if report.verdict is Verdict.REPAIRABLE:
        chars = list(learn_and_repair(chars, fonts).text)
        report = diagnose("".join(chars))
    if not report.usable:
        print(f"text layer is {report.verdict.value} — cannot extract courses")
        print(report.summary())
        return 1

    courses, extraction = extract_courses("".join(chars), doc.page_of)
    print(f"{args.pdf}  ·  {doc.page_count} pages")
    print(extraction.summary())

    def thai_chars(course) -> int:
        return sum(1 for x in (course.description_th or "") if "฀" <= x <= "๿")

    prose = [c for c in courses if thai_chars(c) > 60]
    print(f"{len(prose)} of them have a Thai description long enough to link from\n")

    for course in courses if args.all else prose[: args.limit]:
        title = course.title_th or ""
        print(f"  p.{course.page:>3}  {course.code:12} {course.credit_spec:12} {title}")
        if course.title_en:
            print(f"        {'':12} {'':12} {course.title_en}")
        if args.verbose and course.description_th:
            print(f"        {course.description_th[:150]}")
    return 0


def _cmd_map(args: argparse.Namespace) -> int:
    """Read the curriculum-responsibility matrix (● หลัก / ○ รอง)."""
    from collections import Counter

    from iris.ingest import extract_curriculum_map

    marks, report = extract_curriculum_map(args.pdf)
    print(f"{args.pdf}\n{report.summary()}")
    if not marks:
        return 1
    counts = Counter(m.responsibility for m in marks)
    print(f"\n{counts['primary']} primary (●), {counts['secondary']} secondary (○)")
    if args.verbose:
        by_course: dict[str, list] = {}
        for mark in marks:
            by_course.setdefault(mark.course_code, []).append(mark)
        for code, entries in list(by_course.items())[: args.limit]:
            primary = sorted(m.outcome for m in entries if m.is_primary)
            secondary = sorted(m.outcome for m in entries if not m.is_primary)
            print(f"  {code:12} ● {','.join(primary) or '—':28} ○ {','.join(secondary) or '—'}")
    return 0


def _cmd_db_init(_: argparse.Namespace) -> int:
    from iris.db import create_all

    create_all()
    print(f"schema created at {get_settings().database_url}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="iris", description=__doc__)
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p_snap = sub.add_parser("snapshot", help="report on the pinned national standard")
    p_snap.add_argument("-v", "--verbose", action="store_true")
    p_snap.set_defaults(func=_cmd_snapshot)

    p_check = sub.add_parser("check", help="run the Thai text-layer integrity gate on a TQF PDF")
    p_check.add_argument("pdf", help="path to a มคอ.2 PDF")
    p_check.add_argument("-v", "--verbose", action="store_true", help="show repair examples")
    p_check.add_argument("-o", "--out", help="write the repaired text to a file")
    p_check.set_defaults(func=_cmd_check)

    p_courses = sub.add_parser("courses", help="extract courses from a TQF PDF")
    p_courses.add_argument("pdf")
    p_courses.add_argument(
        "-a", "--all", action="store_true", help="include courses with no description"
    )
    p_courses.add_argument("-n", "--limit", type=int, default=15)
    p_courses.add_argument("-v", "--verbose", action="store_true", help="show descriptions")
    p_courses.set_defaults(func=_cmd_courses)

    p_map = sub.add_parser("map", help="read the curriculum-responsibility matrix")
    p_map.add_argument("pdf")
    p_map.add_argument("-v", "--verbose", action="store_true")
    p_map.add_argument("-n", "--limit", type=int, default=12)
    p_map.set_defaults(func=_cmd_map)

    p_db = sub.add_parser("db", help="database operations")
    db_sub = p_db.add_subparsers(dest="db_command", required=True)
    p_init = db_sub.add_parser("init", help="create the schema directly (dev bootstrap)")
    p_init.set_defaults(func=_cmd_db_init)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
