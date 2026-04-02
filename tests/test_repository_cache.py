import time

from app.services.cache import RepositoryAnalysisCache


def test_cache_set_and_get() -> None:
    cache = RepositoryAnalysisCache(ttl_seconds=60)
    payload = ("result", "md", {"ok": True})

    cache.set("repo", payload)

    assert cache.get("repo") == payload


def test_cache_expires_entries() -> None:
    cache = RepositoryAnalysisCache(ttl_seconds=0)
    cache.set("repo", ("result", "md", {"ok": True}))
    time.sleep(0.01)

    assert cache.get("repo") is None
