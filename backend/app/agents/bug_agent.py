import logging
from typing import List
from pydantic import BaseModel
from app.agents.base_agent import BaseAgent
from app.schemas.review import FindingSchema, PRMetadata
from app.services.diff_parser import ParsedDiff
from app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)


class BugAgentOutput(BaseModel):
    findings: List[FindingSchema]


class BugDetectionAgent(BaseAgent):
    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            name="Bug Detection Agent",
            description="Detects logical bugs, off-by-one errors, null pointer dereferences, and runtime failures.",
            ai_provider=ai_provider
        )

    async def analyze(self, pr_metadata: PRMetadata, parsed_diff: ParsedDiff) -> List[FindingSchema]:
        system_instruction = (
            "You are an expert Bug Detection AI Agent. Your sole responsibility is to inspect code changes in pull requests "
            "and detect logical bugs, edge-case failures, off-by-one errors, unhandled exceptions, and null/undefined dereferences.\n"
            "Rules:\n"
            "1. Only report genuine logical bugs backed by code evidence from added/modified diff lines.\n"
            "2. Category MUST be 'BUG'.\n"
            "3. Provide clear file paths, line ranges, problem descriptions, why it matters, and actionable suggested fixes.\n"
            "4. Do NOT invent files or line numbers. Set confidence >= 0.70."
        )

        diff_summary = []
        for file in parsed_diff.files[:10]: # Limit diff window for optimal token usage
            diff_summary.append(f"File: {file.file_path}\nStatus: {file.status}\nPatch:\n{file.raw_patch[:1500]}")

        prompt = (
            f"PR Title: {pr_metadata.title}\n"
            f"PR Description: {pr_metadata.author} submitting {pr_metadata.changed_files_count} files changed.\n\n"
            f"CODE CHANGES:\n" + "\n\n".join(diff_summary)
        )

        try:
            result = await self.ai_provider.analyze_diff(prompt, system_instruction, BugAgentOutput)
            raw_findings = result.get("findings", [])
            valid_findings = []
            for item in raw_findings:
                try:
                    finding = FindingSchema(**item)
                    if finding.confidence >= 0.70:
                        valid_findings.append(finding)
                except Exception as exc:
                    logger.warning(f"BugAgent finding validation skipped: {str(exc)}")
            return valid_findings
        except Exception as exc:
            logger.error(f"BugAgent execution error: {str(exc)}")
            return []
