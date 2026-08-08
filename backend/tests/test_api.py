from unittest.mock import AsyncMock, patch
import pytest
from app.schemas.review import PRMetadata


@pytest.mark.asyncio
async def test_health_check_endpoint(client):
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "CodeGuard AI" in data["service"]


@pytest.mark.asyncio
async def test_review_endpoint_with_mock_github(client):
    mock_metadata = PRMetadata(
        owner="octocat",
        repo="Hello-World",
        pr_number=1,
        title="Correct typo in README",
        author="octocat",
        html_url="https://github.com/octocat/Hello-World/pull/1",
        state="open",
        base_branch="master",
        head_branch="patch-1",
        changed_files_count=1,
        additions=5,
        deletions=2
    )
    mock_diff = """diff --git a/README.md b/README.md
index 7898192..2e65efe 100644
--- a/README.md
+++ b/README.md
@@ -1 +1 @@
-Hello World!
+Hello World!!
"""

    with patch("app.services.github_service.GitHubService.get_pr_metadata", new_callable=AsyncMock) as mock_get_meta, \
         patch("app.services.github_service.GitHubService.get_pr_diff", new_callable=AsyncMock) as mock_get_diff:

        mock_get_meta.return_value = mock_metadata
        mock_get_diff.return_value = mock_diff

        payload = {
            "repo_url": "https://github.com/octocat/Hello-World/pull/1",
            "ai_provider": "mock"
        }

        response = await client.post("/api/v1/review", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["pr_metadata"]["owner"] == "octocat"
        assert data["pr_metadata"]["repo"] == "Hello-World"
        assert "overall_score" in data
        assert len(data["findings"]) > 0
