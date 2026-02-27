"""Text parsing utilities for LLM responses.

Provides helpers for stripping chain-of-thought ``<think>`` blocks
and extracting structured data from free-form LLM output.
"""

import json
import re
from typing import List, Tuple


def strip_think_tags(text: str) -> str:
    """Remove ``<think>...</think>`` blocks from an LLM response.

    Args:
        text: Raw LLM response that may contain think tags.

    Returns:
        The text after the closing ``</think>`` tag, or the
        original text if no think tags are present.
    """
    if "</think>" in text:
        return text.split("</think>")[-1].strip()
    return text


def split_think_and_response(text: str) -> Tuple[str, str]:
    """Split an LLM response into its think block and final content.

    Args:
        text: Raw LLM response that may contain think tags.

    Returns:
        A tuple ``(think, response)``. If no think tags are present,
        ``think`` is empty and ``response`` is the full text.
    """
    if "</think>" in text:
        parts = text.split("</think>", 1)
        return parts[0].strip(), parts[1].strip()
    return "", text.strip()


def parse_queries(text: str) -> List[str]:
    """Extract a list of search queries from an LLM response.

    Strips ``<think>`` blocks, then attempts to parse JSON with a
    ``queries`` key. Falls back to extracting numbered or bulleted lines.

    Args:
        text: Raw LLM response string.

    Returns:
        A list of up to 5 query strings.
    """
    text = strip_think_tags(text)

    json_match = re.search(r'\{.*"queries"\s*:\s*\[.*\].*\}', text, re.DOTALL)
    if json_match:
        try:
            data = json.loads(json_match.group())
            queries = data.get("queries", [])
            if queries:
                return queries[:5]
        except json.JSONDecodeError:
            pass

    lines = []
    for line in text.strip().splitlines():
        cleaned = re.sub(r"^\s*[\d]+[.\)]\s*", "", line).strip()
        cleaned = re.sub(r"^\s*[-*]\s*", "", cleaned).strip()
        cleaned = cleaned.strip('"').strip("'")
        if cleaned and len(cleaned) > 5:
            lines.append(cleaned)
    return lines[:5]
