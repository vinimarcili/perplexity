"""Data model for a single web search result after extraction and summarization."""

from pydantic import BaseModel, Field


class QueryResult(BaseModel):
    """Represents a single web search result after extraction and summarization.

    Attributes:
        title: Title of the search result page.
        url: URL of the search result page.
        resume: LLM-generated summary of the page content.
    """

    title: str = Field(default=None, description="Title of the search result page")
    url: str = Field(default=None, description="URL of the search result page")
    resume: str = Field(default=None, description="LLM-generated summary of the page content")
