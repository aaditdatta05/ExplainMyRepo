from app.models.analysis import ExplanationResult


def format_explanation_markdown(result: ExplanationResult) -> str:
    citation_lines = "\n".join(
        f"- `{citation.file_path}`: {citation.reason}" for citation in result.citations
    )

    return (
        f"# Repository Summary: {result.context.repo_owner}/{result.context.repo_name}\n\n"
        f"## Overview\n{result.sections.overview}\n\n"
        f"## Modules\n{result.sections.modules}\n\n"
        f"## Flow\n{result.sections.flow}\n\n"
        f"## Grounding Citations\n{citation_lines}\n"
    )


def format_explanation_json(result: ExplanationResult) -> dict[str, object]:
    return {
        "repository": {
            "url": result.context.repo_url,
            "owner": result.context.repo_owner,
            "name": result.context.repo_name,
        },
        "sections": {
            "overview": result.sections.overview,
            "modules": result.sections.modules,
            "flow": result.sections.flow,
        },
        "citations": [
            {"file_path": citation.file_path, "reason": citation.reason}
            for citation in result.citations
        ],
    }
