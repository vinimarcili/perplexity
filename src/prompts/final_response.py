"""Prompt for generating the final research report.

Instructs the LLM to write a 500-800 word response using the accumulated
search summaries, with numbered reference citations.

Placeholders:
    {input}: The user question.
    {search_results}: Formatted summaries of all search results.
"""

from src.prompts.base import BASE_PROMPT

FINAL_RESPONSE_PROMPT: str = BASE_PROMPT + """
Your objective here is to develop a final response to the user using
the reports made during the web search, with their synthesis.

The response should contain something between 500 - 800 words.

Here's the web search results:
<SEARCH_RESULTS>
{search_results}
</SEARCH_RESULTS>

You MUST add reference citations (with the number of the citation, example: [1]) for the
articles you used in each paragraph of your answer.
"""
