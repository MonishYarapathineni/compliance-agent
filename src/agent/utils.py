"""Shared utilities for agent nodes."""

from __future__ import annotations


def format_docs(docs: list) -> str:
    """Format a list of Documents into a cited string for LLM prompts."""
    lines = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown").split("/")[-1]
        page = doc.metadata.get("page", "?")
        lines.append(f"[{source}, page {page}]:\n{doc.page_content}")
    return "\n\n".join(lines)
