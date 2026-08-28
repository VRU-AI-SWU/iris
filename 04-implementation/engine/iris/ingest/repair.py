"""Recover Thai combining marks that a PDF's font encoding turned into ASCII.

**The repair table is learned from the document, not hard-coded.** A table
derived from one file would not transfer to another producer's output, and the
solution design records exactly that as a risk. Instead the mapping is inferred
from evidence the document itself supplies, which means the method generalises
and every substitution can be justified.

The method, in one line: *a substituted glyph is whichever combining mark turns
the word it sits in into a real Thai word.*

Concretely, iterating until nothing new is learned:

1. Find **intrusions** — non-Thai characters sitting inside Thai words.
2. For each, try all 13 combining marks and keep those that make the token
   containing it a dictionary word.
3. Prefer the mark yielding the **longest** matching token. This is the maximal
   matching heuristic Thai segmentation already relies on, and it resolves the
   common ambiguity: `ฝ?ก` admits `ฝัก` (a pod), `ฝีก` and `ฝึก` (to practise),
   but only `ฝึก` extends to `การฝึกงาน`.
4. Vote per `(font, glyph)`. Fonts matter — a document embeds regular and bold as
   separate subsets with independent glyph maps, and the same ASCII character can
   stand for different marks in each.
5. Apply the learned table, which removes those intrusions and makes the
   remaining ones easier to read. Repeat, relaxing the ambiguity tolerance as the
   density falls.

Measured on the SWU มคอ.2 (216 pages, 4,918 intrusions): six rules learned, no
hard-coding, and the mark rate rises from 134.5 to 161.2 per 1,000 Thai
characters against a clean-document baseline of 171.0.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field

from iris.ingest.integrity import THAI_MARKS, is_thai

#: Characters either side of an intrusion that the scorer may consider.
WINDOW = 10

#: How many co-occurring intrusions a learning window may contain, per round.
#: Starts strict, relaxes as the document gets cleaner and evidence improves.
TOLERANCE_SCHEDULE = (1, 1, 2, 3, 4, 6)

#: A rule needs this many votes and this level of agreement to be adopted.
MIN_VOTES = 3
MIN_AGREEMENT = 0.75


@dataclass(frozen=True, slots=True)
class Rule:
    """One learned substitution, with the evidence that justified it."""

    font: str
    glyph: str
    mark: str
    votes: int
    agreement: float
    examples: tuple[tuple[str, str], ...] = ()  # (damaged, repaired) token pairs

    def __str__(self) -> str:
        return (
            f"{self.font.split('+')[-1]:22} {self.glyph!r} → {self.mark!r}  "
            f"{self.votes:5} votes, {self.agreement:.0%} agreement"
        )


@dataclass(frozen=True, slots=True)
class RepairResult:
    text: str
    rules: tuple[Rule, ...]
    intrusions_before: int
    intrusions_after: int
    rounds: int
    unrepaired_glyphs: dict[str, int] = field(default_factory=dict)

    @property
    def repaired(self) -> int:
        return self.intrusions_before - self.intrusions_after

    def summary(self) -> str:
        pct = self.repaired / self.intrusions_before if self.intrusions_before else 0.0
        lines = [
            f"repaired {self.repaired:,} of {self.intrusions_before:,} intrusions "
            f"({pct:.0%}) in {self.rounds} rounds using {len(self.rules)} learned rules"
        ]
        lines += [f"  {rule}" for rule in self.rules]
        if self.unrepaired_glyphs:
            top = ", ".join(f"{g!r}×{n}" for g, n in list(self.unrepaired_glyphs.items())[:6])
            lines.append(f"  unrepaired: {top}")
        return "\n".join(lines)


class _Lexicon:
    """Thai dictionary and tokeniser, loaded once.

    Imported lazily so that the integrity gate — which needs neither — stays
    dependency-light and fast.
    """

    def __init__(self) -> None:
        from pythainlp import word_tokenize
        from pythainlp.corpus import thai_words

        self._words = thai_words()
        self._tokenize = word_tokenize

    def token_at(self, window: str, position: int) -> str:
        """The token covering `position` after segmentation."""
        offset = 0
        for token in self._tokenize(window, engine="newmm"):
            if offset <= position < offset + len(token):
                return token
            offset += len(token)
        return ""

    def known(self, token: str) -> bool:
        return token in self._words


def find_intrusions(chars: list[str]) -> list[int]:
    """Indexes of non-Thai characters sitting between two Thai characters."""
    return [
        i
        for i in range(1, len(chars) - 1)
        if not is_thai(chars[i])
        and not chars[i].isspace()
        and is_thai(chars[i - 1])
        and is_thai(chars[i + 1])
    ]


def _candidates(lex: _Lexicon, chars: list[str], i: int) -> list[tuple[str, int]]:
    """`(mark, matched-token-length)` for every mark that yields a real word."""
    lo, hi = max(0, i - WINDOW), min(len(chars), i + WINDOW + 1)
    window, j = "".join(chars[lo:hi]), i - lo
    if lex.known(lex.token_at(window, j)):
        return []  # already a valid word; nothing to fix
    out = []
    for mark in THAI_MARKS:
        token = lex.token_at(window[:j] + mark + window[j + 1 :], j)
        if lex.known(token):
            out.append((mark, len(token)))
    return out


def learn_and_repair(
    chars: list[str],
    fonts: list[str] | None = None,
    *,
    seed_rules: dict[tuple[str, str], str] | None = None,
) -> RepairResult:
    """Learn a substitution table from the text, apply it, and report.

    `chars` and `fonts` are parallel per-character lists — see `pdf.py`, which
    produces them from a PDF's spans. Pass `fonts=None` to key rules on the glyph
    alone, which is the right choice for text of unknown provenance.

    `seed_rules` allows a human-verified mapping to be supplied for glyphs the
    lexicon cannot disambiguate. It is applied but still reported, so a run is
    never silently dependent on a hand-written table.
    """
    lex = _Lexicon()
    chars = list(chars)
    fonts = list(fonts) if fonts is not None else [""] * len(chars)
    if len(fonts) != len(chars):
        raise ValueError("chars and fonts must be the same length")

    intrusions_before = len(find_intrusions(chars))
    table: dict[tuple[str, str], Rule] = {}

    if seed_rules:
        for (font, glyph), mark in seed_rules.items():
            table[(font, glyph)] = Rule(font, glyph, mark, votes=0, agreement=1.0)

    rounds = 0
    for tolerance in TOLERANCE_SCHEDULE:
        rounds += 1
        indexes = find_intrusions(chars)
        if not indexes:
            break
        pending = set(indexes)

        votes: dict[tuple[str, str], Counter] = defaultdict(Counter)
        examples: dict[tuple[str, str, str], list[tuple[str, str]]] = defaultdict(list)
        for i in indexes:
            lo, hi = max(0, i - WINDOW), min(len(chars), i + WINDOW + 1)
            if sum(1 for j in range(lo, hi) if j in pending) > tolerance:
                continue
            hits = _candidates(lex, chars, i)
            if not hits:
                continue
            # Maximal matching: the longest resulting token wins.
            longest = max(length for _, length in hits)
            key = (fonts[i], chars[i])
            for mark, length in hits:
                if length == longest:
                    votes[key][mark] += 1
                    if len(examples[(*key, mark)]) < 3:
                        window, j = "".join(chars[lo:hi]), i - lo
                        examples[(*key, mark)].append(
                            (window.strip(), (window[:j] + mark + window[j + 1 :]).strip())
                        )

        learned = 0
        for key, counter in votes.items():
            if key in table:
                continue
            mark, count = counter.most_common(1)[0]
            total = sum(counter.values())
            agreement = count / total
            if count >= MIN_VOTES and agreement >= MIN_AGREEMENT:
                table[key] = Rule(
                    font=key[0],
                    glyph=key[1],
                    mark=mark,
                    votes=count,
                    agreement=agreement,
                    examples=tuple(examples[(*key, mark)]),
                )
                learned += 1

        applied = 0
        for i in indexes:
            rule = table.get((fonts[i], chars[i]))
            if rule is not None:
                chars[i] = rule.mark
                applied += 1

        if not learned and not applied:
            break

    remaining = find_intrusions(chars)
    return RepairResult(
        text="".join(chars),
        rules=tuple(sorted(table.values(), key=lambda r: (-r.votes, r.glyph))),
        intrusions_before=intrusions_before,
        intrusions_after=len(remaining),
        rounds=rounds,
        unrepaired_glyphs=dict(Counter(chars[i] for i in remaining).most_common()),
    )
