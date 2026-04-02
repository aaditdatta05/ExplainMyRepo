import re
from pathlib import Path

IMPORT_RE = re.compile(r"^\s*import\s+([a-zA-Z0-9_\.]+)", re.MULTILINE)
FROM_IMPORT_RE = re.compile(r"^\s*from\s+([a-zA-Z0-9_\.]+)\s+import\s+", re.MULTILINE)
REQUIRE_RE = re.compile(r"require\(['\"]([^'\"]+)['\"]\)")
ESM_IMPORT_RE = re.compile(r"from\s+['\"]([^'\"]+)['\"]")


def extract_dependencies(file_path: str, source: str) -> list[str]:
    suffix = Path(file_path).suffix.lower()
    deps: set[str] = set()

    if suffix == ".py":
        deps.update(match.group(1).split(".")[0] for match in IMPORT_RE.finditer(source))
        deps.update(match.group(1).split(".")[0] for match in FROM_IMPORT_RE.finditer(source))
    elif suffix in {".js", ".ts", ".tsx", ".jsx"}:
        deps.update(match.group(1) for match in REQUIRE_RE.finditer(source))
        deps.update(match.group(1) for match in ESM_IMPORT_RE.finditer(source))

    return sorted(dep for dep in deps if dep)


def build_dependency_index(files: dict[str, str]) -> dict[str, list[str]]:
    return {path: extract_dependencies(path, content) for path, content in sorted(files.items())}
