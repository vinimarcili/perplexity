"""Node that generates search queries from the user's question."""

from typing import Dict, List

from src.prompts import QUERY_BUILDER_PROMPT
from src.schemas import ReportState
from src.services.llm import get_llm
from src.utils import parse_queries

llm = get_llm()


def build_first_queries(state: ReportState) -> Dict[str, List[str]]:
    """Generate a list of search queries based on the user's question.

    Calls the LLM and parses the response to extract 3-5 search queries.
    Handles chain-of-thought (``<think>``) blocks from reasoning models
    like deepseek-r1.

    Args:
        state: Current workflow state containing the user ``input``.

    Returns:
        A dict with key ``queries`` mapping to a list of query strings.
    """
    user_input: str = state["input"]
    prompt = QUERY_BUILDER_PROMPT.format(input=user_input)
    result = llm.invoke(prompt)
    return {"queries": parse_queries(result.content)}
