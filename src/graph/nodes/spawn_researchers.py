"""Conditional edge that fans out parallel search nodes."""

from typing import List

from langgraph.types import Send

from src.schemas import ReportState


def spawn_researchers(state: ReportState) -> List[Send]:
    """Fan-out router that dispatches one ``single_search`` node per query.

    Creates a ``Send`` message for each query, carrying both the query
    string and the original user input.

    Args:
        state: Current workflow state containing ``queries`` and ``input``.

    Returns:
        A list of ``Send`` objects targeting the ``single_search`` node.
    """
    return [
        Send("single_search", {"query": q, "input": state["input"]})
        for q in state["queries"]
    ]
