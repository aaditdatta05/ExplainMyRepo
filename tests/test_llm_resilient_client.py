import asyncio

import httpx

from app.services.llm import LLMRateLimitError, LLMRetryConfig, ResilientLLMClient


class FlakyProvider:
    def __init__(self) -> None:
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        if self.calls < 3:
            raise RuntimeError("temporary failure")
        return "ok"


class SlowProvider:
    async def generate(self, prompt: str) -> str:
        await asyncio.sleep(0.05)
        return "late"


class AlwaysFailProvider:
    async def generate(self, prompt: str) -> str:
        raise RuntimeError("primary down")


class HealthyFallbackProvider:
    async def generate(self, prompt: str) -> str:
        return "fallback-ok"


class RateLimitedProvider:
    async def generate(self, prompt: str) -> str:
        request = httpx.Request("POST", "https://example.test")
        response = httpx.Response(status_code=429, request=request)
        raise httpx.HTTPStatusError("rate limited", request=request, response=response)


def test_retries_then_succeeds() -> None:
    client = ResilientLLMClient(
        provider=FlakyProvider(),
        retry_config=LLMRetryConfig(timeout_seconds=1.0, max_retries=2, base_backoff_seconds=0.0),
    )

    output = asyncio.run(client.generate("hello"))

    assert output == "ok"


def test_times_out_and_raises() -> None:
    client = ResilientLLMClient(
        provider=SlowProvider(),
        retry_config=LLMRetryConfig(timeout_seconds=0.001, max_retries=0, base_backoff_seconds=0.0),
    )

    try:
        asyncio.run(client.generate("hello"))
        raise AssertionError("Expected timeout failure")
    except Exception as exc:  # noqa: BLE001
        assert "LLM call failed" in str(exc)


def test_fallback_provider_succeeds_after_primary_failure() -> None:
    client = ResilientLLMClient(
        provider=AlwaysFailProvider(),
        fallback_providers=[HealthyFallbackProvider()],
        retry_config=LLMRetryConfig(timeout_seconds=1.0, max_retries=1, base_backoff_seconds=0.0),
    )

    output = asyncio.run(client.generate("hello"))

    assert output == "fallback-ok"


def test_rate_limit_raises_without_fallback() -> None:
    client = ResilientLLMClient(
        provider=RateLimitedProvider(),
        fallback_providers=[HealthyFallbackProvider()],
        retry_config=LLMRetryConfig(timeout_seconds=1.0, max_retries=2, base_backoff_seconds=0.0),
    )

    try:
        asyncio.run(client.generate("hello"))
        raise AssertionError("Expected rate-limit error")
    except LLMRateLimitError:
        pass
