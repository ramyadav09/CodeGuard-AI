from abc import ABC, abstractmethod
from typing import List
from app.schemas.review import FindingSchema, PRMetadata
from app.services.diff_parser import ParsedDiff
from app.services.ai.base import AIProvider


class BaseAgent(ABC):
    def __init__(self, name: str, description: str, ai_provider: AIProvider):
        self.name = name
        self.description = description
        self.ai_provider = ai_provider

    @abstractmethod
    async def analyze(self, pr_metadata: PRMetadata, parsed_diff: ParsedDiff) -> List[FindingSchema]:
        """
        Executes domain-specific code analysis on the PR diff
        and returns a list of validated findings.
        """
        pass
