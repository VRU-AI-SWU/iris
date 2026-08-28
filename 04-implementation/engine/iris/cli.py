"""Command-line entry point.

The pipeline is driven from here through Sprint 7: the evaluation gate needs a
reproducible command, not a web request.
"""

from __future__ import annotations

import argparse
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

    p_db = sub.add_parser("db", help="database operations")
    db_sub = p_db.add_subparsers(dest="db_command", required=True)
    p_init = db_sub.add_parser("init", help="create the schema directly (dev bootstrap)")
    p_init.set_defaults(func=_cmd_db_init)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
