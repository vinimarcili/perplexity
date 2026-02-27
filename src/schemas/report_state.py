"""LangGraph workflow state definition for the research report pipeline."""

import operator
from typing import List

from typing_extensions import Annotated, TypedDict

from src.schemas.query_result import QueryResult


class ReportState(TypedDict):
    """LangGraph workflow state for the research report pipeline.

    Attributes:
        input: The original user question.
        response: The final generated report.
        queries: List of search queries derived from the user question.
        queries_results: Accumulated search results with summaries.
            Uses ``operator.add`` as a reducer to merge results from parallel nodes.
    """

    input: str
    response: str
    queries: List[str]
    queries_results: Annotated[List[QueryResult], operator.add]
