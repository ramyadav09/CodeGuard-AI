from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.schemas.review import PRMetadata


@pytest.mark.asyncio
async def test_github_service_get_pr_metadata_success():
    """GitHubService.get_pr_metadata parses API response correctly"""
    from app.services.github_service import GitHubService

    svc = GitHubService(token="dummy-token")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "number": 42,
        "title": "Fix null dereference",
        "user": {"login": "dev"},
        "html_url": "https://github.com/owner/repo/pull/42",
        "state": "open",
        "base": {"ref": "main"},
        "head": {"ref": "feature/fix"},
        "changed_files": 3,
        "additions": 50,
        "deletions": 10,
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response):
        metadata = await svc.get_pr_metadata("owner", "repo", 42)

    assert isinstance(metadata, PRMetadata)
    assert metadata.pr_number == 42
    assert metadata.title == "Fix null dereference"
    assert metadata.author == "dev"
    assert metadata.additions == 50


@pytest.mark.asyncio
async def test_github_service_get_pr_metadata_404():
    """GitHubService raises GitHubServiceError on 404"""
    from app.services.github_service import GitHubService, GitHubServiceError

    svc = GitHubService(token="dummy-token")

    mock_response = MagicMock()
    mock_response.status_code = 404

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response):
        with pytest.raises(GitHubServiceError) as exc_info:
            await svc.get_pr_metadata("owner", "repo", 999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_github_service_get_pr_diff_success():
    """GitHubService.get_pr_diff returns raw diff text"""
    from app.services.github_service import GitHubService

    svc = GitHubService(token="dummy-token")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = "diff --git a/x.py b/x.py"

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock, return_value=mock_response):
        diff = await svc.get_pr_diff("owner", "repo", 42)

    assert diff == "diff --git a/x.py b/x.py"


@pytest.mark.asyncio
async def test_github_service_get_pr_metadata_network_error():
    """GitHubService raises GitHubServiceError on network failure"""
    import httpx

    from app.services.github_service import GitHubService, GitHubServiceError

    svc = GitHubService(token="dummy-token")

    with patch(
        "httpx.AsyncClient.get",
        new_callable=AsyncMock,
        side_effect=httpx.RequestError("connection refused"),
    ):
        with pytest.raises(GitHubServiceError) as exc_info:
            await svc.get_pr_metadata("owner", "repo", 42)

    assert exc_info.value.status_code == 503
