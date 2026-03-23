from dataclasses import dataclass
from urllib.parse import urlparse


class RepoUrlError(ValueError):
    """Raised when a repository URL is not a valid GitHub repository URL."""


@dataclass(frozen=True)
class RepoRef:
    owner: str
    name: str
    branch: str | None = None

    @property
    def slug(self) -> str:
        return f"{self.owner}/{self.name}"


def parse_github_repo_url(url: str) -> RepoRef:
    normalized = url.strip()
    if not normalized:
        raise RepoUrlError("Repository URL cannot be empty.")

    if normalized.startswith("git@github.com:"):
        path = normalized.split("git@github.com:", maxsplit=1)[1]
        return _parse_path(path)

    parsed = urlparse(normalized)
    if parsed.scheme not in {"https", "http"}:
        raise RepoUrlError("Only HTTP(S) GitHub repository URLs are supported.")

    if parsed.netloc.lower() != "github.com":
        raise RepoUrlError("Only github.com repositories are currently supported.")

    return _parse_path(parsed.path)


def _parse_path(path: str) -> RepoRef:
    cleaned = path.strip("/")
    if cleaned.endswith(".git"):
        cleaned = cleaned[:-4]

    parts = [part for part in cleaned.split("/") if part]
    if len(parts) < 2:
        raise RepoUrlError("Expected URL format: github.com/<owner>/<repo>")

    owner, name = parts[0], parts[1]
    if not owner or not name:
        raise RepoUrlError("Repository owner and name are required.")

    branch = None
    if len(parts) >= 4 and parts[2] == "tree":
        branch = parts[3]

    return RepoRef(owner=owner, name=name, branch=branch)
