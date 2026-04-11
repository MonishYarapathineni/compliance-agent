"""Shared utilities for agent nodes."""

from __future__ import annotations


def format_docs(docs: list) -> str:
    lines = []
    for doc in docs:
        source = doc.metadata.get("source", "unknown").split("/")[-1]
        page = int(float(doc.metadata.get("page", 0)))  # handle float pages
        lines.append(f"[{source}, page {page}]:\n{doc.page_content}")
    return "\n\n".join(lines)