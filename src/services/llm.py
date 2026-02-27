"""LLM client factory for Ollama integration.

Provides configured ``ChatOllama`` instances based on application settings.
Two models are available:

- **Main model** (``OLLAMA_MODEL``): Used for query generation and final report writing.
  Typically a larger, more capable model (e.g. deepseek-r1:14b).
- **Search model** (``OLLAMA_SEARCH_MODEL``): Used for parallel search summarization.
  Typically a smaller, faster model (e.g. llama3.2:3b) to enable concurrent inference.
"""

from langchain_ollama import ChatOllama

from src.config.settings import settings


def get_llm() -> ChatOllama:
    """Create and return the main ChatOllama instance.

    Used for query generation (``build_first_queries``) and
    final report writing (``final_writer``).

    Returns:
        ChatOllama: A LangChain chat model using the main Ollama model.
    """
    return ChatOllama(
        model=settings.ollama_model,
        base_url=settings.ollama_url,
    )


def get_search_llm() -> ChatOllama:
    """Create and return the lightweight ChatOllama instance for search summarization.

    Used by ``single_search`` nodes that run in parallel.
    A smaller model allows Ollama to handle concurrent requests
    within the available VRAM.

    Returns:
        ChatOllama: A LangChain chat model using the search Ollama model.
    """
    return ChatOllama(
        model=settings.ollama_search_model,
        base_url=settings.ollama_url,
    )
