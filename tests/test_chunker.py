"""Tests for the document chunking module (src/ingestion/chunker.py)."""

from __future__ import annotations
import pytest
from langchain_core.documents import Document
from src.ingestion.chunker import PolicyChunker


class TestPolicyChunker:
    def test_split_returns_list(self):
        chunker = PolicyChunker()
        docs = [
            Document(
                page_content="Some policy text.",
                metadata={"source": "test.pdf", "page": 1},
            )
        ]
        chunks = chunker.split(docs)
        assert isinstance(chunks, list)

    def test_chunk_size_respected(self):
        chunker = PolicyChunker(chunk_size=100, chunk_overlap=0)
        long_text = "word " * 500
        docs = [
            Document(page_content=long_text, metadata={"source": "test.pdf", "page": 1})
        ]
        chunks = chunker.split(docs)
        assert all(len(c.page_content) <= 150 for c in chunks)

    def test_metadata_preserved(self):
        chunker = PolicyChunker()
        docs = [
            Document(
                page_content="Some policy text " * 100,
                metadata={"source": "policy.pdf", "page": 1},
            )
        ]
        chunks = chunker.split(docs)
        assert all("source" in c.metadata for c in chunks)

    def test_chunk_index_attached(self):
        chunker = PolicyChunker(chunk_size=200, chunk_overlap=0)
        text = "This is a compliance policy statement. " * 50
        docs = [Document(page_content=text, metadata={"source": "test.pdf", "page": 1})]
        chunks = chunker.split(docs)
        assert len(chunks) > 0
        assert "chunk_index" in chunks[0].metadata

    def test_empty_documents(self):
        chunker = PolicyChunker()
        assert chunker.split([]) == []

    def test_invalid_strategy_raises(self):
        with pytest.raises(ValueError):
            PolicyChunker(strategy="invalid")

    def test_cover_page_filtered(self):
        chunker = PolicyChunker()
        docs = [
            Document(
                page_content="COVER PAGE", metadata={"source": "test.pdf", "page": 0}
            )
        ]
        chunks = chunker.split(docs)
        assert len(chunks) == 0
