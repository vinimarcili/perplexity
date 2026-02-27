"""Prompt for summarizing a single web search result.

Instructs the LLM to synthesize the raw page content, keeping only
what is relevant to the user's question.

Placeholders:
    {input}: The user question.
    {search_results}: Raw content extracted from a web page.
"""

from src.prompts.base import BASE_PROMPT

SEARCH_RESUME_PROMPT: str = BASE_PROMPT + """
Your objective is to analyze the web search results and make a synthesis of it,
emphasizing only what is relevant to the user's question.

After your work, another agent will use the synthesis to build a final response to the user,
so make sure the synthesis contains only useful information.
Be concise and clear.

Here's the web search results:
<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>
"""
