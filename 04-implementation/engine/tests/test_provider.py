"""The provider seam, and the one distinction it exists to make.

Nearly all of this file is about a single question: when a provider says 429,
does the run back off or does it die? Getting that wrong in either direction is
expensive — retrying an exhausted quota burns the run's wall-clock to reach the
same failure, and dying on an ordinary rate limit throws away a completed
ingestion.
"""

from __future__ import annotations

import json

import httpx
import pytest

from iris.link.provider import (
    CLOUDFLARE_QUOTA_CODE,
    Completion,
    OpenAICompatible,
    ProviderError,
    QuotaExhausted,
    RecordingProvider,
    WorkersAI,
    _with_retries,
)


def _response(status: int, *, json_body=None, headers=None, text="") -> httpx.Response:
    return (
        httpx.Response(
            status_code=status,
            json=json_body,
            headers=headers or {},
            request=httpx.Request("POST", "https://example.test"),
        )
        if json_body is not None
        else httpx.Response(
            status_code=status,
            text=text,
            headers=headers or {},
            request=httpx.Request("POST", "https://example.test"),
        )
    )


# ── Quota exhaustion is not a rate limit ────────────────────────────────────


def test_cloudflare_quota_code_is_never_retried():
    """`code: 4006` inside a 429 means the day's neurons are gone."""
    calls = []

    def send():
        calls.append(1)
        return _response(429, json_body={"errors": [{"code": CLOUDFLARE_QUOTA_CODE}]})

    with pytest.raises(QuotaExhausted):
        _with_retries(send)
    assert len(calls) == 1, "quota exhaustion must fail on the first response"


def test_an_ordinary_429_is_retried(monkeypatch):
    monkeypatch.setattr("iris.link.provider.time.sleep", lambda _: None)
    replies = [
        _response(429, json_body={"errors": [{"code": 1015}]}),
        _response(200, json_body={"ok": True}),
    ]
    result = _with_retries(lambda: replies.pop(0))
    assert result.status_code == 200


def test_a_429_without_a_json_body_is_an_ordinary_rate_limit(monkeypatch):
    """A proxy's plain-text 429 must not be mistaken for quota exhaustion."""
    monkeypatch.setattr("iris.link.provider.time.sleep", lambda _: None)
    replies = [_response(429, text="Too Many Requests"), _response(200, json_body={})]
    assert _with_retries(lambda: replies.pop(0)).status_code == 200


def test_retry_after_is_honoured_but_bounded(monkeypatch):
    slept: list[float] = []
    monkeypatch.setattr("iris.link.provider.time.sleep", slept.append)
    replies = [
        _response(503, headers={"retry-after": "5"}, text=""),
        _response(503, headers={"retry-after": "9999"}, text=""),
        _response(200, json_body={}),
    ]
    _with_retries(lambda: replies.pop(0))
    assert slept[0] == 5.0
    assert slept[1] == 60.0, "an hour-long Retry-After should requeue, not block"


def test_a_client_error_is_not_retried():
    calls = []

    def send():
        calls.append(1)
        return _response(400, text="bad request")

    with pytest.raises(ProviderError):
        _with_retries(send)
    assert len(calls) == 1


def test_retries_are_bounded(monkeypatch):
    monkeypatch.setattr("iris.link.provider.time.sleep", lambda _: None)
    calls = []

    def send():
        calls.append(1)
        return _response(503, text="")

    with pytest.raises(ProviderError):
        _with_retries(send)
    assert len(calls) == 4, "three backoffs then give up"


# ── Provenance travels with the answer ──────────────────────────────────────


def test_a_completion_names_its_provider_and_model():
    """A report that cannot say which model produced it is not reproducible."""
    reply = RecordingProvider(replies=['{"selected": []}'], model="qwen3:8b").complete("x")
    assert reply.provider == "recording"
    assert reply.model == "qwen3:8b"


def test_a_fenced_json_answer_is_recovered():
    """Small models fence their JSON despite instruction; a whole course is too
    much to discard over three backticks."""
    reply = Completion(text='```json\n{"selected": [{"n": 3}]}\n```', provider="t", model="t")
    assert reply.parse_json()["selected"][0]["n"] == 3


def test_prose_around_the_json_is_recovered():
    reply = Completion(text='Sure! {"selected": []} Hope that helps.', provider="t", model="t")
    assert reply.parse_json() == {"selected": []}


def test_an_unrecoverable_answer_raises():
    with pytest.raises(json.JSONDecodeError):
        Completion(text="I cannot help with that.", provider="t", model="t").parse_json()


# ── Construction ────────────────────────────────────────────────────────────


def test_health_reports_failure_rather_than_raising():
    """A run checks health before spending an ingestion; the check must not be
    the thing that crashes it."""
    ok, detail = OpenAICompatible("http://127.0.0.1:9", "nothing").health()
    assert ok is False
    assert detail


def test_workers_ai_defaults_to_the_model_argus_measured():
    provider = WorkersAI("account", "token")
    assert provider.model.startswith("@cf/")
    assert provider.name == "workers-ai"
