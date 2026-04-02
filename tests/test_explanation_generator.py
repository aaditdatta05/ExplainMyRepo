from app.services.explanation_generator import ExplanationGenerator
from app.services.llm_provider import StubLLMProvider


def test_generate_from_files_builds_explanation() -> None:
    generator = ExplanationGenerator(provider=StubLLMProvider())

    result = generator.generate_from_files(
        repository="psf/requests",
        file_contents={
            "README.md": "# requests",
            "app/main.py": "import os",
        },
        max_chars=200,
    )

    assert result.repository == "psf/requests"
    assert "Stub explanation" in result.explanation
