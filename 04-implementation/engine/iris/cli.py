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


def _cmd_clo(args: argparse.Namespace) -> int:
    """Extract per-course learning outcomes and their cognitive-demand verbs."""
    from iris.ingest import extract_learning_outcomes

    outcomes, report = extract_learning_outcomes(args.pdf)
    print(f"{args.pdf}\n{report.summary()}")
    if not outcomes:
        return 1
    by_course: dict[str, list] = {}
    for outcome in outcomes:
        by_course.setdefault(outcome.course_code or "—", []).append(outcome)
    for code, entries in list(by_course.items())[: args.limit]:
        print(f"\n  {code}")
        for entry in sorted(entries, key=lambda e: e.number):
            band = entry.verb_band or "?"
            print(f"     {entry.number}. [{band:10}] {entry.text[:66]}")
    return 0


def _cmd_retrieve(args: argparse.Namespace) -> int:
    """Retrieve candidate skills for a course, or for free text.

    This is the *first* of the two linking stages. It ranks; it does not decide.
    A skill appearing here is a candidate an adjudicator must still weigh against
    the course text, so nothing printed here is a link.
    """
    from iris.link import get_index

    index = get_index()
    if args.pdf:
        from iris.ingest import (
            Verdict,
            diagnose,
            extract,
            extract_courses,
            learn_and_repair,
            normalise_chars,
        )

        document = extract(args.pdf)
        chars, fonts, _ = normalise_chars(document.chars, document.fonts)
        if diagnose("".join(chars)).verdict is Verdict.REPAIRABLE:
            chars = list(learn_and_repair(chars, fonts).text)
        courses, _ = extract_courses("".join(chars), document.page_of)
        wanted = args.course.replace(" ", "") if args.course else None
        targets = [
            (c.code, f"{c.title_th or ''} {c.title_en or ''} {c.description_th}", c.page)
            for c in courses
            if c.description_th and (not wanted or c.code.replace(" ", "") == wanted)
        ]
        if not targets:
            print(f"no course with a description matching {args.course or '(any)'}")
            return 1
        targets = targets[: args.limit]
    else:
        targets = [("query", args.text or "", None)]

    for code, text, page in targets:
        where = f" (p. {page})" if page else ""
        print(f"\n{code}{where}  {' '.join(text.split())[:72]}")
        for candidate in index.search(text, k=args.k):
            print(f"  {candidate}")
    return 0


def _cmd_link(args: argparse.Namespace) -> int:
    """Link a whole programme: retrieve, adjudicate, report — one pinned provider."""
    from iris.link import get_provider, link_programme
    from iris.link.provider import OpenAICompatible, ProviderError

    try:
        provider = get_provider(args.provider)
    except ProviderError as error:
        print(f"provider unavailable: {error}")
        return 2
    if args.model and isinstance(provider, OpenAICompatible):
        provider.model = args.model

    ok, detail = provider.health()
    print(f"provider {provider.name} · model {provider.model} · health {ok} ({detail})")
    if not ok:
        return 2

    def show(result) -> None:
        if result.failed:
            print(f"\n  ! {result.course_code}  FAILED — {result.rejected[0]}")
            return
        head = f"\n  {result.course_code}"
        print(
            f"{head}  (no link — the vocabulary names nothing this course develops)"
            if result.is_zero_link
            else head
        )
        for link in result.links:
            print(f"{link}")
            if args.verbose and link.evidence:
                print(f"        “{link.evidence[:70]}”")
        if result.out_of_vocabulary:
            print(f"      out-of-vocabulary: {', '.join(result.out_of_vocabulary[:4])}")

    _, report = link_programme(args.pdf, provider, k=args.k, limit=args.limit, on_course=show)
    print(f"\n{report.summary()}")
    for note in report.notes:
        print(f"⚠️  {note}")
    return 1 if report.notes else 0


