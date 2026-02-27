"""Node that aggregates search summaries and generates the final report."""

from typing import Dict, List, Tuple

from src.prompts import FINAL_RESPONSE_PROMPT
from src.schemas import QueryResult, ReportState
from src.services.llm import get_llm

llm = get_llm()


def _format_sources(results: List[QueryResult]) -> Tuple[str, str]:
    """Format query results into prompt context and a references block.

    Args:
        results: List of search results with titles, URLs, and summaries.

    Returns:
        A tuple ``(search_context, references)`` where ``search_context``
        is the numbered text for the LLM prompt and ``references`` is the
        markdown-formatted citation list.
    """
    context_parts: List[str] = []
    reference_parts: List[str] = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"[{i}]\nTitle: {result.title}\nURL: {result.url}\n"
            f"Resume: {result.resume}\n=======================\n"
        )
        reference_parts.append(f"[{i}] - [{result.title}]({result.url})")

    return "\n".join(context_parts), "\n".join(reference_parts)


def final_writer(state: ReportState) -> Dict[str, str]:
    """Aggregate search summaries and generate the final research report.

    Formats all accumulated ``queries_results`` into a structured prompt,
    asks the LLM to write a 500-800 word response with citations,
    and appends a references section.

    Args:
        state: Current workflow state with ``queries_results`` and ``input``.

    Returns:
        A dict with key ``response`` containing the full report string
        including references.
    """
    search_context, references = _format_sources(state["queries_results"])

    prompt = FINAL_RESPONSE_PROMPT.format(
        input=state["input"],
        search_results=search_context,
    )
    llm_result = llm.invoke(prompt)
    return {"response": f"{llm_result.content}\n\nReferences:\n{references}"}
