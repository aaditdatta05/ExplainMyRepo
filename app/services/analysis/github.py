import re

GITHUB_REPO_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?/?$"
)


class InvalidRepositoryUrlError(ValueError):
    pass


def parse_github_repo_url(repo_url: str) -> tuple[str, str]:
    match = GITHUB_REPO_URL_RE.match(repo_url.strip())
    if not match:
        raise InvalidRepositoryUrlError("Repository URL must be a valid GitHub repository URL")

    owner = match.group("owner")
    repo = match.group("repo")
    return owner, repo
