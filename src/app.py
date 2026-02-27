"""Streamlit UI for the Local Perplexity research assistant.

Orchestrates the layout components and graph execution.
"""

import streamlit as st

from src.graph.builder import build_graph
from src.layout import render_header, render_results, render_search_form


@st.cache_resource
def _get_graph():
    """Build and cache the compiled LangGraph workflow.

    Returns:
        CompiledStateGraph: A compiled graph, cached across Streamlit reruns.
    """
    return build_graph()


def run_app() -> None:
    """Launch the Streamlit application.

    Initializes session state, renders layout components via the
    ``layout`` module, and triggers graph execution when the user
    submits a search. Validates that user input is not empty.
    """
    if "searching" not in st.session_state:
        st.session_state.searching = False

    graph = _get_graph()
    is_busy: bool = st.session_state.searching

    render_header()
    user_input: str = render_search_form(is_busy)

    if st.session_state.searching:
        if not user_input.strip():
            st.session_state.searching = False
            st.warning("Please enter a question before searching.")
            return
        render_results(graph, user_input)
