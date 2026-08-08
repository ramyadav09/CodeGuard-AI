import logging

from pydantic import BaseModel

from app.agents.base_agent import BaseAgent
from app.schemas.review import FindingSchema, PRMetadata
from app.services.ai.base import AIProvider
from app.services.diff_parser import ParsedDiff

logger = logging.getLogger(__name__)


class TestAgentOutput(BaseModel):
    findings: list[FindingSchema]


class TestAnalysisAgent(BaseAgent):
    __test__ = False

    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            name="Test Analysis Agent",
            description=(
                "Evaluates test coverage of modified/added code branches and suggests "
                "concrete unit test cases."
            ),
            ai_provider=ai_provider,
        )

    async def analyze(
        self, pr_metadata: PRMetadata, parsed_diff: ParsedDiff
    ) -> list[FindingSchema]:
        system_instruction = (
            "You are an expert Test Analysis AI Agent. Analyze whether newly added or "
            "modified code paths in the PR diff have adequate unit/integration test "
            "coverage. Suggest concrete, runnable unit test code cases.\n"
            "Rules:\n"
            "1. Category MUST be 'TESTING'.\n"
            "2. Identify specific un-tested branches or edge cases.\n"
            "3. Provide concrete copyable test code snippets in suggested_fix.\n"
            "4. Only output findings with confidence >= 0.70."
        )

        diff_summary = []
        for file in parsed_diff.files[:10]:
            diff_summary.append(
                f"File: {file.file_path}\nStatus: {file.status}\nPatch:\n{file.raw_patch[:1500]}"
            )

        prompt = f"PR Title: {pr_metadata.title}\n\nCODE CHANGES:\n" + "\n\n".join(diff_summary)

        try:
            result = await self.ai_provider.analyze_diff(
                prompt, system_instruction, TestAgentOutput
            )
            raw_findings = result.get("findings", [])
            valid_findings = []
            for item in raw_findings:
                try:
                    finding = FindingSchema(**item)
                    if finding.confidence >= 0.70:
                        valid_findings.append(finding)
                except Exception as exc:
                    logger.warning(f"TestAnalysisAgent finding validation skipped: {exc!s}")
            return valid_findings
        except Exception as exc:
            logger.error(f"TestAnalysisAgent execution error: {exc!s}")
            return []
