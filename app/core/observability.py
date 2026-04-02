from dataclasses import dataclass
from time import perf_counter

from fastapi import Request


@dataclass(slots=True)
class MetricsSnapshot:
    total_requests: int
    total_errors: int
    average_latency_ms: float


class MetricsRegistry:
    def __init__(self) -> None:
        self._total_requests = 0
        self._total_errors = 0
        self._total_latency_ms = 0.0

    def record(self, *, status_code: int, latency_ms: float) -> None:
        self._total_requests += 1
        self._total_latency_ms += latency_ms
        if status_code >= 400:
            self._total_errors += 1

    def snapshot(self) -> MetricsSnapshot:
        average = 0.0
        if self._total_requests:
            average = self._total_latency_ms / self._total_requests

        return MetricsSnapshot(
            total_requests=self._total_requests,
            total_errors=self._total_errors,
            average_latency_ms=round(average, 3),
        )


async def metrics_middleware(request: Request, call_next, registry: MetricsRegistry):
    started = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - started) * 1000
    registry.record(status_code=response.status_code, latency_ms=elapsed_ms)
    return response
