"""Tests for the document chunking module (src/ingestion/chunker.py).

Verifies that ``PolicyChunker`` correctly splits documents, preserves
metadata, respects chunk size and overlap settings, and handles edge cases
such as empty inputs and single-sentence documents.
"""

from __future__ import annotations

import pytest

# TODO: from src.ingestion.chunker import PolicyChunker


class TestPolicyChunker:
    """Unit tests for PolicyChunker."""

    def test_split_returns_list(self):
        """split() should always return a list, even for a single document."""
        # TODO: chunker = PolicyChunker()
        # TODO: docs = [Document(page_content="Some policy text.", metadata={})]
        # TODO: chunks = chunker.split(docs)
        # TODO: assert isinstance(chunks, list)
        pass

    def test_chunk_size_respected(self):
        """No chunk should exceed the configured chunk_size in characters."""
        # TODO: chunker = PolicyChunker(chunk_size=100, chunk_overlap=0)
        # TODO: long_text = "word " * 500
        # TODO: docs = [Document(page_content=long_text, metadata={})]
        # TODO: chunks = chunker.split(docs)
        # TODO: assert all(len(c.page_content) <= 100 for c in chunks)
        pass

    def test_metadata_preserved(self):
        """Original document metadata should be present in every chunk."""
        # TODO: chunker = PolicyChunker()
        # TODO: docs = [Document(page_content="text", metadata={"source": "policy.pdf"})]
        # TODO: chunks = chunker.split(docs)
        # TODO: assert all("source" in c.metadata for c in chunks)
        pass

    def test_empty_documents(self):
        """split() on an empty list should return an empty list without error."""
        # TODO: chunker = PolicyChunker()
        # TODO: assert chunker.split([]) == []
        pass
