import asyncio
import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.schemas.review import PRReviewRequest, PRReviewResponse, PRMetadata, FindingSchema
from app.services.github_service import GitHubService
from app.services.diff_parser import DiffParser
from app.services.ai.factory import get_ai_provider
from app.agents.bug_agent import BugDetectionAgent
from app.agents.security_agent import SecurityReviewAgent
from app.agents.code_quality_agent import CodeQualityAgent
from app.agents.test_agent import TestAnalysisAgent
from app.agents.aggregator import ReviewAggregator
from app.models.review import RepositoryModel, PullRequestModel, ReviewReportModel, FindingModel

logger = logging.getLogger(__name__)


class PRReviewSkill:
    """
    Custom skill defining a repeatable, 10-step process for ingesting PR metadata,
    parsing git diffs, orchestrating multi-agent analysis, aggregating findings,
    and returning structured developer reports.
    """

    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db

    async def execute(self, request: PRReviewRequest) -> PRReviewResponse:
        # Step 1: Parse PR input
        github_service = GitHubService()
        if request.repo_url:
            owner, repo, pr_number = github_service.parse_pr_url(request.repo_url)
        elif request.owner and request.repo and request.pr_number:
            owner, repo, pr_number = request.owner, request.repo, request.pr_number
        else:
            raise ValueError("Must provide either repo_url or owner, repo, and pr_number.")

        # Step 2: Fetch PR Metadata & Diff Patch from GitHub
        pr_metadata: PRMetadata = await github_service.get_pr_metadata(owner, repo, pr_number)
        raw_diff: str = await github_service.get_pr_diff(owner, repo, pr_number)

        # Step 3: Parse diff patch
        parsed_diff = DiffParser.parse_patch(raw_diff)

        # Step 4: Get AI Provider
        ai_provider = get_ai_provider(request.ai_provider)

        # Step 5: Instantiate domain agents
        bug_agent = BugDetectionAgent(ai_provider)
        security_agent = SecurityReviewAgent(ai_provider)
        quality_agent = CodeQualityAgent(ai_provider)
        test_agent = TestAnalysisAgent(ai_provider)

        # Step 6: Parallel Agent Execution
        bug_task = bug_agent.analyze(pr_metadata, parsed_diff)
        sec_task = security_agent.analyze(pr_metadata, parsed_diff)
        qual_task = quality_agent.analyze(pr_metadata, parsed_diff)
        test_task = test_agent.analyze(pr_metadata, parsed_diff)

        results = await asyncio.gather(bug_task, sec_task, qual_task, test_task, return_exceptions=True)

        all_findings = []
        for res in results:
            if isinstance(res, list):
                all_findings.extend(res)

        # Step 7: Aggregate & Deduplicate Findings
        overall_score, severity_breakdown, final_findings, summary = ReviewAggregator.aggregate(all_findings)

        created_at_iso = datetime.now(timezone.utc).isoformat()

        # Step 8: Database Persistence (if DB session provided)
        report_id = "temp-report-id"
        if self.db:
            try:
                # Check or create repo
                stmt = select(RepositoryModel).where(RepositoryModel.owner == owner, RepositoryModel.name == repo)
                result = await self.db.execute(stmt)
                repo_obj = result.scalar_one_or_none()
                if not repo_obj:
                    repo_obj = RepositoryModel(
                        owner=owner,
                        name=repo,
                        url=f"https://github.com/{owner}/{repo}"
                    )
                    self.db.add(repo_obj)
                    await self.db.flush()

                # Check or create PR
                stmt_pr = select(PullRequestModel).where(
                    PullRequestModel.repository_id == repo_obj.id,
                    PullRequestModel.pr_number == pr_number
                )
                result_pr = await self.db.execute(stmt_pr)
                pr_obj = result_pr.scalar_one_or_none()
                if not pr_obj:
                    pr_obj = PullRequestModel(
                        repository_id=repo_obj.id,
                        pr_number=pr_number,
                        title=pr_metadata.title,
                        author=pr_metadata.author,
                        html_url=pr_metadata.html_url,
                        state=pr_metadata.state,
                        base_branch=pr_metadata.base_branch,
                        head_branch=pr_metadata.head_branch,
                        changed_files_count=pr_metadata.changed_files_count,
                        additions=pr_metadata.additions,
                        deletions=pr_metadata.deletions
                    )
                    self.db.add(pr_obj)
                    await self.db.flush()

                # Create Review Report
                report_obj = ReviewReportModel(
                    pull_request_id=pr_obj.id,
                    overall_score=overall_score,
                    summary=summary
                )
                self.db.add(report_obj)
                await self.db.flush()
                report_id = report_obj.id

                # Create Finding models
                for f in final_findings:
                    finding_obj = FindingModel(
                        review_report_id=report_obj.id,
                        severity=f.severity,
                        category=f.category,
                        file_path=f.file_path,
                        line_start=f.line_start,
                        line_end=f.line_end,
                        title=f.title,
                        description=f.description,
                        why_it_matters=f.why_it_matters,
                        suggested_fix=f.suggested_fix,
                        confidence=f.confidence
                    )
                    self.db.add(finding_obj)

                await self.db.commit()
            except Exception as db_exc:
                logger.error(f"Failed to persist review to DB: {str(db_exc)}")
                await self.db.rollback()

        # Step 9 & 10: Format PRReviewResponse
        response = PRReviewResponse(
            id=report_id,
            pr_metadata=pr_metadata,
            overall_score=overall_score,
            summary=summary,
            findings_count=len(final_findings),
            severity_breakdown=severity_breakdown,
            findings=final_findings,
            created_at=created_at_iso
        )
        return response
