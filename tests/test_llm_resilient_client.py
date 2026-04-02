import asyncio

from app.services.llm import LLMRetryConfig, ResilientLLMClient


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
