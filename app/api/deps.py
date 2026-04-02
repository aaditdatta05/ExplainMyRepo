from app.core.config import get_settings
from app.services.analysis.orchestrator import RepositoryAnalysisOrchestrator
from app.services.llm import LLMRetryConfig, ResilientLLMClient
from app.services.llm.providers import TemplateLLMProvider


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
    return RepositoryAnalysisOrchestrator(llm_client=client)
