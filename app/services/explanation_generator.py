from dataclasses import dataclass

from app.services.analysis_context import AnalysisContext, build_analysis_context
from app.services.llm_provider import LLMProvider, LLMRequest
from app.services.prompt_templates import SYSTEM_PROMPT, build_user_prompt


@dataclass(frozen=True)
class ExplanationResult:
    repository: str
    explanation: str


class ExplanationGenerator:
    def __init__(self, provider: LLMProvider) -> None:
        self.provider = provider

    def generate_from_context(self, context: AnalysisContext) -> ExplanationResult:
        request = LLMRequest(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=build_user_prompt(context),
        )
        response = self.provider.generate(request)
        return ExplanationResult(repository=context.repository, explanation=response.content)

    def generate_from_files(
        self,
        repository: str,
        file_contents: dict[str, str],
        max_chars: int = 12000,
    ) -> ExplanationResult:
        context = build_analysis_context(
            repository=repository,
            file_contents=file_contents,
            max_chars=max_chars,
        )
        return self.generate_from_context(context)
