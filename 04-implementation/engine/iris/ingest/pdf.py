"""Read a PDF into characters with their font, for the integrity gate.

PyMuPDF is used for the per-span font information, which the repair table is
keyed on: a document embeds regular and bold as separate font subsets with
independent glyph maps, and the same ASCII character can stand for a different
combining mark in each.

The extractor is *not* a variable here. poppler, PyMuPDF and xberg return
byte-identical damage on the SWU document — the defect is the PDF's missing
character map, so no reader can recover what is not in the file.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True, slots=True)
class TextLine:
    """One laid-out line, positioned in reading order and already repaired.

    `across` and `down` are the line's centre in *reading* order, so a rotated
    page needs no special handling downstream — see `_reading_axes`.
    """

    across: float
    down: float
    text: str
    page: int  # 1-based


@dataclass(frozen=True, slots=True)
class ExtractedText:
    """Parallel per-character text and font, plus per-page offsets."""

    chars: list[str]
    fonts: list[str]
    page_starts: list[int]  # index into `chars` where each page begins
    page_count: int

    @property
    def text(self) -> str:
        return "".join(self.chars)

    def page_of(self, index: int) -> int:
        """1-based page number containing a character index — the provenance
        every extracted course description carries."""
        page = 0
        for page, start in enumerate(self.page_starts, 1):
            if index < start:
                return max(1, page - 1)
        return max(1, page)


def _reading_axes(bbox, rotation: int, page_height: float) -> tuple[float, float]:
    """Map a bbox centre onto (across, down) in reading order.

    A rotated page stores coordinates in the unrotated frame, so the axis that
    reads left-to-right is not x. Every positional extractor shares this.
    """
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    if rotation == 90:
        return page_height - y, x
    if rotation == 270:
        return y, -x
    return x, y


@lru_cache(maxsize=8)
def _repaired_lines_cached(
    path: str,
) -> tuple[tuple[TextLine, ...], tuple[tuple[tuple[str, str], str], ...]]:
    lines, table = _read_repaired(path)
    return tuple(lines), tuple(table.items())


def repaired_lines(path: Path | str) -> tuple[list[TextLine], dict[tuple[str, str], str]]:
    """Lines in reading order, with the document's own glyph repair applied.

    Cached per file: learning the repair table means a full pass over the
    document, and several extractors want the same lines.
    """
    lines, table = _repaired_lines_cached(str(Path(path).resolve()))
    return list(lines), dict(table)


def _read_repaired(path: Path | str) -> tuple[list[TextLine], dict[tuple[str, str], str]]:
    """Do the work behind `repaired_lines`.

    Positional extractors — the curriculum matrix, the outcome table — read spans
    directly rather than the flat character stream, so they would otherwise miss
    the normalisation and repair the rest of the pipeline performs. `ประยุกต์`
    would reach them as `ประยุกต=`, and a verb lookup would fail on text that is
    merely damaged rather than absent.

    The repair table is learned once from the whole document, then applied
    per character with its font, which keeps a glyph meaning different things in
    the regular and bold subsets from being conflated.

    ⚠️ **Only at intrusion positions** — a character with Thai on both sides.
    Applying the table everywhere would rewrite legitimate digits: SWU's table
    maps `2` to `้`, which turns the course code `คพ242` into `คพ้4้`. The rule
    is the same one `repair.learn_and_repair` uses on the flat character stream;
    it has to be repeated here because this reader works line by line.
    """
    import pymupdf

    from iris.ingest.integrity import Verdict, diagnose
    from iris.ingest.normalise import normalise
    from iris.ingest.repair import find_intrusions, learn_and_repair

    document = extract(path)
    table: dict[tuple[str, str], str] = {}
    if diagnose(document.text).verdict is Verdict.REPAIRABLE:
        result = learn_and_repair(document.chars, document.fonts)
        table = {(rule.font, rule.glyph): rule.mark for rule in result.rules}

    lines: list[TextLine] = []
    with pymupdf.open(path) as doc:
        for number, page in enumerate(doc, 1):
            height = page.rect.height
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    chars: list[str] = []
                    fonts: list[str] = []
                    for index, span in enumerate(line["spans"]):
                        if index:
                            chars.append(" ")
                            fonts.append("")
                        chars.extend(span["text"])
                        fonts.extend([span["font"]] * len(span["text"]))

                    # Substitute only where a character has Thai on both sides.
                    for position in find_intrusions(chars):
                        mark = table.get((fonts[position], chars[position]))
                        if mark:
                            chars[position] = mark

                    text = normalise("".join(chars).strip()).text
                    if not text:
                        continue
                    across, down = _reading_axes(line["bbox"], page.rotation, height)
                    lines.append(TextLine(across, down, text, number))
    return lines, table


def extract(path: Path | str) -> ExtractedText:
    """Extract text with font attribution."""
    import pymupdf

    chars: list[str] = []
    fonts: list[str] = []
    page_starts: list[int] = []

    with pymupdf.open(path) as doc:
        for page in doc:
            page_starts.append(len(chars))
            for block in page.get_text("dict")["blocks"]:
                for line in block.get("lines", []):
                    for span in line["spans"]:
                        chars.extend(span["text"])
                        fonts.extend([span["font"]] * len(span["text"]))
                    chars.append("\n")
                    fonts.append("")
        count = doc.page_count

    return ExtractedText(chars=chars, fonts=fonts, page_starts=page_starts, page_count=count)
