from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class LLMRequest:
    system_prompt: str
    user_prompt: str


@dataclass(frozen=True)
class LLMResponse:
    content: str


class LLMProvider(Protocol):
    def generate(self, request: LLMRequest) -> LLMResponse:
        ...


class StubLLMProvider:
    def generate(self, request: LLMRequest) -> LLMResponse:
        summary = request.user_prompt[:200].strip()
        return LLMResponse(content=f"Stub explanation:\n{summary}")
