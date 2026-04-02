import time

from app.models.analysis import AnalysisContext, ExplanationResult, ExplanationSections
from app.services.cache import RepositoryAnalysisCache


def _build_result() -> ExplanationResult:
    return ExplanationResult(
        context=AnalysisContext(
            repo_url="https://github.com/psf/requests",
            repo_owner="psf",
            repo_name="requests",
        ),
        sections=ExplanationSections(
            overview="overview",
            modules="modules",
            flow="flow",
        ),
        citations=[],
    )


def test_cache_set_and_get() -> None:
    cache = RepositoryAnalysisCache(ttl_seconds=60)
    structured: dict[str, object] = {"ok": True}
    payload = (_build_result(), "md", structured)

    cache.set("repo", payload)

    assert cache.get("repo") == payload


def test_cache_expires_entries() -> None:
    cache = RepositoryAnalysisCache(ttl_seconds=0)
    structured: dict[str, object] = {"ok": True}
    cache.set("repo", (_build_result(), "md", structured))
    time.sleep(0.01)

    assert cache.get("repo") is None
