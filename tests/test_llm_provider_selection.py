import pytest

from app.api.deps import get_llm_provider
from app.core.config import get_settings
from app.services.llm.providers import (
    GeminiLLMProvider,
    MissingCredentialsLLMProvider,
    TemplateLLMProvider,
)


def test_provider_selection_template(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXPLAIN_MY_REPO_LLM_PROVIDER", "template")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, TemplateLLMProvider)


def test_provider_selection_gemini_with_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXPLAIN_MY_REPO_LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EXPLAIN_MY_REPO_GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("EXPLAIN_MY_REPO_GEMINI_MODEL", "gemini-1.5-flash")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, GeminiLLMProvider)


def test_provider_selection_gemini_missing_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXPLAIN_MY_REPO_LLM_PROVIDER", "gemini")
    monkeypatch.setenv("EXPLAIN_MY_REPO_GEMINI_API_KEY", "")
    get_settings.cache_clear()

    provider = get_llm_provider()

    assert isinstance(provider, MissingCredentialsLLMProvider)
