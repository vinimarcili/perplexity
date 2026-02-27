"""Result display components: streaming status, think block, and final response."""

import streamlit as st
from langgraph.graph.state import CompiledStateGraph

from src.utils import split_think_and_response


def _extract_response(output: dict) -> str:
    """Extract the ``response`` value from a debug stream event payload.

    Handles both dict and list-of-tuples result formats across
    different LangGraph versions.

    Args:
        output: A single debug stream event dict.

    Returns:
        The response string if found, otherwise empty string.
    """
    result_data = output["payload"]["result"]
    if isinstance(result_data, dict) and "response" in result_data:
        return result_data["response"]
    if isinstance(result_data, list):
        for item in result_data:
            if isinstance(item, (list, tuple)) and len(item) > 1:
                if isinstance(item[1], dict) and "response" in item[1]:
                    return item[1]["response"]
    return ""


def _render_response(response: str) -> None:
    """Render the final response, splitting think blocks if present.

    Args:
        response: The full LLM response string.
    """
    think, content = split_think_and_response(response)

    if think:
        with st.expander("Think", expanded=False):
            st.write(think)

    st.write(content)


def render_results(graph: CompiledStateGraph, user_input: str) -> None:
    """Stream the graph execution and render the final response.

    Displays intermediate node execution steps inside a status widget,
    then shows the final response. If the model uses chain-of-thought
    (``<think>`` blocks), the reasoning is placed in a collapsible expander.

    Args:
        graph: The compiled LangGraph to stream.
        user_input: The user's question to pass as graph input.
    """
    response = ""

    with st.status("Searching..."):
        for output in graph.stream({"input": user_input}, stream_mode="debug"):
            if output["type"] == "task_result":
                st.write(f"Running **{output['payload']['name']}**")
                extracted = _extract_response(output)
                if extracted:
                    response = extracted

    st.session_state.searching = False

    if not response:
        st.warning("No response was generated. The graph may have failed to produce results.")
        return

    _render_response(response)
