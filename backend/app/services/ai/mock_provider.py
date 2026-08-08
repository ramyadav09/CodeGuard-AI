from typing import Any

from pydantic import BaseModel

from app.services.ai.base import AIProvider


class MockAIProvider(AIProvider):
    """
    Deterministic AI Provider used for unit tests, offline development,
    and Playwright E2E pipeline verification without external API dependencies.
    """

    async def analyze_diff(
        self, prompt: str, system_instruction: str, schema: type[BaseModel]
    ) -> dict[str, Any]:
        sys_lower = system_instruction.lower()
        prompt_lower = prompt.lower()
        findings = []

        if "security review ai agent" in sys_lower or "security" in sys_lower:
            findings.append(
                {
                    "severity": "CRITICAL",
                    "category": "SECURITY",
                    "file_path": "backend/app/core/config.py",
                    "line_start": 14,
                    "line_end": 18,
                    "title": "Hardcoded Credentials Risk",
                    "description": (
                        "Fallback API token detected in configuration settings "
                        "string default value."
                    ),
                    "why_it_matters": (
                        "Committing hardcoded secrets exposes authentication tokens to public "
                        "git history and unauthorized access."
                    ),
                    "suggested_fix": (
                        "Use os.getenv('API_KEY') without fallback plaintext defaults or "
                        "raise a ConfigurationError if missing."
                    ),
                    "confidence": 0.95,
                }
            )
            findings.append(
                {
                    "severity": "HIGH",
                    "category": "SECURITY",
                    "file_path": "backend/app/api/endpoints/review.py",
                    "line_start": 42,
                    "line_end": 45,
                    "title": "Unsanitized Path Parameter",
                    "description": (
                        "User-supplied repo path is concatenated directly into URL request "
                        "without encoding."
                    ),
                    "why_it_matters": (
                        "Malicious path parameters could cause SSRF or path traversal "
                        "vulnerabilities when executing outgoing API requests."
                    ),
                    "suggested_fix": (
                        "Sanitize and URL-encode path variables using urllib.parse.quote() "
                        "before making outgoing HTTP requests."
                    ),
                    "confidence": 0.91,
                }
            )

        elif "bug detection ai agent" in sys_lower or "bug" in sys_lower:
            findings.append(
                {
                    "severity": "HIGH",
                    "category": "BUG",
                    "file_path": "backend/app/services/diff_parser.py",
                    "line_start": 52,
                    "line_end": 56,
                    "title": "Potential NoneType Dereference",
                    "description": (
                        "Attempting to access .group(1) on regex search without verifying match "
                        "is not None."
                    ),
                    "why_it_matters": (
                        "If the diff patch header format differs slightly, re.search returns "
                        "None and crashes with AttributeError at runtime."
                    ),
                    "suggested_fix": (
                        "Add an explicit `if match:` check before accessing regex group "
                        "parameters."
                    ),
                    "confidence": 0.89,
                }
            )

        elif "quality" in prompt_lower or "quality" in system_instruction.lower():
            findings.append(
                {
                    "severity": "MEDIUM",
                    "category": "CODE_QUALITY",
                    "file_path": "frontend/src/components/FindingCard.tsx",
                    "line_start": 28,
                    "line_end": 35,
                    "title": "High Cognitive Complexity",
                    "description": (
                        "Nested ternary conditional operators used for severity badge styling "
                        "rendering."
                    ),
                    "why_it_matters": (
                        "Deeply nested inline ternaries degrade code readability and make "
                        "component maintenance error-prone."
                    ),
                    "suggested_fix": (
                        "Extract severity styling into a dedicated lookup dictionary mapping "
                        "severity strings to Tailwind classes."
                    ),
                    "confidence": 0.85,
                }
            )

        elif "test" in prompt_lower or "test" in system_instruction.lower():
            findings.append(
                {
                    "severity": "MEDIUM",
                    "category": "TESTING",
                    "file_path": "backend/app/services/github_service.py",
                    "line_start": 30,
                    "line_end": 40,
                    "title": "Missing Test Coverage for Rate-Limit Error Branch",
                    "description": (
                        "The HTTP 429 rate limit exception path in get_pr_metadata is unverified "
                        "in unit test suite."
                    ),
                    "why_it_matters": (
                        "If GitHub API returns HTTP 429 in production, unhandled rate-limit "
                        "handling could cause unexpected server 500 errors."
                    ),
                    "suggested_fix": (
                        "Add pytest test case mocking a 429 response from GitHub API and asserting "
                        "GitHubServiceError status_code == 429."
                    ),
                    "confidence": 0.88,
                }
            )

        return {"summary": "Mock analysis complete with findings.", "findings": findings}
