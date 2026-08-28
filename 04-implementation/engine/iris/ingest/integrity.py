"""Thai text-layer integrity diagnostic.

Thai text extracted from institutional PDFs is frequently corrupted in ways that
are invisible to a naive parser: extraction succeeds, returns plausible-looking
Thai, and has silently lost or substituted combining marks. Two failure modes are
measured in `03-solution-design/data-feasibility.md`, on real มคอ.2 documents:

- **substitution** — marks stacked above a consonant fall into font-private glyph
  slots with no `ToUnicode` entry and extract as ASCII (`ข้อมูล` → `ข2อมูล`).
  Reversible; see `repair.py`.
- **loss** — `ำ` collapses to `า` throughout, with nothing to distinguish it from
  an original `า`. Not reversible from the text layer.

Neither raises an error anywhere in the stack. poppler, PyMuPDF and xberg return
byte-identical damage on the SWU document, because the defect is the PDF's
missing character map, not the reader's handling of it. A generic document
quality score does not catch it either — xberg reports 1.0 on a document whose
karan is 99 % destroyed.

This module is therefore the gate every document passes before ingestion, and it
must run again after any repair or vision re-extraction.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from enum import StrEnum

#: Thai combining marks: above-vowels, below-vowels, tone marks, thanthakhat.
THAI_MARKS = "ัิีึืุู็่้๊๋์ํ"

#: Marks measured as intact in the damaged SWU document — vowels survive.
ROBUST_MARKS = "ัิีึืุู"

#: Marks measured as damaged — the upper register: tone marks and karan.
FRAGILE_MARKS = "็่้๊๋์"

#: Marks per 1,000 Thai characters in a clean document. Measured on the KU
#: มคอ.2, whose text layer is undamaged in this respect (data-feasibility.md).
CLEAN_BASELINE = 171.0

#: Per-mark rate per 1,000 Thai characters in the same clean document.
#:
#: ⚠️ **Diagnostic detail, not a verdict driver.** Mark rates depend on a
#: document's vocabulary as well as its integrity — a computer-science curriculum
#: uses karan far more than a general one (`คอมพิวเตอร์`, `ซอฟต์แวร์`), so a rate
#: below this baseline may mean different content rather than lost marks. The
#: verdict uses the *total* rate and the *intrusion count*, both of which are
#: robust to vocabulary. Per-mark retention is reported because it localises the
#: damage for a human, not because it decides anything.
CLEAN_MARK_RATES: dict[str, float] = {
    "ั": 24.30,
    "ิ": 35.71,
    "ี": 13.71,
    "ึ": 2.62,
    "ื": 9.51,
    "ุ": 7.98,
    "ู": 8.39,
    "็": 2.89,
    "่": 24.35,
    "้": 23.31,
    "๊": 0.05,
    "๋": 0.00,
    "์": 18.17,
}

#: Sara am. Its complete absence indicates collapse to `า` — lossy, and not
#: repairable from the text layer.
SARA_AM = "ำ"

#: Thai characters required before absence of `ำ` may be read as collapse.
#: The inference is statistical, not logical: a short or vocabulary-narrow
#: passage can legitimately contain none (`คอมพิวเตอร์ ซอฟต์แวร์
#: อิเล็กทรอนิกส์` has no ำ at all). `ำ` occurs about 7.6 times per 1,000 Thai
#: characters in the SWU document, so absence across this many is decisive
#: while absence across a paragraph is not.
SARA_AM_MIN_THAI = 5_000


class Verdict(StrEnum):
    """What may be done with a document's text layer."""

    CLEAN = "clean"  # use it
    REPAIRABLE = "repairable"  # substitution damage; repair.py can reverse it
    REPAIRED = "repaired"  # was repairable, and the repair brought it back
    LOSSY = "lossy"  # information is gone; re-extract with a vision model
    UNUSABLE = "unusable"  # not enough Thai to judge, or damage beyond both


def is_thai(ch: str) -> bool:
    return "฀" <= ch <= "๿"


@dataclass(frozen=True, slots=True)
class IntegrityReport:
    """The diagnostic, in full. Recorded on the programme and shown to the user."""

    verdict: Verdict
    thai_chars: int
    mark_rate: float  # marks per 1,000 Thai characters
    mark_rates: dict[str, float] = field(default_factory=dict)
    retention: dict[str, float] = field(default_factory=dict)  # vs CLEAN_MARK_RATES
    intrusions: int = 0  # non-Thai characters sitting inside Thai words
    intrusion_glyphs: dict[str, int] = field(default_factory=dict)
    sara_am_count: int = 0
    thai_ratio: float = 0.0  # guards the vision path's language-bias failure
    notes: tuple[str, ...] = ()

    @property
    def usable(self) -> bool:
        """Whether ingestion may proceed on this text."""
        return self.verdict in (Verdict.CLEAN, Verdict.REPAIRED)

    def summary(self) -> str:
        head = (
            f"{self.verdict.value.upper()}: {self.mark_rate:.1f} marks per 1,000 Thai "
            f"characters (clean baseline {CLEAN_BASELINE:.0f}), {self.thai_chars:,} Thai chars"
        )
        return head + ("\n  " + "\n  ".join(self.notes) if self.notes else "")


