"""Node that generates search queries from the user's question."""

from typing import Dict, List

from src.prompts import QUERY_BUILDER_PROMPT
from src.schemas import QueryList, ReportState
from src.services.llm import get_llm

llm = get_llm()


def build_first_queries(state: ReportState) -> Dict[str, List[str]]:
    """Generate a list of search queries based on the user's question.

    Uses the LLM with structured output to produce 3-5 search queries
    that will be used to research the user's topic.

    Args:
        state: Current workflow state containing the user ``input``.

    Returns:
        A dict with key ``queries`` mapping to a list of query strings.

    Example:
        >>> result = build_first_queries({"input": "What is LangGraph?"})
        >>> result["queries"]
        ['LangGraph framework overview', 'LangGraph vs LangChain', ...]
    """
    user_input: str = state["input"]
    prompt = QUERY_BUILDER_PROMPT.format(input=user_input)
    query_llm = llm.with_structured_output(QueryList)
    result: QueryList = query_llm.invoke(prompt)
    return {"queries": result.queries}
