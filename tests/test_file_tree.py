from pathlib import Path

from app.services.file_tree import scan_repository_tree


def test_scan_repository_tree_ignores_common_directories(tmp_path: Path) -> None:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('ok')", encoding="utf-8")

    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "config").write_text("[core]", encoding="utf-8")

    nodes = scan_repository_tree(tmp_path)

    assert [node.path for node in nodes] == ["src/main.py"]
