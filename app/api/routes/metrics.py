from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import get_metrics_registry
from app.core.observability import MetricsRegistry

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("")
def get_metrics(
    registry: Annotated[MetricsRegistry, Depends(get_metrics_registry)],
) -> dict[str, float | int]:
    snapshot = registry.snapshot()
    return {
        "total_requests": snapshot.total_requests,
        "total_errors": snapshot.total_errors,
        "average_latency_ms": snapshot.average_latency_ms,
    }
