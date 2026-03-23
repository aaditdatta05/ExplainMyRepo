from pathlib import Path

import pytest

from app.services.repo_fetcher import RepoFetcher, RepoFetchError
from app.services.repo_url import RepoRef


def test_repo_fetcher_returns_target_path(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    fetcher = RepoFetcher(workspace=tmp_path)
    repo = RepoRef(owner="psf", name="requests", branch="main")

    class Result:
        returncode = 0
        stderr = ""

    def fake_run(cmd: list[str], capture_output: bool, text: bool) -> Result:
        assert "clone" in cmd
        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)

    fetched = fetcher.fetch(repo)
    assert fetched.local_path == tmp_path / "psf-requests"


def test_repo_fetcher_raises_on_clone_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    fetcher = RepoFetcher(workspace=tmp_path)
    repo = RepoRef(owner="psf", name="requests")

    class Result:
        returncode = 1
        stderr = "fatal: failed"

    def fake_run(cmd: list[str], capture_output: bool, text: bool) -> Result:
        return Result()

    monkeypatch.setattr("subprocess.run", fake_run)

    with pytest.raises(RepoFetchError):
        fetcher.fetch(repo)
