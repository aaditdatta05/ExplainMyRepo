from app.services.analysis_context import AnalysisContext
from app.services.prompt_templates import build_user_prompt


def test_build_user_prompt_contains_context_sections() -> None:
    context = AnalysisContext(
        repository="octocat/hello-world",
        language_counts={"Python": 3},
        important_files=["README.md", "app/main.py"],
        dependency_index={"app/main.py": ["fastapi"]},
        included_files=["README.md"],
        excluded_files=[],
    )

    prompt = build_user_prompt(context)

    assert "Repository: octocat/hello-world" in prompt
    assert "Languages:" in prompt
    assert "Important files:" in prompt
    assert "Dependencies:" in prompt
