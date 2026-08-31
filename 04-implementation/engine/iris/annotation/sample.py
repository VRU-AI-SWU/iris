"""Draw the Sprint 4 stratified annotation sample, and write the workbook.

The gate needs ~50 courses spread across core, elective and general education, and
it needs the same 50 every time it is drawn — a gold standard that shifts between
runs cannot anchor a published number. So the sample is **seeded and recorded**,
and re-running with the same programme, snapshot and seed reproduces it exactly.

**How a course gets its stratum.** `iris.ingest.structure` reads the programme's
own numbered course listing, which is where the มคอ.2 says what is core and what is
elective. That listing does not name every course the catalogue describes — SWU
lists 46 of its 73 — so the remainder is resolved by **elimination**, and the
elimination is only sound because the document validates it: the credit check shows
`2.1 วิชาแกน` claiming 12 credits and yielding exactly 12, so the required categories
are listed exhaustively. A described course absent from all of them is therefore not
required. Every such course is flagged `by_elimination` in the workbook so an
annotator can see which label was read and which was inferred.

**The workbook is a spreadsheet on purpose.** The Sprint 4 plan calls for a minimal
review surface — *"a spreadsheet or CLI, not the Sprint 9 screen"* — because the
point is to test the annotation protocol before any interface is designed. It is
written UTF-8 with a BOM so Excel opens Thai correctly on a Windows machine, which
is what the annotators will use.
"""

from __future__ import annotations

import csv
import hashlib
import random
from dataclasses import dataclass, field
from pathlib import Path

#: The three strata the Sprint 4 sampling plan names, in workbook order.
STRATA = ("core", "elective", "general-education")

#: Target sample size. The plan says "~50 courses"; the split follows each stratum's
#: share of the programme, subject to the floor below.
TARGET = 50

#: No stratum may fall below this, however small its share. A stratum with two
#: courses in the sample cannot support any claim about that stratum, and general
#: education is exactly the group whose zero-link rate the design wants to report.
MIN_PER_STRATUM = 8

#: Seed for the draw. Fixed and recorded rather than random, because the annotated
#: set is committed as a reusable benchmark and must be reproducible from the
#: programme, the snapshot date and this number alone.
SEED = 20260831


@dataclass(frozen=True, slots=True)
class SampledCourse:
    code: str
    title_th: str
    title_en: str
    credits: float
    description: str
    stratum: str
    category: str  # the document's own label, e.g. "2.2 วิชาบังคับ"
    by_elimination: bool
    page: int | None


@dataclass
class SampleReport:
    programme: str
    seed: int
    described: int = 0
    categorised: int = 0
    by_elimination: int = 0
    population: dict[str, int] = field(default_factory=dict)
    drawn: dict[str, int] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def summary(self) -> str:
        pop = " · ".join(f"{s} {self.population.get(s, 0)}" for s in STRATA)
        got = " · ".join(f"{s} {self.drawn.get(s, 0)}" for s in STRATA)
        return (
            f"{self.described} described courses ({self.categorised} placed by the "
            f"document, {self.by_elimination} by elimination)\n"
            f"  population: {pop}\n"
            f"  sample:     {got}   total {sum(self.drawn.values())}   seed {self.seed}"
        )


