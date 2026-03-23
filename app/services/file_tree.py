from dataclasses import dataclass
from pathlib import Path

DEFAULT_IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "dist",
    "build",
    "__pycache__",
}


@dataclass(frozen=True)
class FileNode:
    path: str
    size_bytes: int


def scan_repository_tree(root: Path, ignored_dirs: set[str] | None = None) -> list[FileNode]:
    resolved_ignored = ignored_dirs or DEFAULT_IGNORED_DIRS
    nodes: list[FileNode] = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        relative = path.relative_to(root)
        if any(part in resolved_ignored for part in relative.parts):
            continue

        nodes.append(
            FileNode(
                path=str(relative).replace("\\", "/"),
                size_bytes=path.stat().st_size,
            )
        )

    nodes.sort(key=lambda item: item.path)
    return nodes
