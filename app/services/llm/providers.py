class TemplateLLMProvider:
    async def generate(self, prompt: str) -> str:
        return (
            "This repository automates codebase explanation by combining repository analysis "
            "signals with an LLM-driven summarization pipeline."
        )