def draw_sample(
    pdf: Path | str,
    *,
    target: int = TARGET,
    seed: int = SEED,
) -> tuple[list[SampledCourse], SampleReport]:
    """Draw the stratified sample for one programme."""
    from iris.ingest.structure import extract_structure
    from iris.link.pipeline import read_courses

    pdf = Path(pdf)
    courses = read_courses(pdf)
    placed, _ = extract_structure(pdf)

    population: list[SampledCourse] = []
    for course in courses:
        code = course.code.replace(" ", "")
        category = placed.get(code)
        population.append(
            SampledCourse(
                code=course.code,
                title_th=course.title,
                title_en="",
                credits=0.0,
                description=" ".join(course.text.split()),
                stratum=category.stratum if category else "elective",
                category=f"{category.number} {category.label}" if category else "—",
                by_elimination=category is None,
                page=course.page,
            )
        )

    report = SampleReport(programme=pdf.stem, seed=seed)
    report.described = len(population)
    report.categorised = sum(1 for c in population if not c.by_elimination)
    report.by_elimination = sum(1 for c in population if c.by_elimination)

    buckets: dict[str, list[SampledCourse]] = {s: [] for s in STRATA}
    for course in population:
        buckets.setdefault(course.stratum, []).append(course)
    report.population = {s: len(buckets[s]) for s in STRATA}

    sizes = {s: len(buckets[s]) for s in STRATA}
    quotas = _quotas(sizes, target)
    for stratum, size in sizes.items():
        if size < MIN_PER_STRATUM:
            report.notes.append(
                f"{stratum}: the floor is {MIN_PER_STRATUM} but the programme describes "
                f"only {size} such courses — all {size} are taken and the stratum is "
                "under-powered. Say so wherever a per-stratum figure is reported."
            )
    rng = random.Random(seed)
    drawn: list[SampledCourse] = []
    for stratum in STRATA:
        pool = sorted(buckets[stratum], key=lambda c: c.code)
        drawn.extend(rng.sample(pool, min(quotas[stratum], len(pool))))
    report.drawn = {s: sum(1 for c in drawn if c.stratum == s) for s in STRATA}

    return sorted(drawn, key=lambda c: (STRATA.index(c.stratum), c.code)), report


def _quotas(sizes: dict[str, int], target: int) -> dict[str, int]:
    """Proportional split, with a floor, summing to `target`.

    Proportional so the sample reflects the programme, floored so no stratum is too
    small to say anything about — general education is a tenth of a CS curriculum but
    the design reports its zero-link rate, and a sample of three cannot carry that.
    """
    total = sum(sizes.values()) or 1
    quotas = {s: max(MIN_PER_STRATUM, round(target * n / total)) for s, n in sizes.items()}
    quotas = {s: min(q, sizes[s]) for s, q in quotas.items()}
    # Trim or top up the largest stratum so the total lands on target.
    while sum(quotas.values()) != target:
        movable = [
            s
            for s in STRATA
            if (sum(quotas.values()) > target and quotas[s] > MIN_PER_STRATUM)
            or (sum(quotas.values()) < target and quotas[s] < sizes[s])
        ]
        if not movable:
            break
        biggest = max(movable, key=lambda s: quotas[s])
        quotas[biggest] += 1 if sum(quotas.values()) < target else -1
    return quotas


def write_workbook(
    courses: list[SampledCourse],
    report: SampleReport,
    out: Path | str,
    *,
    annotator: str = "",
) -> Path:
    """Write one annotator's blank workbook.

    Blank on purpose. The annotator fills the skill, evidence and level columns
    before seeing any model output — rule 2 of the guideline, and the rule whose
    violation made Sprint 3's precision figure wrong.
    """
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    header = [
        "ลำดับ",
        "รหัสวิชา",
        "ชื่อวิชา",
        "หมวด",
        "ชั้น",
        "หน้าต้นทาง",
        "คำอธิบายรายวิชา",
        "ทักษะ (รหัสหรือชื่อ)",
        "ข้อความหลักฐาน (คัดลอก)",
        "ระดับ (พื้นฐาน/ปานกลาง/สูง)",
        "ทักษะนอกคลัง",
        "หมายเหตุ",
    ]
    # utf-8-sig: Excel on Windows reads Thai correctly only with the BOM.
    with out.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [f"# {report.programme} · seed {report.seed} · ผู้ประเมิน: {annotator or '____'}"]
        )
        writer.writerow(["# กรอกคอลัมน์ทักษะ/หลักฐาน/ระดับ ก่อนเห็นผลของระบบ · หนึ่งวิชามีได้หลายแถว"])
        writer.writerow(header)
        for index, course in enumerate(courses, 1):
            label = course.category + (" (โดยการคัดออก)" if course.by_elimination else "")
            writer.writerow(
                [
                    index,
                    course.code,
                    course.title_th,
                    label,
                    _stratum_th(course.stratum),
                    course.page or "",
                    course.description,
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
            )
    return out


def _stratum_th(stratum: str) -> str:
    return {
        "core": "วิชาแกน/บังคับ",
        "elective": "วิชาเลือก",
        "general-education": "ศึกษาทั่วไป",
    }.get(stratum, stratum)


def fingerprint(courses: list[SampledCourse]) -> str:
    """A short digest of the drawn sample, for recording alongside results."""
    joined = "|".join(c.code for c in courses)
    return hashlib.sha256(joined.encode()).hexdigest()[:12]
