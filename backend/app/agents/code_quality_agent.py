import logging
from typing import List
from pydantic import BaseModel
from app.agents.base_agent import BaseAgent
from app.schemas.review import FindingSchema, PRMetadata
from app.services.diff_parser import ParsedDiff
from app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)


class QualityAgentOutput(BaseModel):
    findings: List[FindingSchema]


class CodeQualityAgent(BaseAgent):
    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            name="Code Quality Agent",
            description="Identifies code smells, duplication, high cognitive complexity, bad abstractions, and maintainability issues.",
            ai_provider=ai_provider
        )

    async def analyze(self, pr_metadata: PRMetadata, parsed_diff: ParsedDiff) -> List[FindingSchema]:
        system_instruction = (
            "You are an expert Code Quality AI Agent. Inspect code diffs for maintainability issues, code smells, "
            "excessive cognitive complexity, duplicated logic, dead code, poor naming, and anti-patterns.\n"
            "Rules:\n"
            "1. Category MUST be 'CODE_QUALITY', 'PERFORMANCE', or 'MAINTAINABILITY'.\n"
            "2. Provide pragmatic, actionable refactoring code snippets.\n"
            "3. Only output findings with confidence >= 0.70."
        )

        diff_summary = []
        for file in parsed_diff.files[:10]:
            diff_summary.append(f"File: {file.file_path}\nStatus: {file.status}\nPatch:\n{file.raw_patch[:1500]}")

        prompt = (
            f"PR Title: {pr_metadata.title}\n\n"
            f"CODE CHANGES:\n" + "\n\n".join(diff_summary)
        )

        try:
            result = await self.ai_provider.analyze_diff(prompt, system_instruction, QualityAgentOutput)
            raw_findings = result.get("findings", [])
            valid_findings = []
            for item in raw_findings:
                try:
                    finding = FindingSchema(**item)
                    if finding.confidence >= 0.70:
                        valid_findings.append(finding)
                except Exception as exc:
                    logger.warning(f"CodeQualityAgent finding validation skipped: {str(exc)}")
            return valid_findings
        except Exception as exc:
            logger.error(f"CodeQualityAgent execution error: {str(exc)}")
            return []
