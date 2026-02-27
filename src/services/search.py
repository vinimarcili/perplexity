"""Web search and content extraction service using Tavily.

Handles querying the Tavily API, extracting raw page content,
and returning structured results.
"""

from typing import Optional, Tuple

from tavily import TavilyClient

from src.config.settings import settings


def _get_client() -> TavilyClient:
    """Create a Tavily API client.

    Returns:
        TavilyClient: Authenticated Tavily client instance.
    """
    return TavilyClient(api_key=settings.tavily_api_key)


def search_and_extract(query: str) -> Optional[Tuple[str, str, str]]:
    """Search the web for a query and extract the raw content of the top result.

    Performs a Tavily search, takes the first result, and extracts
    the full page content for downstream summarization.

    Args:
        query: The search query string.

    Returns:
        A tuple of ``(title, url, raw_content)`` if extraction succeeds,
        or ``None`` if no results are found, extraction fails, or an
        API error occurs.

    Example:
        >>> result = search_and_extract("what is LangGraph")
        >>> if result:
        ...     title, url, raw_content = result
    """
    try:
        client = _get_client()

        search_results = client.search(query=query, max_results=1, include_raw_content=False)
        if not search_results.get("results"):
            return None

        result_item = search_results["results"][0]
        title: str = result_item["title"]
        url: str = result_item["url"]

        extraction = client.extract(urls=[url])
        if not extraction.get("results"):
            return None

        raw_content: str = extraction["results"][0].get("raw_content", "")
        if not raw_content:
            return None

        return title, url, raw_content
    except Exception:
        return None
