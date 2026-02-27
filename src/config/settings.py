"""Application settings loaded from environment variables.

This module centralizes all configuration values used across the application,
including API URLs, model names, and API keys.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Holds all application configuration values.

    Attributes:
        ollama_url: Base URL for the Ollama API server.
        ollama_model: Name of the Ollama model to use for inference.
        tavily_api_key: API key for the Tavily web search service.
    """

    def __init__(self) -> None:
        """Initialize settings from environment variables."""
        self.ollama_url: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
        self.ollama_model: str = os.getenv("OLLAMA_MODEL", "deepseek-r1:14b")
        self.tavily_api_key: str = os.getenv("TAVILY_API_KEY", "")


settings = Settings()
