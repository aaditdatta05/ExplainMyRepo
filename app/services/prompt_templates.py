from app.services.analysis_context import AnalysisContext

SYSTEM_PROMPT = (
    "You are a repository analysis assistant. "
    "Explain codebases clearly using only provided context."
)


def build_user_prompt(context: AnalysisContext) -> str:
    lines: list[str] = []
    lines.append(f"Repository: {context.repository}")
    lines.append("Languages:")
    for language, count in context.language_counts.items():
        lines.append(f"- {language}: {count}")

    lines.append("Important files:")
    for path in context.important_files[:10]:
        lines.append(f"- {path}")

    lines.append("Dependencies:")
    for path, deps in context.dependency_index.items():
        lines.append(f"- {path}: {', '.join(deps) if deps else 'none'}")

    return "\n".join(lines)
