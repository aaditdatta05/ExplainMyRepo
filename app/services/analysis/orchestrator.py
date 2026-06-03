import json
import shutil # Used for cleaning up temp directories
import tempfile # Used for creating temp directories
# without these , temp files created during analysis won't be cleaned up, leading to disk space issues over time.
from collections.abc import AsyncIterator
from pathlib import Path

from app.models.analysis import AnalysisContext, ExplanationResult, ExplanationSections
from app.services.analysis.github import parse_github_repo_url
from app.services.analysis_context import build_analysis_context
from app.services.cache import RepositoryAnalysisCache
from app.services.explanation import (
    build_grounding_citations,
    format_explanation_json,
    format_explanation_markdown,
)
from app.services.file_tree import scan_repository_tree
from app.services.github_client import GitHubClient
from app.services.llm import ResilientLLMClient
from app.services.repo_fetcher import RepoFetcher
from app.services.repo_url import RepoRef


class RepositoryAnalysisOrchestrator:
    def __init__(
        self,
        llm_client: ResilientLLMClient,
        cache: RepositoryAnalysisCache,
        github_token: str | None = None,
    ) -> None:
        self._llm_client = llm_client
        self._cache = cache
        self._github_token = github_token

    async def analyze(self, repo_url: str) -> tuple[ExplanationResult, str, dict[str, object]]:
        cached = self._cache.get(repo_url)
        if cached is not None:
            return cached

        owner, repo = parse_github_repo_url(repo_url)

        workspace = Path(tempfile.mkdtemp())
        try:
            result, markdown_output, structured_output = await self._run_analysis(
                repo_url=repo_url,
                owner=owner,
                repo=repo,
                workspace=workspace,
            )
        finally:
            shutil.rmtree(workspace, ignore_errors=True)

        self._cache.set(repo_url, (result, markdown_output, structured_output))
        return result, markdown_output, structured_output

    async def _run_analysis(
        self,
        repo_url: str,
        owner: str,
        repo: str,
        workspace: Path,
    ) -> tuple[ExplanationResult, str, dict[str, object]]:
        with GitHubClient(token=self._github_token) as gh:
            repo_meta = gh.get_repository(owner, repo)
            branch = repo_meta.default_branch

        fetcher = RepoFetcher(workspace=workspace)
        fetched = fetcher.fetch(RepoRef(owner=owner, name=repo, branch=branch))

        nodes = scan_repository_tree(fetched.local_path)
        file_contents: dict[str, str] = {}
        for node in nodes:
            full_path = fetched.local_path / node.path
            try:
                file_contents[node.path] = full_path.read_text(
                    encoding="utf-8", errors="ignore"
                )
            except OSError:
                continue

        analysis_ctx = build_analysis_context(
            repository=f"{owner}/{repo}",
            file_contents=file_contents,
            max_chars=12000,
        )

        context = AnalysisContext(
            repo_url=repo_url,
            repo_owner=owner,
            repo_name=repo,
            important_files=analysis_ctx.important_files,
            dependencies=list(
                {dep for deps in analysis_ctx.dependency_index.values() for dep in deps}
            ),
            detected_languages=list(analysis_ctx.language_counts.keys()),
        )

        from app.services.prompt_templates import build_user_prompt
        prompt = (
            "You are a repository analysis assistant. "
            "Return strict JSON only with keys: overview, modules, flow. "
            "Each value must be a clear specific paragraph about THIS repository. "
            "Do not include markdown fences or extra text.\n\n"
            + build_user_prompt(analysis_ctx)
        )

        response = await self._llm_client.generate(prompt)
        overview, modules, flow = self._parse_sections(response)

        result = ExplanationResult(
            context=context,
            sections=ExplanationSections(
                overview=overview,
                modules=modules,
                flow=flow,
            ),
            citations=build_grounding_citations(analysis_ctx.included_files),
        )

        return result, format_explanation_markdown(result), format_explanation_json(result)

    @staticmethod
    def _parse_sections(response: str) -> tuple[str, str, str]:
        try:
            payload = json.loads(response)
            overview = str(payload.get("overview", "")).strip()
            modules = str(payload.get("modules", "")).strip()
            flow = str(payload.get("flow", "")).strip()
            if overview and modules and flow:
                return overview, modules, flow
        except json.JSONDecodeError:
            pass

        fallback = response.strip()
        if not fallback:
            fallback = "Repository analysis is temporarily unavailable."
        return fallback, fallback, fallback

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