"""Search form components: text input and search button."""

import streamlit as st


def _on_search() -> None:
    """Callback that marks the search as running in session state."""
    st.session_state.searching = True


def render_search_form(is_busy: bool) -> str:
    """Render the search input field and button.

    Both components are disabled while a search is in progress
    to prevent duplicate submissions.

    Args:
        is_busy: Whether a search is currently running.

    Returns:
        The user's question string from the text input.
    """
    user_input: str = st.text_input(
        "What is your question?",
        value="What's the difference between a standard VSCode and Cursor/Windsurf and other AI IDEs?",
        disabled=is_busy,
    )

    st.button("Search", on_click=_on_search, disabled=is_busy)

    return user_input
