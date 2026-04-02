from dataclasses import dataclass


@dataclass(frozen=True)
class ContextBudgetResult:
    selected_paths: list[str]
    dropped_paths: list[str]
    consumed_chars: int


def apply_context_budget(
    paths: list[str],
    file_contents: dict[str, str],
    max_chars: int,
) -> ContextBudgetResult:
    selected: list[str] = []
    dropped: list[str] = []
    consumed = 0

    for path in paths:
        content = file_contents.get(path, "")
        cost = len(content)
        if consumed + cost > max_chars:
            dropped.append(path)
            continue

        selected.append(path)
        consumed += cost

    return ContextBudgetResult(
        selected_paths=selected,
        dropped_paths=dropped,
        consumed_chars=consumed,
    )
