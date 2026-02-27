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
    with st.status("Searching..."):
        for output in graph.stream({"input": user_input}, stream_mode="debug"):
            if output["type"] == "task_result":
                node_name: str = output["payload"]["name"]
                st.write(f"Running **{node_name}**")

    st.session_state.searching = False

    response: str = output["payload"]["result"][0][1]

    if "</think>" in response:
        think_str = response.split("</think>")[0]
        final_response = response.split("</think>")[1]

        with st.expander("Think", expanded=False):
            st.write(think_str)

        st.write(final_response)
    else:
        st.write(response)
