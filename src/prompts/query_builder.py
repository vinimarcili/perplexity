"""Prompt for generating search queries from a user question.

Instructs the LLM to produce 3-5 search queries based on the user's input.

Placeholders:
    {input}: The user question.
"""

from src.prompts.base import BASE_PROMPT

QUERY_BUILDER_PROMPT: str = BASE_PROMPT + """
Your objective is to generate 3-5 **web search queries** that will be used to research the user's question.

Rules:
- Each query must be a short search engine query (like you would type into Google).
- One query per line, numbered (e.g. "1. query here").
- Do NOT explain, describe, or answer the question. ONLY output the numbered queries.

Example output:
1. VSCode vs Cursor AI IDE comparison
2. Windsurf IDE features and pricing
3. AI-powered code editors 2025 review
"""
