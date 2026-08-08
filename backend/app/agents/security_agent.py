import logging
from typing import List
from pydantic import BaseModel
from app.agents.base_agent import BaseAgent
from app.schemas.review import FindingSchema, PRMetadata
from app.services.diff_parser import ParsedDiff
from app.services.ai.base import AIProvider

logger = logging.getLogger(__name__)


class SecurityAgentOutput(BaseModel):
    findings: List[FindingSchema]


class SecurityReviewAgent(BaseAgent):
    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            name="Security Review Agent",
            description="Inspects code changes for OWASP vulnerabilities, hardcoded secrets, injection risks, and unsafe input handling.",
            ai_provider=ai_provider
        )

    async def analyze(self, pr_metadata: PRMetadata, parsed_diff: ParsedDiff) -> List[FindingSchema]:
        system_instruction = (
            "You are an expert Security Review AI Agent. Your role is to inspect git diff patches for security vulnerabilities, "
            "including hardcoded credentials/secrets, SQL/command injection, Cross-Site Scripting (XSS), unvalidated inputs, and unsafe dependency usage.\n"
            "Rules:\n"
            "1. Category MUST be 'SECURITY'.\n"
            "2. Never leak actual raw secret strings in responses (mask as '***').\n"
            "3. Use CRITICAL severity for hardcoded secrets or remote code execution risks.\n"
            "4. Only output findings with confidence >= 0.70."
        )

        diff_summary = []
        for file in parsed_diff.files[:10]:
            diff_summary.append(f"File: {file.file_path}\nStatus: {file.status}\nPatch:\n{file.raw_patch[:1500]}")

        prompt = (
            f"PR Title: {pr_metadata.title}\n"
            f"PR Repository: {pr_metadata.owner}/{pr_metadata.repo}\n\n"
            f"CODE CHANGES:\n" + "\n\n".join(diff_summary)
        )

        try:
            result = await self.ai_provider.analyze_diff(prompt, system_instruction, SecurityAgentOutput)
            raw_findings = result.get("findings", [])
            valid_findings = []
            for item in raw_findings:
                try:
                    finding = FindingSchema(**item)
                    if finding.confidence >= 0.70:
                        valid_findings.append(finding)
                except Exception as exc:
                    logger.warning(f"SecurityAgent finding validation skipped: {str(exc)}")
            return valid_findings
        except Exception as exc:
            logger.error(f"SecurityAgent execution error: {str(exc)}")
            return []
