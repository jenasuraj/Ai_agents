from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseModel


class Settings(BaseModel):
    """Environment-backed settings.

    Real secrets should live only in your local `.env` file.
    This file only reads those values; it does not store any secret.
    """

    app_name: str = "AI Agents"
    environment: str = "development"
    openai_api_key: str | None = None
    openrouter_api_key: str | None = None
    groq_api_key: str | None = None
    tavily_api_key: str | None = None
    firecrawl_api_key: str | None = None
    elevenlabs_api_key: str | None = None
    github_token: str | None = None
    notion_api_key: str | None = None


@lru_cache
def get_settings() -> Settings:
    """Load environment variables from `.env` and return typed settings."""

    load_dotenv()

    return Settings(
        environment=os.getenv("ENVIRONMENT", "development"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openrouter_api_key=os.getenv("OPENROUTER_API_KEY"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        tavily_api_key=os.getenv("TAVILY_API_KEY"),
        firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY"),
        elevenlabs_api_key=os.getenv("ELEVENLABS_API_KEY"),
        github_token=os.getenv("GITHUB_TOKEN"),
        notion_api_key=os.getenv("NOTION_API_KEY"),
    )
