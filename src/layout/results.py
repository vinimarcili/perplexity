"""Result display components: streaming status, think block, and final response."""

import streamlit as st
from langgraph.graph.state import CompiledStateGraph


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
                node_name: str = output["payload"]["name"]
                st.write(f"Running **{node_name}**")

                result_data = output["payload"]["result"]
                if isinstance(result_data, dict) and "response" in result_data:
                    response = result_data["response"]
                elif isinstance(result_data, list):
                    for item in result_data:
                        if isinstance(item, (list, tuple)) and len(item) > 1:
                            if isinstance(item[1], dict) and "response" in item[1]:
                                response = item[1]["response"]

    st.session_state.searching = False

    if not response:
        st.warning("No response was generated. The graph may have failed to produce results.")
        return

    if "</think>" in response:
        think_str = response.split("</think>")[0]
        final_response = response.split("</think>")[1]

        with st.expander("Think", expanded=False):
            st.write(think_str)

        st.write(final_response)
    else:
        st.write(response)
