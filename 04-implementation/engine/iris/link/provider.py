"""One provider-blind interface over the two model backends Iris may use.

Adjudication runs either on a **local OpenAI-compatible endpoint** on
`gpu-linux-server` or on **Cloudflare Workers AI**. The pattern is taken from the
lab's Argus project, which already runs it in production, and it fits Iris better
than it fits Argus: TQF documents are public institutional records, so nothing
forces the work to stay on the machine, and a handful of programmes per year sits
inside the Workers AI free tier at ≈ $0.036 per programme.

🔴 **The provider is pinned per run. There is no mid-run fallback.** Argus switches
provider mid-case and records which model read each page; that is right for a demo
and wrong here. A programme whose 78 courses were linked by two different models is
not a reproducible analysis and cannot be compared against another programme. If a
quota is exhausted mid-run the run *fails* and requeues on the other provider from
the start — which is why `QuotaExhausted` is a distinct exception and not folded
into the retry path.

The corollary binds the evaluation: the Sprint 4 gate must measure whichever
provider and model will serve production.
"""

from __future__ import annotations

import json
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

#: Cloudflare's application-level code for *account quota exhausted*, carried
#: inside a 429 body. Ported from Argus `server/llm.ts`.
#:
#: ⚠️ It must never be retried. An ordinary 429 means "too fast, back off"; this
#: one means "the day's neurons are gone", and retrying burns the run's wall-clock
#: to arrive at the same failure.
CLOUDFLARE_QUOTA_CODE = 4006

#: Statuses worth retrying: rate limiting that is *not* quota exhaustion, and the
#: transient 5xx family.
RETRYABLE_STATUSES = frozenset({408, 429, 500, 502, 503, 504})

#: Backoff schedule in seconds, used when the response carries no `Retry-After`.
BACKOFF_SCHEDULE = (1.0, 2.0, 4.0)

#: Longest `Retry-After` worth honouring. Beyond this the run should fail and be
#: requeued rather than hold a GPU slot idle.
MAX_RETRY_AFTER = 60.0


class ProviderError(RuntimeError):
    """The provider could not answer, and retrying will not help."""


class QuotaExhausted(ProviderError):
    """The provider's allowance is spent.

    Separate from `ProviderError` because it is the one failure the caller must
    handle differently: the run is abandoned and requeued on the other provider,
    not retried on this one.
    """


@dataclass(frozen=True, slots=True)
class Completion:
    """One model response, with what it cost, who produced it, and how it ended.

    `provider` and `model` travel with the response rather than being looked up
    later, because they are recorded on `analysis_run` and a report that cannot
    say which model produced it is not reproducible.
    """

    text: str
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    latency_s: float = 0.0
    finish_reason: str = ""

    @property
    def is_truncated(self) -> bool:
        """Whether the model ran out of budget before it finished.

        ⚠️ Load-bearing. A reasoning model spends its budget in a `reasoning`
        field the OpenAI shape does not return as content, so a truncated answer
        arrives as an **empty string** — indistinguishable, downstream, from a
        model that considered the candidates and chose none. Measured on
        `qwen3:8b`: every one of six courses came back empty with
        `finish_reason: length`. Since "this course develops nothing the
        vocabulary names" is a *meaningful* output in this design, the two must
        never be conflated.
        """
        return self.finish_reason == "length" or (
            not self.text.strip() and bool(self.finish_reason)
        )

    def parse_json(self) -> Any:
        """The response as JSON, tolerating a model that wrapped it in a fence.

        Adjudication asks for a structured object; small models sometimes answer
        with ```json around it despite instruction. Recovering that is cheaper
        than discarding the whole course.
        """
        text = self.text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1].rsplit("```", 1)[0]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            start, end = text.find("{"), text.rfind("}")
            if start >= 0 and end > start:
                return json.loads(text[start : end + 1])
            raise


class Provider(ABC):
    """What the linker needs from a model backend, and nothing more."""

    name: str
    model: str

    @abstractmethod
    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        schema: dict[str, Any] | None = None,
    ) -> Completion:
        """Answer `prompt`, optionally constrained to a JSON schema."""

    def health(self) -> tuple[bool, str]:
        """Whether the backend answers at all — checked before a run starts.

        A run that dies on course 3 of 78 has wasted the ingestion; a two-second
        probe up front is worth it.
        """
        try:
            reply = self.complete("Reply with the single word: ok", max_tokens=8)
        except Exception as error:
            return False, f"{type(error).__name__}: {error}"
        return True, reply.text.strip()[:40]


