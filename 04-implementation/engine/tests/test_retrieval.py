"""Candidate retrieval over the national vocabulary.

Retrieval is the stage that bounds everything downstream: what it misses, no
adjudicator can recover. These tests pin the measured behaviour of the lexical
channel, which needs no model and therefore no GPU.
"""

from __future__ import annotations

import pytest

from iris.link import get_index, skeleton, tokenize
from iris.snapshot import SkillType

#: Six SWU courses hand-labelled during Sprint 3.
#:
#: ⚠️ **A development set, not the Sprint 4 gold standard.** One author, no
#: second annotator, no agreement statistic, and the labels are deliberately
#: narrow. It exists to fix `k` and to catch regressions — nothing measured here
#: may be reported as an evaluation result.
DEV_SET: dict[str, set[str]] = {
    "คพ242": {"sql", "relational-data-modeling", "database-design", "databases", "data-modeling"},
    "คพ241": {"algorithms", "data-structures"},
    "คพ222": {"operating-systems"},
    "คพ231": {"computer-networking"},
    "คพ112": {"object-oriented-programming-oop", "computer-programming"},
    "คพ251": {"web-development"},
}


@pytest.fixture(scope="module")
def index():
    return get_index()


# ── Tokenisation ────────────────────────────────────────────────────────────


def test_mixed_script_text_tokenises_on_both_sides():
    tokens = tokenize("การเขียนโปรแกรมด้วย Python และ SQL")
    assert "python" in tokens and "sql" in tokens
    assert any("เขียน" in t or "โปรแกรม" in t for t in tokens)


def test_tool_names_survive_their_punctuation():
    """`.NET Core` and `C#` are names; stripping their punctuation loses them."""
    assert "net" in tokenize(".NET Core") or "net.core" in tokenize(".NET Core")
    assert "c#" in tokenize("C# programming")


# ── The damage-tolerant channel ─────────────────────────────────────────────


def test_skeleton_ignores_vowels_and_marks():
    assert skeleton("เครือข่ายคอมพิวเตอร์") == skeleton("เครือขายคอมพวเตอร")


def test_skeleton_survives_the_damage_it_exists_for():
    """A tone mark lost to whitespace, and an unrepaired karan."""
    assert skeleton("เครือข ายคอมพิวเตอร=".replace(" ", "")) == skeleton("เครือข่ายคอมพิวเตอร์")


def test_damaged_thai_still_retrieves_its_skill(index):
    """The measured failure that motivated the channel.

    Before it, this text returned Storage Architecture and Rhinoceros.
    """
    damaged = "เครือข ายคอมพิวเตอร= สถาปัตยกรรมการสื่อสารข้อมูล โพรโทคอล"
    names = [(c.skill.title_en or "").lower() for c in index.search(damaged, k=20)]
    assert any("network" in n for n in names), names[:5]


# ── Retrieval quality ───────────────────────────────────────────────────────


def test_index_covers_the_whole_vocabulary(index):
    assert len(index) == 4376
    assert index.vocabulary_size > 8000  # three surface forms plus skeletons


def test_database_course_retrieves_its_skills(index):
    """CP242, verified by hand against the page in the design review."""
    text = (
        "ระบบฐานข้อมูล การสร้างแบบจำลองและออกแบบฐานข้อมูลเชิงสัมพันธ์ "
        "การทำให้เป็นบรรทัดฐาน ภาษาเอสคิวแอล การทำดัชนี กระบวนการสอบถามข้อมูล"
    )
    slugs = [c.skill.slug for c in index.search(text, k=10)]
    assert "sql" in slugs
    assert any("data-modeling" in s for s in slugs)


def test_tool_skills_are_reachable_lexically(index):
    """The `tools` third of the vocabulary matches by name, not by meaning —
    the reason the design specifies hybrid retrieval rather than dense alone."""
    hits = index.search("การพัฒนาแอปพลิเคชันด้วย Docker และ Kubernetes", k=15)
    assert any(c.skill.type is SkillType.TOOLS for c in hits)


def test_candidates_carry_their_rank_and_evidence(index):
    hits = index.search("ภาษาเอสคิวแอล ฐานข้อมูล", k=5)
    assert [c.rank for c in hits] == [1, 2, 3, 4, 5]
    assert all(c.matched for c in hits)
    assert hits[0].score >= hits[-1].score


def test_empty_query_returns_nothing_rather_than_everything(index):
    assert index.search("", k=10) == []
    assert index.search("...", k=10) == []
