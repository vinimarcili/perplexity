"""Entry point for the Local Perplexity application.

Run with::

    uv run streamlit run main.py
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
)

from src.app import run_app

run_app()
