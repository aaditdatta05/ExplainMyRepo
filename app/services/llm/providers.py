import httpx


class MissingCredentialsLLMProvider:
    def __init__(self, provider_name: str, env_var_name: str) -> None:
        self._provider_name = provider_name
        self._env_var_name = env_var_name

    async def generate(self, prompt: str) -> str:
        raise RuntimeError(
            f"{self._provider_name} provider is selected but credentials are missing. "
            f"Set {self._env_var_name}."
        )


class TemplateLLMProvider:
    async def generate(self, prompt: str) -> str:
        return (
            "This repository automates codebase explanation by combining repository analysis "
            "signals with an LLM-driven summarization pipeline."
        )


class GeminiLLMProvider:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash") -> None:
        self._api_key = api_key
        self._model = model

    async def generate(self, prompt: str) -> str:
        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent"
        )
        params = {"key": self._api_key}
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt,
                        }
                    ]
                }
            ]
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(endpoint, params=params, json=payload)
            response.raise_for_status()
            data = response.json()

        candidates = data.get("candidates")
        if not isinstance(candidates, list) or not candidates:
            raise RuntimeError("Gemini response did not contain candidates.")

        content = candidates[0].get("content", {})
        parts = content.get("parts", [])
        if not isinstance(parts, list) or not parts:
            raise RuntimeError("Gemini response did not contain text parts.")

        text = parts[0].get("text")
        if not isinstance(text, str) or not text.strip():
            raise RuntimeError("Gemini response text is empty.")

        return text.strip()
