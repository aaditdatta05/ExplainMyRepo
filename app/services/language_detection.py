from pathlib import Path

EXTENSION_LANGUAGE_MAP = {
    ".py": "Python",
    ".js": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".jsx": "JavaScript",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".md": "Markdown",
    ".json": "JSON",
    ".yml": "YAML",
    ".yaml": "YAML",
    ".toml": "TOML",
    ".sh": "Shell",
}


def detect_language(file_path: str) -> str:
    suffix = Path(file_path).suffix.lower()
    return EXTENSION_LANGUAGE_MAP.get(suffix, "Unknown")


def classify_files_by_language(paths: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for file_path in paths:
        language = detect_language(file_path)
        counts[language] = counts.get(language, 0) + 1
    return dict(sorted(counts.items(), key=lambda item: item[0]))
