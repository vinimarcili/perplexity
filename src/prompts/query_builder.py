"""Prompt for generating search queries from a user question.

Instructs the LLM to produce 3-5 search queries based on the user's input.

Placeholders:
    {input}: The user question.
"""

from src.prompts.base import BASE_PROMPT

QUERY_BUILDER_PROMPT: str = BASE_PROMPT + """
Your first objective is to build a list of queries that will be used to find answers to the user's question.

Answer with anything between 3-5 queries.
"""
