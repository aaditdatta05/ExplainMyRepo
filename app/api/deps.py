from app.core.config import get_settings
from app.core.observability import MetricsRegistry
from app.services.analysis.orchestrator import RepositoryAnalysisOrchestrator
from app.services.cache import RepositoryAnalysisCache
from app.services.llm import LLMRetryConfig, ResilientLLMClient
from app.services.llm.providers import TemplateLLMProvider

_metrics_registry = MetricsRegistry()
_analysis_cache: RepositoryAnalysisCache | None = None


def get_metrics_registry() -> MetricsRegistry:
    return _metrics_registry


def get_analysis_cache() -> RepositoryAnalysisCache:
    global _analysis_cache

    if _analysis_cache is None:
        _analysis_cache = RepositoryAnalysisCache(
            ttl_seconds=get_settings().cache_ttl_seconds,
        )
    return _analysis_cache


def get_analysis_orchestrator() -> RepositoryAnalysisOrchestrator:
    settings = get_settings()

    client = ResilientLLMClient(
        provider=TemplateLLMProvider(),
        retry_config=LLMRetryConfig(
            timeout_seconds=settings.llm_timeout_seconds,
            max_retries=settings.llm_max_retries,
            base_backoff_seconds=settings.llm_base_backoff_seconds,
        ),
    )
    return RepositoryAnalysisOrchestrator(
        llm_client=client,
        cache=get_analysis_cache(),
    )
