from collections.abc import AsyncIterator

from app.models.analysis import AnalysisContext, ExplanationResult, ExplanationSections
from app.services.analysis.github import parse_github_repo_url
from app.services.cache import RepositoryAnalysisCache
from app.services.explanation import (
    build_grounding_citations,
    format_explanation_json,
    format_explanation_markdown,
)
from app.services.llm import ResilientLLMClient


class RepositoryAnalysisOrchestrator:
    def __init__(self, llm_client: ResilientLLMClient, cache: RepositoryAnalysisCache) -> None:
        self._llm_client = llm_client
        self._cache = cache

    async def analyze(self, repo_url: str) -> tuple[ExplanationResult, str, dict[str, object]]:
        cached = self._cache.get(repo_url)
        if cached is not None:
            result, markdown_output, structured_output = cached
            return result, markdown_output, structured_output

        owner, repo = parse_github_repo_url(repo_url)

        context = AnalysisContext(
            repo_url=repo_url,
            repo_owner=owner,
            repo_name=repo,
            important_files=["README.md", "pyproject.toml", "app/main.py"],
            dependencies=["fastapi", "pydantic-settings", "httpx"],
            detected_languages=["Python"],
        )

        overview = await self._llm_client.generate(
            "Write a concise project overview for repository "
            f"{owner}/{repo} mentioning purpose and audience."
        )
        modules = (
            "Core modules include API routes in app/api, runtime configuration in app/core, "
            "and orchestration services in app/services."
        )
        flow = (
            "The API accepts a repository URL, builds analysis context, generates sectioned "
            "explanations, then returns markdown and JSON outputs with citations."
        )

        result = ExplanationResult(
            context=context,
            sections=ExplanationSections(
                overview=overview,
                modules=modules,
                flow=flow,
            ),
            citations=build_grounding_citations(context.important_files),
        )
        markdown_output = format_explanation_markdown(result)
        structured_output = format_explanation_json(result)
        self._cache.set(repo_url, (result, markdown_output, structured_output))

        return result, markdown_output, structured_output

    async def stream_analyze(self, repo_url: str) -> AsyncIterator[dict[str, object]]:
        yield {"event": "status", "data": "validating repository url"}
        parse_github_repo_url(repo_url)

        yield {"event": "status", "data": "running analysis"}
        result, markdown_output, structured_output = await self.analyze(repo_url)

        yield {"event": "result", "data": structured_output}
        yield {
            "event": "complete",
            "data": {
                "repository_url": result.context.repo_url,
                "markdown": markdown_output,
            },
        }
