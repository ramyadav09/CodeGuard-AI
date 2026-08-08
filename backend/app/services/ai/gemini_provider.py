import json
import logging
from typing import Any

import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.mock_provider import MockAIProvider

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = "gemini-1.5-flash"
        self.endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        )

    async def analyze_diff(
        self, prompt: str, system_instruction: str, schema: type[BaseModel]
    ) -> dict[str, Any]:
        if not self.api_key:
            logger.warning("No Gemini API key supplied. Falling back to MockAIProvider.")
            return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)

        payload = {
            "system_instruction": {"parts": [{"text": system_instruction}]},
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.2, "response_mime_type": "application/json"},
        }

        headers = {"Content-Type": "application/json"}
        params = {"key": self.api_key}

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    self.endpoint, json=payload, headers=headers, params=params
                )
                if response.status_code != 200:
                    logger.error(
                        f"Gemini API returned error HTTP {response.status_code}: {response.text}"
                    )
                    return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)

                data = response.json()
                candidates = data.get("candidates", [])
                if not candidates:
                    return {"summary": "No findings generated.", "findings": []}

                raw_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "{}")
                parsed_json = json.loads(raw_text)
                return parsed_json
            except (httpx.RequestError, json.JSONDecodeError, ValidationError) as exc:
                logger.error(f"GeminiProvider exception: {exc!s}. Falling back to MockAIProvider.")
                return await MockAIProvider().analyze_diff(prompt, system_instruction, schema)
