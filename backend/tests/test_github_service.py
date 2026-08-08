import pytest
from app.services.github_service import GitHubService, GitHubServiceError


def test_parse_valid_pr_url():
    url = "https://github.com/facebook/react/pull/1024"
    owner, repo, pr_number = GitHubService.parse_pr_url(url)
    assert owner == "facebook"
    assert repo == "react"
    assert pr_number == 1024


def test_parse_invalid_pr_url():
    url = "https://github.com/facebook/react"
    with pytest.raises(GitHubServiceError) as exc_info:
        GitHubService.parse_pr_url(url)
    assert "Invalid GitHub PR URL format" in str(exc_info.value)
