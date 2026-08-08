import pytest
from app.schemas.review import PRMetadata
from app.services.diff_parser import DiffParser
from app.services.ai.mock_provider import MockAIProvider
from app.agents.bug_agent import BugDetectionAgent
from app.agents.security_agent import SecurityReviewAgent
from app.agents.code_quality_agent import CodeQualityAgent
from app.agents.test_agent import TestAnalysisAgent

SAMPLE_DIFF = """diff --git a/backend/app/core/config.py b/backend/app/core/config.py
index 1234567..89abcdef 100644
--- a/backend/app/core/config.py
+++ b/backend/app/core/config.py
@@ -14,4 +14,6 @@ class Settings:
     SECRET_KEY = "hardcoded_secret_val"
"""


@pytest.mark.asyncio
async def test_domain_agents():
    provider = MockAIProvider()
    metadata = PRMetadata(
        owner="test-owner",
        repo="test-repo",
        pr_number=1,
        title="Fix security leak",
        author="developer",
        html_url="https://github.com/test-owner/test-repo/pull/1",
        state="open",
        base_branch="main",
        head_branch="patch",
        changed_files_count=1,
        additions=2,
        deletions=0
    )
    parsed = DiffParser.parse_patch(SAMPLE_DIFF)

    sec_agent = SecurityReviewAgent(provider)
    sec_findings = await sec_agent.analyze(metadata, parsed)
    assert len(sec_findings) > 0
    assert sec_findings[0].category.value == "SECURITY"

    bug_agent = BugDetectionAgent(provider)
    bug_findings = await bug_agent.analyze(metadata, parsed)
    assert len(bug_findings) > 0
    assert bug_findings[0].category.value == "BUG"

    qual_agent = CodeQualityAgent(provider)
    qual_findings = await qual_agent.analyze(metadata, parsed)
    assert len(qual_findings) > 0

    test_agent = TestAnalysisAgent(provider)
    test_findings = await test_agent.analyze(metadata, parsed)
    assert len(test_findings) > 0
