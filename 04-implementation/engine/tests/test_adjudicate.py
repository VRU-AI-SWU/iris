"""Adjudication — and the three things the model is not trusted with.

The model chooses; this module decides what the choice is worth. Each test below
corresponds to a way a model answer can be wrong in a way that would otherwise
reach a curriculum committee as if it were fact.
"""

from __future__ import annotations

import json

from iris.link import RecordingProvider, adjudicate, build_prompt, verify_evidence
from iris.link.retrieval import Candidate
from iris.snapshot import get_snapshot

DESCRIPTION = (
    "ระบบฐานข้อมูล การสร้างแบบจำลองและออกแบบฐานข้อมูลเชิงสัมพันธ์ "
    "การทำให้เป็นบรรทัดฐาน ภาษาเอสคิวแอล การทำดัชนีและกระบวนการสอบถามข้อมูล"
)


def _candidates(n: int = 5) -> list[Candidate]:
    skills = get_snapshot().skills[:n]
    return [Candidate(skill=s, score=10.0 - i, rank=i + 1) for i, s in enumerate(skills)]


def _reply(selected, out_of_vocabulary=()) -> str:
    return json.dumps({"selected": selected, "out_of_vocabulary": list(out_of_vocabulary)})


# ── 1. A selection outside the shortlist is rejected, not repaired ──────────


def test_a_candidate_number_that_was_not_offered_is_rejected():
    provider = RecordingProvider(replies=[_reply([{"n": 99, "evidence": "ภาษาเอสคิวแอล"}])])
    result = adjudicate(DESCRIPTION, _candidates(5), provider)
    assert result.links == ()
    assert "99" in result.rejected[0]


def test_a_valid_selection_becomes_a_link_carrying_its_retrieval_rank():
    candidates = _candidates(5)
    provider = RecordingProvider(replies=[_reply([{"n": 3, "evidence": "ภาษาเอสคิวแอล"}])])
    result = adjudicate(DESCRIPTION, candidates, provider, course_code="คพ242")
    assert len(result.links) == 1
    link = result.links[0]
    assert link.slug == candidates[2].skill.slug
    assert link.retrieval_rank == 3
    assert link.course_code == "คพ242"


def test_the_same_skill_selected_twice_links_once():
    provider = RecordingProvider(
        replies=[_reply([{"n": 2, "evidence": "ฐานข้อมูล"}, {"n": 2, "evidence": "ฐานข้อมูล"}])]
    )
    assert len(adjudicate(DESCRIPTION, _candidates(5), provider).links) == 1


# ── 2. Evidence is verified against the course text ─────────────────────────


def test_a_quoted_span_that_occurs_in_the_text_verifies():
    assert verify_evidence("ภาษาเอสคิวแอล", DESCRIPTION)


def test_a_span_the_model_composed_does_not_verify():
    """The failure that would put an indefensible link in front of a committee."""
    assert not verify_evidence("การเขียนโปรแกรมเชิงวัตถุด้วยภาษาจาวา", DESCRIPTION)


def test_evidence_verifies_through_the_damage_sprint_2_left_alone():
    """Sprint 2 does not repair a tone mark that became a space, because `ไม` and
    `ไม่` are both real words. A model reading `เครือข าย` quotes back `เครือข่าย`
    — correctly — and that must not be scored as a fabrication."""
    damaged = "หลักการของเครือข ายคอมพิวเตอร และโพรโทคอล"
    assert verify_evidence("เครือข่ายคอมพิวเตอร์", damaged)


def test_a_too_short_span_proves_nothing():
    assert not verify_evidence("การ", DESCRIPTION)
    assert not verify_evidence("", DESCRIPTION)


def test_an_unverifiable_span_still_links_but_is_marked():
    """Demoted, not dropped: retrieval and adjudication may both be right while
    the model paraphrased its evidence, and discarding that loses a real link."""
    provider = RecordingProvider(replies=[_reply([{"n": 1, "evidence": "ไม่ได้อยู่ในข้อความนี้เลย"}])])
    result = adjudicate(DESCRIPTION, _candidates(5), provider)
    assert len(result.links) == 1
    assert result.links[0].evidence_verified is False


# ── 3. "None of these" is a first-class answer ──────────────────────────────


def test_an_empty_selection_is_a_valid_outcome_not_an_error():
    result = adjudicate(DESCRIPTION, _candidates(5), RecordingProvider(replies=[_reply([])]))
    assert result.is_zero_link
    assert result.rejected == ()


def test_out_of_vocabulary_skills_are_recorded_separately():
    provider = RecordingProvider(replies=[_reply([], ["สถาปัตยกรรมคอมพิวเตอร์"])])
    result = adjudicate(DESCRIPTION, _candidates(5), provider)
    assert result.out_of_vocabulary == ("สถาปัตยกรรมคอมพิวเตอร์",)


def test_an_unparseable_answer_is_recorded_with_a_reason():
    provider = RecordingProvider(replies=["I'm sorry, I can't do that."])
    result = adjudicate(DESCRIPTION, _candidates(5), provider)
    assert result.links == ()
    assert result.rejected == ("unparseable response",)


def test_no_candidates_means_no_model_call():
    provider = RecordingProvider(replies=[_reply([{"n": 1, "evidence": "x"}])])
    assert adjudicate(DESCRIPTION, [], provider).links == ()
    assert provider.prompts == [], "an empty shortlist must not cost a model call"


# ── The prompt ──────────────────────────────────────────────────────────────


def test_the_prompt_numbers_candidates_by_retrieval_rank():
    prompt = build_prompt(DESCRIPTION, _candidates(3))
    assert "1. " in prompt and "3. " in prompt
    assert DESCRIPTION.split()[0] in prompt


def test_the_prompt_asks_for_a_copied_span_not_a_paraphrase():
    prompt = build_prompt(DESCRIPTION, _candidates(3))
    assert "copy" in prompt.lower()
    assert "paraphrase" in prompt.lower()


def test_the_prompt_states_that_an_empty_answer_is_allowed():
    """Without this the model invents a link rather than return nothing, and
    general-education courses acquire skills they do not teach."""
    assert "empty" in build_prompt(DESCRIPTION, _candidates(3)).lower()


# ── A model that failed to answer is not a course that develops nothing ─────


def test_a_truncated_answer_is_a_failure_not_a_zero_link_course():
    """Measured on `qwen3:8b` before `reasoning_effort` was set: a reasoning model
    spends its whole budget in a field the OpenAI shape does not return as
    content, so all six development-set courses came back as empty strings with
    `finish_reason: length`. Counting those as "develops no named skill" would
    have put a fabricated coverage statistic in the paper."""
    provider = RecordingProvider(replies=[""], finish_reason="length")
    result = adjudicate(DESCRIPTION, _candidates(5), provider)
    assert result.failed is True
    assert result.is_zero_link is False, "a failure must not be counted as coverage"
    assert "truncated" in result.rejected[0]


def test_an_unparseable_answer_is_also_a_failure():
    result = adjudicate(DESCRIPTION, _candidates(5), RecordingProvider(replies=["nope"]))
    assert result.failed is True
    assert result.is_zero_link is False


def test_a_genuine_empty_selection_is_not_a_failure():
    result = adjudicate(DESCRIPTION, _candidates(5), RecordingProvider(replies=[_reply([])]))
    assert result.failed is False
    assert result.is_zero_link is True
