from app.services.analysis_context import build_analysis_context


def test_build_analysis_context_returns_ranked_budgeted_context() -> None:
    files = {
        "README.md": "# Project\n",
        "app/main.py": "import os\nimport requests\n",
        "tests/test_main.py": "import pytest\n",
    }

    context = build_analysis_context("psf/requests", files, max_chars=100)

    assert context.repository == "psf/requests"
    assert "Python" in context.language_counts
    assert "README.md" in context.important_files
    assert "app/main.py" in context.dependency_index
