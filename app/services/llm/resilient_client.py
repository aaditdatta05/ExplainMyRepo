import asyncio
from dataclasses import dataclass

from app.services.llm.provider import LLMProvider


class LLMCallError(RuntimeError):
    """Raised when an LLM call fails after all retries."""


@dataclass(slots=True)
class LLMRetryConfig:
    timeout_seconds: float = 20.0
    max_retries: int = 2
    base_backoff_seconds: float = 0.5


class ResilientLLMClient:
    def __init__(self, provider: LLMProvider, retry_config: LLMRetryConfig | None = None) -> None:
        self._provider = provider
        self._retry_config = retry_config or LLMRetryConfig()

    async def generate(self, prompt: str) -> str:
        last_exception: Exception | None = None

        for attempt in range(self._retry_config.max_retries + 1):
            try:
                return await asyncio.wait_for(
                    self._provider.generate(prompt),
                    timeout=self._retry_config.timeout_seconds,
                )
            except Exception as exc:  # noqa: BLE001 - we retry all transient failures consistently
                last_exception = exc
                if attempt >= self._retry_config.max_retries:
                    break
                await asyncio.sleep(self._retry_config.base_backoff_seconds * (2**attempt))

        raise LLMCallError("LLM call failed after retries") from last_exception
