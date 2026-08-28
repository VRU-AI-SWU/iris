"""Restore Thai characters that a PDF's text layer split or decomposed.

Distinct from `repair.py`, and run before it. Repair reverses a *substitution* —
one character standing in for another — and needs a table learned from the
document. Normalisation reverses a *structural* break, where the character's
identity is recoverable from Thai orthography alone, so it needs no evidence and
no model.

Both patterns concern `ำ` (sara am), which producers mishandle in two ways:

| Pattern | Producer seen | Recovery |
|---|---|---|
| `ํ` + `า` — nikhahit plus sara aa | Adobe Acrobat (SU: 1,467) | compose |
| consonant + space + `า` — a gap where the mark belongs | MS Word (CMU: 728, KU: 135) | close it |

**The second rule is safe because of Thai orthography, not statistics.** `า` is a
dependent vowel: it cannot begin a syllable, so it cannot follow a word boundary.
A space before `า` is therefore always an artefact.

Unicode normalisation does not help — `ำ` (U+0E33) has no canonical decomposition,
so NFC leaves `ํ` + `า` untouched.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

#: `ํ` (nikhahit, U+0E4D) followed by `า` (sara aa) is a decomposed `ำ`.
DECOMPOSED_SARA_AM = re.compile("ํา")

#: A Thai consonant, whitespace, then `า`. The whitespace occupies the position
#: where `ำ` should be. The class includes U+00A0, which PDF text layers emit.
SPLIT_SARA_AM = re.compile(r"([ก-ฮ])[ \t ]+(า)")


@dataclass(frozen=True, slots=True)
class NormaliseResult:
    text: str
    composed: int  # ํ + า  →  ำ
    rejoined: int  # consonant + space + า  →  consonant + ำ

    @property
    def total(self) -> int:
        return self.composed + self.rejoined

    def summary(self) -> str:
        if not self.total:
            return "no sara am normalisation needed"
        parts = []
        if self.composed:
            parts.append(f"{self.composed:,} decomposed ํ+า composed")
        if self.rejoined:
            parts.append(f"{self.rejoined:,} split consonant-space-า rejoined")
        return "sara am: " + ", ".join(parts)


def normalise(text: str) -> NormaliseResult:
    """Restore `ำ` wherever the text layer broke it apart."""
    composed = len(DECOMPOSED_SARA_AM.findall(text))
    text = DECOMPOSED_SARA_AM.sub("ำ", text)

    rejoined = len(SPLIT_SARA_AM.findall(text))
    text = SPLIT_SARA_AM.sub(lambda m: m.group(1) + "ำ", text)

    return NormaliseResult(text=text, composed=composed, rejoined=rejoined)


def normalise_chars(
    chars: list[str], fonts: list[str]
) -> tuple[list[str], list[str], NormaliseResult]:
    """Normalise parallel character and font lists, keeping them aligned.

    Both patterns *shorten* the text, so the font list is filtered to match.
    """
    text = "".join(chars)
    result = normalise(text)
    if not result.total:
        return chars, fonts, result

    out_chars: list[str] = []
    out_fonts: list[str] = []
    i = 0
    n = len(chars)
    while i < n:
        # ํ + า  →  ำ
        if chars[i] == "ํ" and i + 1 < n and chars[i + 1] == "า":
            out_chars.append("ำ")
            out_fonts.append(fonts[i])
            i += 2
            continue
        # consonant + space(s) + า  →  consonant + ำ
        if "ก" <= chars[i] <= "ฮ":
            j = i + 1
            while j < n and chars[j] in " \t ":
                j += 1
            if j > i + 1 and j < n and chars[j] == "า":
                out_chars.extend([chars[i], "ำ"])
                out_fonts.extend([fonts[i], fonts[i]])
                i = j + 1
                continue
        out_chars.append(chars[i])
        out_fonts.append(fonts[i])
        i += 1

    return (
        out_chars,
        out_fonts,
        NormaliseResult(
            text="".join(out_chars), composed=result.composed, rejoined=result.rejoined
        ),
    )
