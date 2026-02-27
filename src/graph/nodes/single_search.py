"""Node that searches the web for a single query and summarizes the result."""

from typing import Dict, List

from src.prompts import SEARCH_RESUME_PROMPT
from src.schemas import QueryResult
from src.services.llm import get_llm
from src.services.search import search_and_extract

llm = get_llm()


def single_search(state: dict) -> Dict[str, List[QueryResult]]:
    """Search the web for a single query and summarize the result.

    Receives a dict (from ``Send``) containing the query and original
    user input. Performs web search, extracts page content, and asks
    the LLM to summarize it.

    Args:
        state: A dict with keys:
            - ``query`` (str): The search query.
            - ``input`` (str): The original user question (for context).

    Returns:
        A dict with key ``queries_results`` containing a single-element
        list with the summarized ``QueryResult``, or an empty list if
        extraction failed.
    """
    query: str = state["query"]
    user_input: str = state["input"]

    result = search_and_extract(query)
    if result is None:
        return {"queries_results": []}

    title, url, raw_content = result
    prompt = SEARCH_RESUME_PROMPT.format(input=user_input, search_results=raw_content)
    llm_result = llm.invoke(prompt)

    query_result = QueryResult(
        title=title,
        url=url,
        resume=llm_result.content,
    )
    return {"queries_results": [query_result]}
