import json
import logging
from typing import Any

import httpx
from pydantic import BaseModel

from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.mock_provider import MockAIProvider

logger = logging.getLogger(__name__)


class NvidiaProvider(AIProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.AI_API_KEY
        self.endpoint = "https://integrate.api.nvidia.com/v1/chat/completions"

    async def analyze_diff(
        self, prompt: str, system_instruction: str, schema: type[BaseModel]
    ) -> dict[str, Any]:
        if not self.api_key:
            logger.warning("No Nvidia API key supplied. Falling back to MockAIProvider.")
            return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)

        payload = {
            "model": "meta/llama-3.1-70b-instruct",
            "messages": [
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(self.endpoint, json=payload, headers=headers)
                if response.status_code != 200:
                    logger.error(
                        f"Nvidia API returned error HTTP {response.status_code}: {response.text}"
                    )
                    return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)

                data = response.json()
                raw_text = data["choices"][0]["message"]["content"]
                return json.loads(raw_text)
            except Exception as exc:
                logger.error(f"NvidiaProvider exception: {exc!s}. Falling back to MockAIProvider.")
                return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)