class OpenAICompatible(Provider):
    """Any server speaking the OpenAI chat-completions API.

    Covers Ollama, vLLM and LM Studio alike, which is the point: dev and
    production differ only by `MODEL_SERVER_URL`.
    """

    name = "local"

    def __init__(
        self,
        base_url: str,
        model: str,
        *,
        api_key: str = "not-needed",
        timeout: float = 180.0,
        reasoning_effort: str | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.timeout = timeout
        #: Sent only when set, because a server that does not know the field may
        #: reject the whole request. `"none"` is what disables thinking on Ollama;
        #: `chat_template_kwargs.enable_thinking` and `think` were both measured
        #: to be silently ignored there.
        self.reasoning_effort = reasoning_effort

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        schema: dict[str, Any] | None = None,
    ) -> Completion:
        import httpx

        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if self.reasoning_effort:
            payload["reasoning_effort"] = self.reasoning_effort
        if schema:
            # Ollama and vLLM both accept the OpenAI structured-output shape.
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "link", "schema": schema, "strict": True},
            }

        started = time.monotonic()
        with httpx.Client(timeout=self.timeout) as client:
            response = _with_retries(
                lambda: client.post(
                    f"{self.base_url}/chat/completions",
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
            )
        body = response.json()
        usage = body.get("usage") or {}
        choice = body["choices"][0]
        return Completion(
            text=choice["message"].get("content") or "",
            provider=self.name,
            model=self.model,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_s=time.monotonic() - started,
            finish_reason=choice.get("finish_reason") or "",
        )


class WorkersAI(Provider):
    """Cloudflare Workers AI.

    Present so that a run is not blocked when `gpu-linux-server` is training for
    another project — a risk the design records, and one that has been real for
    the whole of Sprints 1–3.
    """

    name = "workers-ai"

    def __init__(
        self,
        account_id: str,
        api_token: str,
        model: str = "@cf/google/gemma-4-26b-a4b-it",
        *,
        timeout: float = 180.0,
    ) -> None:
        self.account_id = account_id
        self.api_token = api_token
        self.model = model
        self.timeout = timeout

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        schema: dict[str, Any] | None = None,
    ) -> Completion:
        import httpx

        messages = ([{"role": "system", "content": system}] if system else []) + [
            {"role": "user", "content": prompt}
        ]
        payload: dict[str, Any] = {
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if schema:
            payload["response_format"] = {"type": "json_schema", "json_schema": schema}

        url = f"https://api.cloudflare.com/client/v4/accounts/{self.account_id}/ai/run/{self.model}"
        started = time.monotonic()
        with httpx.Client(timeout=self.timeout) as client:
            response = _with_retries(
                lambda: client.post(
                    url,
                    json=payload,
                    headers={"Authorization": f"Bearer {self.api_token}"},
                )
            )
        body = response.json()
        if not body.get("success", True):
            raise ProviderError(f"workers-ai refused: {body.get('errors')}")
        result = body.get("result") or {}
        usage = result.get("usage") or {}
        return Completion(
            text=result.get("response") or "",
            provider=self.name,
            model=self.model,
            prompt_tokens=usage.get("prompt_tokens", 0),
            completion_tokens=usage.get("completion_tokens", 0),
            latency_s=time.monotonic() - started,
        )


@dataclass
class RecordingProvider(Provider):
    """A provider that answers from a script — for tests and for dry runs.

    Adjudication is the one stage that cannot be exercised deterministically
    against a real model, so the prompt construction, the schema and the parsing
    are tested through this and the model is measured separately.
    """

    replies: list[str] = field(default_factory=list)
    name: str = "recording"
    model: str = "scripted"
    prompts: list[str] = field(default_factory=list)
    finish_reason: str = "stop"

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
        schema: dict[str, Any] | None = None,
    ) -> Completion:
        self.prompts.append(prompt)
        text = self.replies.pop(0) if self.replies else "{}"
        return Completion(
            text=text,
            provider=self.name,
            model=self.model,
            finish_reason=self.finish_reason,
        )


def _with_retries(send):
    """Send a request, honouring the difference between *slow down* and *stop*.

    The distinction is the whole point of this function. A 429 carrying
    Cloudflare's `code: 4006` means the account's daily neurons are spent — no
    amount of backoff recovers it, and the run must fail so it can be requeued on
    the other provider. Any other 429, and the transient 5xx family, is worth a
    bounded retry that honours `Retry-After` when the server sends one.
    """
    last: Exception | None = None
    for attempt, pause in enumerate((*BACKOFF_SCHEDULE, None)):
        try:
            response = send()
        except Exception as error:
            last = error
            if pause is None:
                raise ProviderError(f"request failed after {attempt} retries: {error}") from error
            time.sleep(pause)
            continue

        if response.status_code < 400:
            return response

        if response.status_code == 429 and _is_quota_exhaustion(response):
            raise QuotaExhausted(
                "provider quota exhausted (Cloudflare code "
                f"{CLOUDFLARE_QUOTA_CODE}); the run must requeue on the other provider"
            )

        if response.status_code not in RETRYABLE_STATUSES or pause is None:
            raise ProviderError(f"HTTP {response.status_code}: {response.text[:200]}")

        time.sleep(_retry_after(response, default=pause))

    raise ProviderError(f"exhausted retries: {last}")


def _is_quota_exhaustion(response) -> bool:
    """Whether a 429 is *quota spent* rather than *too fast*."""
    try:
        body = response.json()
    except Exception:
        return False
    errors = body.get("errors") or []
    if isinstance(errors, list):
        return any(isinstance(e, dict) and e.get("code") == CLOUDFLARE_QUOTA_CODE for e in errors)
    return False


def _retry_after(response, *, default: float) -> float:
    """`Retry-After` in seconds, bounded — a long wait should requeue instead."""
    header = response.headers.get("retry-after")
    if not header:
        return default
    try:
        return min(float(header), MAX_RETRY_AFTER)
    except ValueError:
        return default


def get_provider(name: str | None = None) -> Provider:
    """Build the configured provider.

    Called once per run, never per course: the provider is pinned for the run and
    recorded on `analysis_run` alongside the model and the snapshot date.
    """
    from iris.config import get_settings

    settings = get_settings()
    choice = (name or os.getenv("IRIS_PROVIDER") or "local").lower()

    if choice in {"workers-ai", "workers", "cloudflare"}:
        account = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        token = os.getenv("CLOUDFLARE_API_TOKEN")
        if not account or not token:
            raise ProviderError("workers-ai needs CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN")
        model = os.getenv("IRIS_MODEL") or "@cf/google/gemma-4-26b-a4b-it"
        return WorkersAI(account, token, model)

    model = os.getenv("IRIS_MODEL") or settings.extraction_model
    if not model:
        raise ProviderError("no model configured: set IRIS_MODEL or EXTRACTION_MODEL")
    return OpenAICompatible(
        settings.model_server_url,
        model,
        reasoning_effort=os.getenv("IRIS_REASONING_EFFORT") or None,
    )
