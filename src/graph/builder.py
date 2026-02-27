"""Graph construction and compilation for the research workflow.

Assembles the LangGraph ``StateGraph`` by wiring together nodes and edges,
then compiles it into a runnable graph.
"""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.graph.nodes import (
    build_first_queries,
    final_writer,
    single_search,
    spawn_researchers,
)
from src.schemas import ReportState


def build_graph() -> CompiledStateGraph:
    """Build and compile the research workflow graph.

    The graph follows this pipeline::

        START
          │
          ▼
        build_first_queries
          │
          ▼ (conditional fan-out)
        single_search  ×N  (parallel)
          │
          ▼
        final_writer
          │
          ▼
        END

    Returns:
        CompiledStateGraph: A compiled LangGraph ready to be invoked or streamed.

    Example:
        >>> graph = build_graph()
        >>> result = graph.invoke({"input": "What is LangGraph?"})
        >>> print(result["response"])
    """
    builder = StateGraph(ReportState)

    builder.add_node("build_first_queries", build_first_queries)
    builder.add_node("single_search", single_search)
    builder.add_node("final_writer", final_writer)

    builder.add_edge(START, "build_first_queries")
    builder.add_conditional_edges("build_first_queries", spawn_researchers, ["single_search"])
    builder.add_edge("single_search", "final_writer")
    builder.add_edge("final_writer", END)

    return builder.compile()
