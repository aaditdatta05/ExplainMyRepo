from app.services.dependency_graph import build_dependency_index, extract_dependencies


def test_extract_dependencies_for_python() -> None:
    source = "import os\nimport requests\nfrom pathlib import Path\n"
    deps = extract_dependencies("app/main.py", source)
    assert deps == ["os", "pathlib", "requests"]


def test_extract_dependencies_for_javascript() -> None:
    source = "const x = require('react');\nimport y from 'axios';"
    deps = extract_dependencies("ui/index.js", source)
    assert deps == ["axios", "react"]


def test_build_dependency_index_sorts_paths() -> None:
    index = build_dependency_index(
        {
            "b.py": "import os",
            "a.py": "import sys",
        }
    )
    assert list(index.keys()) == ["a.py", "b.py"]
