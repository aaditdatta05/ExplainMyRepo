from app.services.llm_provider import LLMRequest, StubLLMProvider


def test_stub_provider_returns_response() -> None:
    provider = StubLLMProvider()
    response = provider.generate(LLMRequest(system_prompt="system", user_prompt="hello world"))

    assert "Stub explanation" in response.content
    assert "hello world" in response.content
