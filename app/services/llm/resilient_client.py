import asyncio
from dataclasses import dataclass
from collections.abc import Sequence

import httpx

from app.services.llm.provider import LLMProvider


class LLMCallError(RuntimeError):
    """Raised when an LLM call fails after all retries."""


class LLMRateLimitError(LLMCallError):
    """Raised when the upstream LLM provider reports rate limiting."""


@dataclass(slots=True)
class LLMRetryConfig:
    timeout_seconds: float = 20.0
    max_retries: int = 2
    base_backoff_seconds: float = 0.5


class ResilientLLMClient:
    def __init__(
        self,
        provider: LLMProvider,
        retry_config: LLMRetryConfig | None = None,
        fallback_providers: Sequence[LLMProvider] | None = None,
    ) -> None:
        self._providers = [provider, *(fallback_providers or [])]
        self._retry_config = retry_config or LLMRetryConfig()

    async def generate(self, prompt: str) -> str:
        last_exception: Exception | None = None

        for provider in self._providers:
            for attempt in range(self._retry_config.max_retries + 1):
                try:
                    return await asyncio.wait_for(
                        provider.generate(prompt),
                        timeout=self._retry_config.timeout_seconds,
                    )
                except Exception as exc:  # noqa: BLE001 - retry and fallback handle mixed failures
                    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 429:
                        raise LLMRateLimitError(
                            "LLM provider rate limit exceeded. Please retry shortly."
                        ) from exc
                    last_exception = exc
                    if attempt >= self._retry_config.max_retries:
                        break
                    await asyncio.sleep(self._retry_config.base_backoff_seconds * (2**attempt))

        raise LLMCallError("LLM call failed after retries across all providers") from last_exception
