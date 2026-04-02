from dataclasses import dataclass

from app.services.context_budget import apply_context_budget
from app.services.dependency_graph import build_dependency_index
from app.services.file_scoring import rank_important_files
from app.services.language_detection import classify_files_by_language


@dataclass(frozen=True)
class AnalysisContext:
    repository: str
    language_counts: dict[str, int]
    important_files: list[str]
    dependency_index: dict[str, list[str]]
    included_files: list[str]
    excluded_files: list[str]


def build_analysis_context(
    repository: str,
    file_contents: dict[str, str],
    max_chars: int = 12000,
) -> AnalysisContext:
    paths = sorted(file_contents.keys())
    language_counts = classify_files_by_language(paths)

    ranked = rank_important_files(paths, limit=min(20, len(paths)))
    ranked_paths = [item.path for item in ranked]

    budget = apply_context_budget(ranked_paths, file_contents, max_chars=max_chars)
    dependency_index = build_dependency_index(
        {path: file_contents[path] for path in budget.selected_paths}
    )

    return AnalysisContext(
        repository=repository,
        language_counts=language_counts,
        important_files=ranked_paths,
        dependency_index=dependency_index,
        included_files=budget.selected_paths,
        excluded_files=budget.dropped_paths,
    )
