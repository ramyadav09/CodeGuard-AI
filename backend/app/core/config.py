import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "CodeGuard AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # GitHub Configuration
    GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN", None)

    # AI Provider Configuration
    AI_PROVIDER: str = os.getenv("AI_PROVIDER", "mock")
    AI_API_KEY: str | None = os.getenv("AI_API_KEY", None)

    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./codeguard.db"
    )  # Override with Neon PostgreSQL URL in .env

    # Server Settings
    PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
