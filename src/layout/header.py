"""Header section of the Streamlit UI."""

import streamlit as st


def render_header() -> None:
    """Render the application title.

    Displays the main heading at the top of the page.
    """
    st.title("Local Perplexity")
