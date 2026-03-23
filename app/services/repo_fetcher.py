import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from app.services.repo_url import RepoRef


class RepoFetchError(RuntimeError):
    """Raised when a repository cannot be cloned."""


@dataclass(frozen=True)
class FetchedRepo:
    repo: RepoRef
    local_path: Path


class RepoFetcher:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.workspace.mkdir(parents=True, exist_ok=True)

    def fetch(self, repo: RepoRef) -> FetchedRepo:
        target = self.workspace / f"{repo.owner}-{repo.name}"
        if target.exists():
            shutil.rmtree(target)

        clone_url = f"https://github.com/{repo.slug}.git"
        cmd = [
            "git",
            "clone",
            "--depth",
            "1",
            "--branch",
            repo.branch or "HEAD",
            clone_url,
            str(target),
        ]

        completed = subprocess.run(cmd, capture_output=True, text=True)
        if completed.returncode != 0:
            raise RepoFetchError(completed.stderr.strip() or "Failed to clone repository.")

        return FetchedRepo(repo=repo, local_path=target)
