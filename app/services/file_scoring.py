from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ScoredFile:
    path: str
    score: int


KEYWORD_SCORES = {
    "readme": 20,
    "main": 8,
    "app": 7,
    "config": 7,
    "settings": 7,
    "pyproject": 6,
    "requirements": 6,
    "dockerfile": 6,
    "workflow": 5,
    "test": 3,
}


def score_file_importance(path: str) -> int:
    normalized = path.lower().replace("\\", "/")
    name = Path(normalized).name

    score = 1
    for keyword, value in KEYWORD_SCORES.items():
        if keyword in normalized or keyword in name:
            score += value

    return score


def rank_important_files(paths: list[str], limit: int = 10) -> list[ScoredFile]:
    scored = [ScoredFile(path=path, score=score_file_importance(path)) for path in paths]
    scored.sort(key=lambda item: (-item.score, item.path))
    return scored[:limit]
