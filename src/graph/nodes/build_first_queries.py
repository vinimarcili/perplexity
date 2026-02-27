"""Node that generates search queries from the user's question."""

import json
import re
from typing import Dict, List

from src.prompts import QUERY_BUILDER_PROMPT
from src.schemas import ReportState
from src.services.llm import get_llm

llm = get_llm()


def _parse_queries(text: str) -> List[str]:
    """Extract a list of queries from the LLM response.

    Handles responses that may contain ``<think>`` blocks and/or
    JSON with a ``queries`` key. Falls back to extracting numbered
    or bulleted lines if JSON parsing fails.

    Args:
        text: Raw LLM response string.

    Returns:
        A list of query strings.
    """
    if "</think>" in text:
        text = text.split("</think>")[-1].strip()

    json_match = re.search(r'\{.*"queries"\s*:\s*\[.*\].*\}', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group())
            return data.get("queries", [])
        except json.JSONDecodeError:
            pass

    lines = []
    for line in text.strip().splitlines():
        line = re.sub(r"^\s*[\d]+[\.\)]\s*", "", line).strip()
        line = re.sub(r"^\s*[-\*]\s*", "", line).strip()
        line = line.strip('"').strip("'")
        if line and len(line) > 5:
            lines.append(line)
    return lines[:5]


def build_first_queries(state: ReportState) -> Dict[str, List[str]]:
    """Generate a list of search queries based on the user's question.

    Calls the LLM and parses the response to extract 3-5 search queries.
    Handles chain-of-thought (``<think>``) blocks from reasoning models
    like deepseek-r1.

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
    result = llm.invoke(prompt)
    queries = _parse_queries(result.content)
    return {"queries": queries}
