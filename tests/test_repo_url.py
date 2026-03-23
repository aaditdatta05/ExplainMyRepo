import pytest

from app.services.repo_url import RepoUrlError, parse_github_repo_url


@pytest.mark.parametrize(
    "url,owner,name,branch",
    [
        ("https://github.com/psf/requests", "psf", "requests", None),
        ("https://github.com/psf/requests.git", "psf", "requests", None),
        ("git@github.com:psf/requests.git", "psf", "requests", None),
        (
            "https://github.com/psf/requests/tree/main",
            "psf",
            "requests",
            "main",
        ),
    ],
)
def test_parse_github_repo_url_valid(url: str, owner: str, name: str, branch: str | None) -> None:
    repo = parse_github_repo_url(url)
    assert repo.owner == owner
    assert repo.name == name
    assert repo.branch == branch


def test_parse_github_repo_url_rejects_non_github_host() -> None:
    with pytest.raises(RepoUrlError):
        parse_github_repo_url("https://gitlab.com/example/repo")


def test_parse_github_repo_url_rejects_invalid_shape() -> None:
    with pytest.raises(RepoUrlError):
        parse_github_repo_url("https://github.com/only-owner")
