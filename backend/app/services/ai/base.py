from abc import ABC, abstractmethod
from typing import Dict, Any, Type, List
from pydantic import BaseModel


class AIProvider(ABC):
    @abstractmethod
    async def analyze_diff(
        self,
        prompt: str,
        system_instruction: str,
        schema: Type[BaseModel]
    ) -> Dict[str, Any]:
        """
        Sends analysis prompt and system instructions to the LLM provider
        and returns a dictionary matching the specified Pydantic schema.
        """
        pass
