"""Node that aggregates search summaries and generates the final report."""

from typing import Dict

from src.prompts import FINAL_RESPONSE_PROMPT
from src.schemas import ReportState
from src.services.llm import get_llm

llm = get_llm()


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
    search_results = ""
    references = ""

    for i, result in enumerate(state["queries_results"]):
        search_results += f"[{i + 1}]\n"
        search_results += f"Title: {result.title}\n"
        search_results += f"URL: {result.url}\n"
        search_results += f"Resume: {result.resume}\n"
        search_results += "=======================\n\n"
        references += f"[{i + 1}] - [{result.title}]({result.url})\n"

    prompt = FINAL_RESPONSE_PROMPT.format(
        input=state["input"],
        search_results=search_results,
    )
    llm_result = llm.invoke(prompt)
    response = f"{llm_result.content}\n\nReferences:\n{references}"
    return {"response": response}
