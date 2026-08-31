"""Decide which retrieved candidates a course actually develops.

Retrieval ranks; this stage decides. It is deliberately framed as a **constrained
selection** — *"which of these 30 candidates does this course develop?"* — rather
than open generation, for two reasons that are measured rather than assumed:

- [[zhang-2024-job-market-entity-linking]] reports Acc@32 roughly double Acc@1,
  which is what makes a shortlist worth adjudicating at all.
- A selection task is materially easier for a small local model than free-form
  extraction, and its output is constrained to valid skill IDs *by construction*.
  That matters here because `gpu-linux-server` is shared and the design sizes for
  ~15 GB, not 24.

**Three invariants this module enforces, none of which the model is trusted with.**

1. **A selection outside the candidate list is rejected, not repaired.** Candidates
   are presented as numbers; a number out of range is a hallucination and is
   dropped with a reason recorded.
2. **Every accepted link carries an evidence span that is verified to occur in the
   course text.** This is non-negotiable #6 — a committee member will point at a
   link and ask where it came from. A span the model invented is not provenance,
   so it is checked by substring against the description and the link is demoted
   to `unverified` when it fails.
3. **"None of these" is a first-class answer — and is never confused with a
   model that failed to answer.** A truncated or unparseable response yields
   `failed=True`, which is counted apart from a genuine empty selection. A
   general-education course may legitimately develop nothing the vocabulary
   names, and — measured 2026-08-31 —
   so may a core course whose subject the standard omits entirely
   (สถาปัตยกรรมคอมพิวเตอร์, คณิตศาสตร์ไม่ต่อเนื่อง). Modelling absence as an explicit
   output beats similarity thresholding: [[dong-2023-out-of-kb-mention-discovery]].
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Any

from iris.link.provider import Completion, Provider
from iris.link.retrieval import Candidate

#: Candidates offered per course. Fixed at the lexical channel's saturation point
#: (recall@30 = 75 %, unchanged at @20) rather than chosen — see Sprint 3.
DEFAULT_K = 30

#: A definition's median length is 149 characters; truncating past this keeps a
#: 30-candidate prompt near the measured ~3,970-token budget per course.
MAX_DEFINITION = 240

#: Shortest evidence span worth accepting. Below this a "span" is a fragment that
#: could occur anywhere and proves nothing.
MIN_EVIDENCE = 4

SYSTEM_PROMPT = (
    "You are helping a Thai university curriculum committee map course descriptions "
    "to a national skill standard. You select from a fixed list; you never invent "
    "skills. If none of the listed skills is genuinely developed by the course, you "
    "say so. Answer only with JSON."
)

#: The response shape. `strict` schemas are honoured by Ollama, vLLM and Workers AI
#: alike, which is why the seam can present one interface over all three.
RESPONSE_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "selected": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "n": {"type": "integer"},
                    "evidence": {"type": "string"},
                },
                "required": ["n", "evidence"],
                "additionalProperties": False,
            },
        },
        "out_of_vocabulary": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["selected", "out_of_vocabulary"],
    "additionalProperties": False,
}


@dataclass(frozen=True, slots=True)
class SkillLink:
    """One accepted link, with everything needed to defend it.

    `retrieval_rank` travels with the link because it is the cheapest available
    diagnostic: a link the adjudicator only ever finds at rank 28 tells you the
    retrieval stage is the weak half, and a `k` that was too small would have
    silently lost it.
    """

    skill_id: str
    slug: str
    title: str
    evidence: str
    retrieval_rank: int
    evidence_verified: bool
    course_code: str | None = None
    page: int | None = None

    def __str__(self) -> str:
        mark = "✓" if self.evidence_verified else "~"
        return f"  {mark} {self.title}  ({self.slug}, rank {self.retrieval_rank})"


@dataclass(frozen=True, slots=True)
class Adjudication:
    """What the model made of one course, including what it refused to link."""

    links: tuple[SkillLink, ...]
    out_of_vocabulary: tuple[str, ...]
    rejected: tuple[str, ...] = ()
    completion: Completion | None = None
    course_code: str | None = None
    failed: bool = False

    @property
    def is_zero_link(self) -> bool:
        """The course develops nothing the vocabulary names.

        🔴 **A valid, recorded outcome — and only when the model actually said
        so.** A general-education course legitimately links to nothing, and the
        share of zero-link courses is a reportable coverage statistic about the
        standard. That statistic is worthless if a model that ran out of tokens
        also lands here, so a failed adjudication is excluded.
        """
        return not self.links and not self.failed


@dataclass
class AdjudicationReport:
    courses: int = 0
    linked: int = 0
    zero_link: int = 0
    failed: int = 0
    links: int = 0
    verified: int = 0
    rejected: int = 0
    out_of_vocabulary: int = 0
    prompt_tokens: int = 0
    seconds: float = 0.0
    notes: list[str] = field(default_factory=list)

    def summary(self) -> str:
        share = f"{self.verified}/{self.links}" if self.links else "0/0"
        failed = f", {self.failed} FAILED" if self.failed else ""
        return (
            f"{self.links} links across {self.linked} of {self.courses} courses "
            f"({self.zero_link} zero-link{failed}, {share} with verified evidence, "
            f"{self.rejected} rejected, {self.out_of_vocabulary} out-of-vocabulary) "
            f"— {self.prompt_tokens:,} prompt tokens, {self.seconds:.1f}s"
        )


def build_prompt(text: str, candidates: list[Candidate]) -> str:
    """Render one course and its shortlist as a numbered selection task.

    Numbers rather than slugs: a small model copies `17` reliably and
    `relational-data-modeling` less so, and a number outside `1..k` is
    structurally detectable as a hallucination where a plausible-looking slug is
    not.
    """
    lines = [
        "COURSE DESCRIPTION (Thai):",
        " ".join(text.split()),
        "",
        "CANDIDATE SKILLS:",
    ]
    for candidate in candidates:
        skill = candidate.skill
        name = skill.title_th
        if skill.title_en and skill.title_en != skill.title_th:
            name = f"{skill.title_th} / {skill.title_en}"
        entry = f"{candidate.rank}. {name}"
        if skill.definition:
            definition = " ".join(skill.definition.split())[:MAX_DEFINITION]
            entry += f" — {definition}"
        lines.append(entry)

    lines += [
        "",
        "TASK. Select only the candidates this course genuinely develops in its "
        "students. A candidate that is merely mentioned, or that belongs to the "
        "same field without being taught, must not be selected.",
        "",
        "For each selection give `evidence`: a short phrase copied EXACTLY from the "
        "course description above that shows the course develops it. Do not "
        "paraphrase, translate, or write the phrase yourself — copy it.",
        "",
        "If the course develops a skill that is NOT in the candidate list, name it "
        "in `out_of_vocabulary` (Thai is fine). If none of the candidates fits, "
        "return an empty `selected` list — that is a valid and expected answer for "
        "general-education and theory courses.",
        "",
        'Answer as JSON: {"selected": [{"n": <number>, "evidence": "<copied phrase>"}], '
        '"out_of_vocabulary": ["<name>"]}',
    ]
    return "\n".join(lines)


def adjudicate(
    text: str,
    candidates: list[Candidate],
    provider: Provider,
    *,
    course_code: str | None = None,
    page: int | None = None,
    max_tokens: int = 1200,
) -> Adjudication:
    """Ask the model which candidates the course develops, and verify the answer."""
    if not candidates:
        return Adjudication((), (), course_code=course_code)

    completion = provider.complete(
        build_prompt(text, candidates),
        system=SYSTEM_PROMPT,
        schema=RESPONSE_SCHEMA,
        max_tokens=max_tokens,
    )
    if completion.is_truncated:
        # Measured on qwen3:8b before `reasoning_effort` was set: a reasoning
        # model spends its whole budget in a field the OpenAI shape does not
        # return as content, so the answer arrives as an empty string. Reporting
        # that as "this course develops no named skill" would be a fabrication.
        return Adjudication(
            (),
            (),
            rejected=(f"truncated before answering ({completion.finish_reason})",),
            completion=completion,
            course_code=course_code,
            failed=True,
        )
    try:
        answer = completion.parse_json()
    except Exception:
        return Adjudication(
            (),
            (),
            rejected=("unparseable response",),
            completion=completion,
            course_code=course_code,
            failed=True,
        )
    return _accept(answer, text, candidates, completion, course_code, page)


def _accept(
    answer: Any,
    text: str,
    candidates: list[Candidate],
    completion: Completion,
    course_code: str | None,
    page: int | None,
) -> Adjudication:
    """Turn a model answer into links, dropping everything unverifiable."""
    by_rank = {candidate.rank: candidate for candidate in candidates}
    links: list[SkillLink] = []
    rejected: list[str] = []
    seen: set[str] = set()

    for item in (answer or {}).get("selected") or []:
        if not isinstance(item, dict):
            rejected.append(f"malformed selection: {item!r:.40}")
            continue
        try:
            number = int(item.get("n"))
        except (TypeError, ValueError):
            rejected.append(f"non-numeric selection: {item.get('n')!r:.20}")
            continue

        candidate = by_rank.get(number)
        if candidate is None:
            # A number outside the shortlist. The model did not choose from the
            # list it was given, so there is nothing to link to.
            rejected.append(f"candidate {number} was not offered")
            continue
        if candidate.skill.slug in seen:
            continue
        seen.add(candidate.skill.slug)

        evidence = " ".join(str(item.get("evidence") or "").split())
        links.append(
            SkillLink(
                skill_id=candidate.skill.id,
                slug=candidate.skill.slug,
                title=candidate.skill.title_en or candidate.skill.title_th,
                evidence=evidence,
                retrieval_rank=candidate.rank,
                evidence_verified=verify_evidence(evidence, text),
                course_code=course_code,
                page=page,
            )
        )

    residue = tuple(
        " ".join(str(name).split())
        for name in ((answer or {}).get("out_of_vocabulary") or [])
        if str(name).strip()
    )
    return Adjudication(
        links=tuple(links),
        out_of_vocabulary=residue,
        rejected=tuple(rejected),
        completion=completion,
        course_code=course_code,
    )


def verify_evidence(evidence: str, text: str) -> bool:
    """Whether the span the model quoted really occurs in the course text.

    ⚠️ **Compared with Thai whitespace and combining marks folded away.** The
    documents Iris reads have damaged text layers: Sprint 2 leaves one class of
    damage unrepaired, where a tone mark became a space, because rewriting it can
    change meaning. A model reading `เครือข าย` will quote it back as `เครือข่าย` —
    correctly. Comparing raw would reject that quote and lose real provenance, so
    both sides are reduced to their base characters before comparison.

    This is a deliberately *weaker* check than exact substring, and the weakening
    is bounded: it tolerates whitespace and diacritics, nothing else. A span the
    model composed from elsewhere still fails.
    """
    if len(evidence.strip()) < MIN_EVIDENCE:
        return False
    return _fold(evidence) in _fold(text)


_COMBINING = re.compile(r"[ัิ-ฺ็-๎]")


def _fold(text: str) -> str:
    """Reduce Thai text to what damage cannot alter: base characters, no spaces."""
    stripped = _COMBINING.sub("", unicodedata.normalize("NFC", text))
    return "".join(stripped.split()).lower()
