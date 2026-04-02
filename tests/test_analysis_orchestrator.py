import asyncio

from app.services.analysis.orchestrator import RepositoryAnalysisOrchestrator
from app.services.cache import RepositoryAnalysisCache


class CountingLLMClient:
    def __init__(self, response: str) -> None:
        self.response = response
        self.calls = 0

    async def generate(self, prompt: str) -> str:
        self.calls += 1
        return self.response


def test_analyze_uses_single_llm_call_and_parses_sections() -> None:
    client = CountingLLMClient(
        '{"overview":"Overview text","modules":"Modules text","flow":"Flow text"}'
    )
    orchestrator = RepositoryAnalysisOrchestrator(
        llm_client=client,
        cache=RepositoryAnalysisCache(ttl_seconds=300),
    )

    result, _, _ = asyncio.run(orchestrator.analyze("https://github.com/psf/requests"))

    assert client.calls == 1
    assert result.sections.overview == "Overview text"
    assert result.sections.modules == "Modules text"
    assert result.sections.flow == "Flow text"


def test_analyze_falls_back_to_raw_response_when_non_json() -> None:
    client = CountingLLMClient("plain response")
    orchestrator = RepositoryAnalysisOrchestrator(
        llm_client=client,
        cache=RepositoryAnalysisCache(ttl_seconds=300),
    )

    result, _, _ = asyncio.run(orchestrator.analyze("https://github.com/psf/requests"))

    assert client.calls == 1
    assert result.sections.overview == "plain response"
    assert result.sections.modules == "plain response"
    assert result.sections.flow == "plain response"