def _intrusions(text: str) -> Counter:
    """Non-Thai, non-space characters with Thai on both sides.

    A substituted mark always sits inside a Thai word, so this is where the
    damage shows up — and the glyph histogram is what `repair.py` learns from.
    """
    found: Counter = Counter()
    for i in range(1, len(text) - 1):
        ch = text[i]
        if is_thai(ch) or ch.isspace():
            continue
        if is_thai(text[i - 1]) and is_thai(text[i + 1]):
            found[ch] += 1
    return found


def diagnose(text: str, *, min_thai_chars: int = 500) -> IntegrityReport:
    """Classify a document's Thai text layer.

    The statistic is deliberately simple — a rate, compared against a measured
    baseline — because it must be cheap enough to run on every document, and
    auditable enough that a rejection can be explained to whoever supplied the file.
    """
    thai_chars = sum(1 for c in text if is_thai(c))
    thai_ratio = thai_chars / len(text) if text else 0.0

    if thai_chars < min_thai_chars:
        return IntegrityReport(
            verdict=Verdict.UNUSABLE,
            thai_chars=thai_chars,
            mark_rate=0.0,
            thai_ratio=thai_ratio,
            notes=(
                f"only {thai_chars} Thai characters — too little to judge. "
                "A scanned document with no text layer looks like this.",
            ),
        )

    per_1k = {m: text.count(m) / thai_chars * 1000 for m in CLEAN_MARK_RATES}
    mark_rate = sum(per_1k.values())
    retention = {m: (per_1k[m] / base if base > 0 else 1.0) for m, base in CLEAN_MARK_RATES.items()}

    intrusion_counts = _intrusions(text)
    intrusions = sum(intrusion_counts.values())
    sara_am = text.count(SARA_AM)

    notes: list[str] = []

    # ── Sara am collapse: lossy, and not recoverable from the text layer ─────
    if sara_am == 0 and thai_chars >= SARA_AM_MIN_THAI:
        notes.append(
            "no ำ (sara am) anywhere — it has collapsed to า throughout. "
            "Nothing distinguishes an original า from a collapsed ำ, so this is "
            "lossy: re-extract with a vision model."
        )
        return IntegrityReport(
            verdict=Verdict.LOSSY,
            thai_chars=thai_chars,
            mark_rate=mark_rate,
            mark_rates=per_1k,
            retention=retention,
            intrusions=intrusions,
            intrusion_glyphs=dict(intrusion_counts.most_common()),
            sara_am_count=sara_am,
            thai_ratio=thai_ratio,
            notes=tuple(notes),
        )

    if sara_am == 0:
        notes.append(
            f"no ำ found, but only {thai_chars:,} Thai characters — too few to "
            f"distinguish collapse from narrow vocabulary (threshold "
            f"{SARA_AM_MIN_THAI:,})."
        )

    # Localise the damage for a human. Reported, never decisive — see the note
    # on CLEAN_MARK_RATES.
    for m in sorted(FRAGILE_MARKS, key=lambda m: retention.get(m, 1.0)):
        if CLEAN_MARK_RATES[m] > 1 and retention.get(m, 1.0) < 0.6:
            notes.append(f"{m!r} at {retention[m]:.0%} of the clean-document rate")

    # ── Verdict, on the two vocabulary-robust signals ────────────────────────
    # `intrusions` is direct evidence of substitution: an ASCII character inside
    # a Thai word is not something a correctly-encoded document produces.
    intrusion_rate = intrusions / thai_chars * 1000
    rate_ratio = mark_rate / CLEAN_BASELINE

    if intrusion_rate < 1.0 and rate_ratio >= 0.90:
        verdict = Verdict.CLEAN
    elif intrusion_rate >= 5.0:
        verdict = Verdict.REPAIRABLE
        notes.append(
            f"{intrusions:,} substituted glyphs inside Thai words "
            f"({intrusion_rate:.1f} per 1,000 Thai chars): "
            f"{', '.join(f'{g!r}×{n}' for g, n in intrusion_counts.most_common(5))} — "
            "substitution rather than deletion, so a repair table can reverse it."
        )
    elif rate_ratio >= 0.90:
        verdict = Verdict.REPAIRED
        notes.append(
            f"mark rate is {rate_ratio:.0%} of the clean baseline with only "
            f"{intrusions:,} residual intrusions — usable."
        )
    else:
        verdict = Verdict.LOSSY
        notes.append(
            f"mark rate is {rate_ratio:.0%} of the clean baseline but only {intrusions:,} "
            "substituted glyphs remain to explain it — the marks appear deleted rather "
            "than substituted, so no table can recover them."
        )

    return IntegrityReport(
        verdict=verdict,
        thai_chars=thai_chars,
        mark_rate=mark_rate,
        mark_rates=per_1k,
        retention=retention,
        intrusions=intrusions,
        intrusion_glyphs=dict(intrusion_counts.most_common()),
        sara_am_count=sara_am,
        thai_ratio=thai_ratio,
        notes=tuple(notes),
    )