def _cmd_sample(args: argparse.Namespace) -> int:
    """Draw the Sprint 4 annotation sample and write one workbook per annotator."""
    from iris.annotation import draw_sample, write_workbook
    from iris.annotation.sample import fingerprint

    courses, report = draw_sample(args.pdf, target=args.size, seed=args.seed)
    print(report.summary())
    for note in report.notes:
        print(f"⚠️  {note}")
    print(f"\nsample fingerprint {fingerprint(courses)} — record it with any result")

    if args.out:
        out = pathlib.Path(args.out)
        names = args.annotator or ["A", "B"]
        for name in names:
            path = write_workbook(courses, report, out / f"sample-{name}.csv", annotator=name)
            print(f"  wrote {path}")
        return 0

    for course in courses:
        flag = "*" if course.by_elimination else " "
        print(f"  {flag}{course.stratum:18} {course.code:9} {course.title_th[:44]}")
    print("\n  * category inferred by elimination, not read from the listing")
    return 0


def _cmd_structure(args: argparse.Namespace) -> int:
    """Read the programme structure — which category each course sits in."""
    from iris.ingest.structure import extract_structure

    placed, report = extract_structure(args.pdf)
    print(f"{args.pdf}\n{report.summary()}\n")
    for category in report.categories:
        print(f"  {category}")
    checks = report.credit_check()
    if checks:
        print("\ncredit check — the document's own claim against what was read:")
        print("\n".join(checks))
    if args.verbose:
        from collections import defaultdict

        grouped = defaultdict(list)
        for code, category in sorted(placed.items()):
            grouped[f"{category.number} {category.label}"].append(code)
        print()
        for label, codes in sorted(grouped.items()):
            print(f"  {label:30} ({len(codes):2}) {' '.join(codes)}")
    return 0 if report.categories else 1


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

    p_clo = sub.add_parser("clo", help="extract per-course learning outcomes")
    p_clo.add_argument("pdf")
    p_clo.add_argument("-n", "--limit", type=int, default=8)
    p_clo.set_defaults(func=_cmd_clo)

    p_retrieve = sub.add_parser(
        "retrieve", help="rank candidate skills for a course (stage 1 of linking)"
    )
    p_retrieve.add_argument("pdf", nargs="?", help="a มคอ.2 PDF; omit to rank free text")
    p_retrieve.add_argument("-c", "--course", help="a single course code, e.g. คพ242")
    p_retrieve.add_argument("-t", "--text", help="free text to rank, instead of a PDF")
    p_retrieve.add_argument("-k", type=int, default=20, help="candidates per course")
    p_retrieve.add_argument("-n", "--limit", type=int, default=5, help="courses to show")
    p_retrieve.set_defaults(func=_cmd_retrieve)

    p_link = sub.add_parser("link", help="link a programme to the national vocabulary")
    p_link.add_argument("pdf", help="path to a มคอ.2 PDF")
    p_link.add_argument("-p", "--provider", help="local | workers-ai (default: $IRIS_PROVIDER)")
    p_link.add_argument("-m", "--model", help="override the model for this run")
    p_link.add_argument("-k", type=int, default=30, help="candidates offered per course")
    p_link.add_argument("-n", "--limit", type=int, help="stop after this many courses")
    p_link.add_argument("-v", "--verbose", action="store_true", help="show evidence spans")
    p_link.set_defaults(func=_cmd_link)

    p_struct = sub.add_parser(
        "structure", help="read the programme structure (core / elective / general education)"
    )
    p_struct.add_argument("pdf")
    p_struct.add_argument("-v", "--verbose", action="store_true", help="list courses per category")
    p_struct.set_defaults(func=_cmd_structure)

    p_sample = sub.add_parser("sample", help="draw the Sprint 4 stratified annotation sample")
    p_sample.add_argument("pdf")
    p_sample.add_argument("-n", "--size", type=int, default=50, help="target sample size")
    p_sample.add_argument("--seed", type=int, default=20260831, help="recorded with the sample")
    p_sample.add_argument("-o", "--out", help="directory to write annotator workbooks into")
    p_sample.add_argument(
        "-a", "--annotator", action="append", help="annotator name; repeat for each (default A, B)"
    )
    p_sample.set_defaults(func=_cmd_sample)

    p_db = sub.add_parser("db", help="database operations")
    db_sub = p_db.add_subparsers(dest="db_command", required=True)
    p_init = db_sub.add_parser("init", help="create the schema directly (dev bootstrap)")
    p_init.set_defaults(func=_cmd_db_init)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
