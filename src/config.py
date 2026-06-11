"""Configuration management for the Enterprise AI Logistics Solution."""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Logistics AI Engine"
    app_version: str = "1.0.0"
    debug: bool = False

    # AI Model
    gemini_model: str = "gemini-1.5-pro"
    ai_temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    ai_max_tokens: int = 2048

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_key: Optional[str] = None

    # Dashboard
    dashboard_host: str = "0.0.0.0"
    dashboard_port: int = 8501

    # Security
    rate_limit_per_minute: int = 60
    enable_cors: bool = True
    cors_origins: list = ["*"]

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


def get_settings() -> Settings:
    """Get application settings instance."""
    return Settings()
