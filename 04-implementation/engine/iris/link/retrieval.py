"""Candidate retrieval over the national skill vocabulary.

Linking a course to the standard is a two-stage problem. This module is the first
stage: narrow 4,376 skills down to the few dozen an adjudicator can weigh, given
a course description. It exists as a separate stage because the literature is
consistent that **ranking is much cheaper than selection** —
[[zhang-2024-job-market-entity-linking]] reports Acc@32 roughly double Acc@1, and
[[le-2026-competency-tagging-evidence]] MRR 0.82 against micro-F1 0.57. Whatever
retrieval misses, no adjudicator can recover.

**Lexical, and deliberately first.** Dense retrieval needs an embedding model and
therefore a GPU or an API; BM25 needs neither, so it gives a measured baseline
before any inference infrastructure exists. It is also expected to *win* on the
`tools` third of the vocabulary — `Docker`, `.NET Core`, `Apache Spark` match by
their name, not by their meaning — which is why the design specifies hybrid
retrieval rather than dense alone.

**Three surface forms per skill, free.** The standard gives every entry a Thai
title, an English title and a Thai definition. That is exactly the *synonym
enhancement* [[dong-2023-out-of-kb-mention-discovery]] had to construct by hand,
and it matters here because a Thai course description may name a skill in either
language — `ภาษาเอสคิวแอล` or `SQL`.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache

from iris.snapshot import Skill, Snapshot, get_snapshot

#: BM25 parameters. The defaults from the literature; a skill entry is short and
#: uniform in length, so neither is sensitive here.
BM25_K1 = 1.2
BM25_B = 0.75

#: A definition describes a skill but is not its name, so matches there count for
#: less than matches on a title.
FIELD_WEIGHTS = {"title_th": 3.0, "title_en": 3.0, "definition": 1.0}

#: Weights for the damage-tolerant skeleton channel.
#:
#: Both channels carry the same modest weight. Raising the whole-phrase weight to
#: 3.0 was tried and made recall@10 *worse* (75 % → 67 %) on the development set
#: without rescuing the case it was meant to; the values stay uniform rather than
#: tuned, because six hand-labelled courses cannot support tuning without
#: overfitting to them.
SKELETON_PHRASE_WEIGHT = 1.0
SKELETON_PIECE_WEIGHT = 1.0

#: Skeleton tokens live in their own namespace so they cannot collide with real ones.
SKELETON_PREFIX = "\x00skel:"

#: Thai tokens shorter than this carry no discriminating signal.
MIN_TOKEN = 2

#: A skeleton shorter than this collides with far too much to be useful.
MIN_SKELETON = 3

#: Longest whole-phrase skeleton worth emitting; beyond this a phrase is prose,
#: not a name, and will match nothing.
MAX_PHRASE_SKELETON = 24

_LATIN = re.compile(r"[A-Za-z][A-Za-z0-9+#.\-]*")
_THAI_RUN = re.compile(r"[ก-๙]+")
#: A Thai phrase, allowing the single interior spaces that damage leaves behind.
_THAI_PHRASE = re.compile(r"[ก-๙]+(?:[ \t\xa0][ก-๙]+)*")


@dataclass(frozen=True, slots=True)
class Candidate:
    """One retrieved skill, with why it was retrieved."""

    skill: Skill
    score: float
    rank: int
    matched: tuple[str, ...] = ()  # the tokens that fired

    def __str__(self) -> str:
        name = self.skill.title_en or self.skill.title_th
        return f"{self.rank:3}. {self.score:6.2f}  {name}  [{self.skill.type.value}]"


def skeleton(text: str) -> str:
    """A Thai run reduced to its consonants.

    Damage that survives repair — a tone mark lost to whitespace, a karan the
    repair table could not place — changes the vowels and marks of a word but
    almost never its consonants. `เครือข ายคอมพิวเตอร=` and
    `เครือข่ายคอมพิวเตอร์` both reduce to `ครอขยคอมพวตอร`.

    Measured cost: 7.2 % of the vocabulary shares a skeleton with another entry
    (`ซอฟต์แวร์`-like generic words dominate). That is acceptable for a channel
    whose output is a candidate list an adjudicator then filters, and the
    alternative — rewriting the document — risks changing meaning, since `ไม`
    (silk) is as real a word as `ไม่` (not).
    """
    return "".join(c for c in text if "ก" <= c <= "ฮ")


def tokenize(text: str) -> list[str]:
    """Split mixed Thai/English text into comparable tokens.

    Thai has no spaces, so its runs go through a dictionary segmenter while Latin
    runs split on word boundaries. Case is folded; a course description writes
    `SQL` and a skill title writes `sql`.
    """
    if not text:
        return []
    from pythainlp import word_tokenize

    tokens: list[str] = []
    for match in _LATIN.finditer(text):
        token = match.group().lower().strip(".-")
        if len(token) >= MIN_TOKEN:
            tokens.append(token)
    for run in _THAI_RUN.findall(text):
        tokens.extend(t for t in word_tokenize(run, engine="newmm") if len(t) >= MIN_TOKEN)
    return tokens


class SkillIndex:
    """A BM25 index over every surface form of every skill in the vocabulary.

    Built once per snapshot — 4,376 entries is small enough that the whole thing
    lives in memory and needs no external service, which is the same reason the
    design rules out a vector database.
    """

    def __init__(self, snapshot: Snapshot | None = None) -> None:
        self.snapshot = snapshot or get_snapshot()
        self._skills = self.snapshot.skills
        self._postings: dict[str, dict[int, float]] = defaultdict(dict)
        self._lengths: list[float] = []

        for position, skill in enumerate(self._skills):
            weighted: Counter = Counter()
            for field, weight in FIELD_WEIGHTS.items():
                value = getattr(skill, field, None)
                if not value:
                    continue
                for token in tokenize(value):
                    weighted[token] += weight
            # Damage-tolerant channel over the Thai title.
            for token, weight in _skeleton_tokens(skill.title_th):
                weighted[token] += weight
            self._lengths.append(sum(weighted.values()) or 1.0)
            for token, count in weighted.items():
                self._postings[token][position] = count

        total = len(self._skills)
        self._average_length = sum(self._lengths) / total if total else 1.0
        self._idf = {
            token: math.log(1 + (total - len(docs) + 0.5) / (len(docs) + 0.5))
            for token, docs in self._postings.items()
        }

    def __len__(self) -> int:
        return len(self._skills)

    @property
    def vocabulary_size(self) -> int:
        """Distinct tokens across every surface form."""
        return len(self._postings)

    def search(self, text: str, *, k: int = 30) -> list[Candidate]:
        """Top-`k` skills for a course description, best first."""
        query = tokenize(text) + [token for token, _ in _skeleton_tokens(text)]
        if not query:
            return []

        scores: dict[int, float] = defaultdict(float)
        fired: dict[int, set[str]] = defaultdict(set)
        for token in set(query):
            postings = self._postings.get(token)
            if not postings:
                continue
            idf = self._idf[token]
            for position, frequency in postings.items():
                length = self._lengths[position]
                norm = 1 - BM25_B + BM25_B * length / self._average_length
                scores[position] += idf * (frequency * (BM25_K1 + 1) / (frequency + BM25_K1 * norm))
                fired[position].add(token)

        ranked = sorted(scores.items(), key=lambda item: -item[1])[:k]
        return [
            Candidate(
                skill=self._skills[position],
                score=score,
                rank=rank,
                matched=tuple(sorted(fired[position])),
            )
            for rank, (position, score) in enumerate(ranked, 1)
        ]


def _skeleton_tokens(text: str | None) -> list[tuple[str, float]]:
    """Skeletons of the Thai phrases in `text`, long enough to discriminate.

    ⚠️ Phrases are joined **across single spaces** before reduction. The damage
    this channel exists to tolerate often *is* a space — `เครือข่าย` arrives as
    `เครือข าย` — so splitting on whitespace first would break exactly the words
    the channel is meant to rescue.

    The de-spaced phrase is re-segmented so a long phrase does not collapse into
    one skeleton that matches nothing, and the whole phrase is emitted too when
    it is short enough to be a title.
    """
    if not text:
        return []
    from pythainlp import word_tokenize

    tokens: list[tuple[str, float]] = []
    for phrase in _THAI_PHRASE.findall(text):
        joined = "".join(phrase.split())
        for piece in word_tokenize(joined, engine="newmm"):
            bones = skeleton(piece)
            if len(bones) >= MIN_SKELETON:
                tokens.append((SKELETON_PREFIX + bones, SKELETON_PIECE_WEIGHT))
        whole = skeleton(joined)
        if MIN_SKELETON <= len(whole) <= MAX_PHRASE_SKELETON:
            tokens.append((SKELETON_PREFIX + whole, SKELETON_PHRASE_WEIGHT))
    return tokens


@lru_cache(maxsize=1)
def get_index() -> SkillIndex:
    """The process-wide index. Built once; a few seconds over 4,376 skills."""
    return SkillIndex()
