"""LangGraph node functions for the research workflow.

Each function represents a step in the research pipeline:
1. **build_first_queries** — Generate search queries from user input.
2. **single_search** — Search, extract, and summarize a single query.
3. **spawn_researchers** — Fan-out routing that dispatches parallel searches.
4. **final_writer** — Aggregate results and produce the final report.
"""

from src.graph.nodes.build_first_queries import build_first_queries
from src.graph.nodes.single_search import single_search
from src.graph.nodes.spawn_researchers import spawn_researchers
from src.graph.nodes.final_writer import final_writer
