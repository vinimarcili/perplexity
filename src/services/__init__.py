"""Service layer for external integrations (LLM, web search)."""

from src.services.llm import get_llm
from src.services.search import search_and_extract
