#!/usr/bin/env python3
"""Mirror a pinned snapshot of the Thailand Skill Mapping Open Data API.

Source:  https://api.skillmapping.in.th  (OPS MHESI / KMITL)
Docs:    https://api.skillmapping.in.th/docs

The snapshot is the reproducibility anchor for Iris: every gap analysis is
computed against a fixed version of the national skill vocabulary, so results
can be reproduced after the upstream database changes.

Writes to  data/skillmapping/<YYYY-MM-DD>/  :
    manifest.json          snapshot metadata and counts
    industries.json        all industries (th + en titles)
    careers.json           careers for the target industries, with demand
                           distribution (count / percentage) and skillsGrowth
    skills-index.json      full vocabulary index (th + en titles, type, slug)
    skills-detail.json     definition + proficiency levels for every skill
                           referenced by the target industries' careers

Stdlib only — no dependencies, so it runs anywhere.

Usage:
    python3 fetch_snapshot.py                    # digital industry (v1 scope)
    python3 fetch_snapshot.py --industry all
    python3 fetch_snapshot.py --industry digital robotic
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

BASE = "https://api.skillmapping.in.th"
API = f"{BASE}/api/v1"
HEADERS = {
    "User-Agent": "iris-skillgap/1.0 (academic research; SWU)",
    "Accept": "application/json",
}
WORKERS = 4
RETRIES = 3


def get_url(url: str) -> dict | list:
    """GET a URL, retrying on transient failure."""
    last = None
    for attempt in range(RETRIES):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.load(resp)
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last = exc
            time.sleep(2**attempt)
    raise RuntimeError(f"GET {url} failed after {RETRIES} attempts: {last}")


def get(path: str, **params) -> dict | list:
    """GET an API path with query parameters."""
    query = "&".join(f"{k}={v}" for k, v in params.items() if v is not None)
    return get_url(f"{API}/{path.lstrip('/')}" + (f"?{query}" if query else ""))


def paged(path: str, per_page: int = 500, **params) -> list:
    """Collect every page of a paginated endpoint."""
    out, page = [], 1
    while True:
        body = get(path, page=page, perPage=per_page, **params)
        out.extend(body["data"])
        if len(out) >= body["total"] or not body["data"]:
            return out
        page += 1


def bilingual(th: list, en: list, key: str = "id") -> list:
    """Merge an English index into a Thai one as `title_en`."""
    en_title = {item[key]: item.get("title") for item in en}
    return [{**item, "title_en": en_title.get(item[key])} for item in th]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--industry",
        nargs="+",
        default=["digital"],
        help="industry slugs to mirror careers for, or 'all' (default: digital)",
    )
    ap.add_argument(
        "--out",
        type=Path,
        default=Path(__file__).parent,
        help="snapshot root directory",
    )
    args = ap.parse_args()

    root = args.out / date.today().isoformat()
    root.mkdir(parents=True, exist_ok=True)
    started = time.time()

    api_info = get_url(f"{BASE}/")  # root endpoint carries the API version
    print(f"API {api_info.get('version')} → {root}")

    # ── industries ────────────────────────────────────────────────────────────
    industries = bilingual(get("industries"), get("industries", locale="en"))
    wanted = (
        industries
        if args.industry == ["all"]
        else [i for i in industries if i["slug"] in args.industry]
    )
    if not wanted:
        sys.exit(f"no industry matched {args.industry}; have: "
                 f"{[i['slug'] for i in industries]}")
    (root / "industries.json").write_text(
        json.dumps(industries, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"  industries: {len(industries)} "
          f"(mirroring careers for {[i['slug'] for i in wanted]})")

    # ── careers, with the demand distribution already attached ────────────────
    careers = []
    for industry in wanted:
        got = paged(f"industries/{industry['id']}/careers", per_page=200)
        for career in got:
            career["industry_slug"] = industry["slug"]
        careers.extend(got)
        print(f"  careers[{industry['slug']}]: {len(got)}")
    (root / "careers.json").write_text(
        json.dumps(careers, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # ── full vocabulary index ─────────────────────────────────────────────────
    skills = bilingual(paged("skills"), paged("skills", locale="en"))
    (root / "skills-index.json").write_text(
        json.dumps(skills, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(f"  skills index: {len(skills)}")

    # ── detail (definition + proficiency levels) for referenced skills ────────
    referenced = sorted({s["skill"]["id"] for c in careers for s in c["skills"]})
    print(f"  skill detail: {len(referenced)} referenced "
          f"(~{len(referenced) * 0.7 / WORKERS / 60:.0f} min)", flush=True)

    def fetch_detail(skill_id: str) -> dict:
        detail = get(f"skills/{skill_id}")
        detail["title_en"] = get(f"skills/{skill_id}", locale="en").get("title")
        return detail

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        details = []
        for n, detail in enumerate(pool.map(fetch_detail, referenced), 1):
            details.append(detail)
            if n % 200 == 0:
                print(f"    {n}/{len(referenced)}", flush=True)
    (root / "skills-detail.json").write_text(
        json.dumps(details, ensure_ascii=False, indent=1), encoding="utf-8"
    )

    # ── manifest ──────────────────────────────────────────────────────────────
    levelled = [d for d in details if d.get("levels")]
    manifest = {
        "snapshot_date": date.today().isoformat(),
        "source": "https://api.skillmapping.in.th",
        "operator": "Office of the Permanent Secretary, MHESI (OPS) / KMITL",
        "api_version": api_info.get("version"),
        "industries_mirrored": [i["slug"] for i in wanted],
        "counts": {
            "industries": len(industries),
            "careers": len(careers),
            "skills_total": len(skills),
            "skills_referenced": len(referenced),
            "skills_with_levels": len(levelled),
        },
        "skill_types": {
            t: sum(1 for s in skills if s["type"] == t)
            for t in sorted({s["type"] for s in skills})
        },
        "fetch_seconds": round(time.time() - started, 1),
    }
    (root / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
