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
from pathlib import Path


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
