from dataclasses import dataclass
from time import time


@dataclass(slots=True)
class _CacheEntry:
    expires_at: float
    value: tuple[object, str, dict[str, object]]


class RepositoryAnalysisCache:
    def __init__(self, ttl_seconds: int = 300) -> None:
        self._ttl_seconds = ttl_seconds
        self._store: dict[str, _CacheEntry] = {}

    def get(self, key: str) -> tuple[object, str, dict[str, object]] | None:
        entry = self._store.get(key)
        if entry is None:
            return None

        if time() >= entry.expires_at:
            self._store.pop(key, None)
            return None

        return entry.value

    def set(self, key: str, value: tuple[object, str, dict[str, object]]) -> None:
        self._store[key] = _CacheEntry(
            expires_at=time() + self._ttl_seconds,
            value=value,
        )

    def clear(self) -> None:
        self._store.clear()
