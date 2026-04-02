import pytest

from app.core.config import get_settings


@pytest.fixture(autouse=True)
def force_template_provider(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("EXPLAIN_MY_REPO_LLM_PROVIDER", "template")
    monkeypatch.setenv("EXPLAIN_MY_REPO_GEMINI_API_KEY", "")
    monkeypatch.setenv("EXPLAIN_MY_REPO_OPENAI_API_KEY", "")
    get_settings.cache_clear()
