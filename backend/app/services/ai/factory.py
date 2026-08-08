from app.core.config import settings
from app.services.ai.base import AIProvider
from app.services.ai.gemini_provider import GeminiProvider
from app.services.ai.mock_provider import MockAIProvider
from app.services.ai.nvidia_provider import NvidiaProvider


def get_ai_provider(provider_name: str | None = None) -> AIProvider:
    name = (provider_name or settings.AI_PROVIDER).lower()

    if name == "gemini":
        return GeminiProvider()
    elif name == "nvidia":
        return NvidiaProvider()
    else:
        return MockAIProvider()
