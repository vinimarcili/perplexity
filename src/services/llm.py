"""LLM client factory for Ollama integration.

Provides a configured ``ChatOllama`` instance based on application settings.
"""

from langchain_ollama import ChatOllama

from src.config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return a configured ChatOllama instance.

    Returns:
        ChatOllama: A LangChain chat model connected to the local Ollama server.

    Example:
        >>> llm = get_llm()
        >>> response = llm.invoke("Hello")
    """
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
    )
