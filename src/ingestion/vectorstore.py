"""Vector store module.

Manages embedding and persistence of document chunks into a vector database
(default: Chroma).  Provides a retriever interface consumed by the agent's
retriever node.
"""

from __future__ import annotations

import os
import shutil

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import VectorStoreRetriever


class VectorStoreManager:
    """Creates, populates, and exposes a Chroma vector store."""

    def __init__(self, persist_directory: str = "data/processed/chroma") -> None:
        self.persist_directory = persist_directory
        self.embedding = OpenAIEmbeddings(model="text-embedding-3-small")
        self._store: Chroma | None = None

    def build(self, chunks: list) -> None:
        """Embed ``chunks`` and persist them to disk.

        Removes any existing database at ``persist_directory`` first to avoid
        stale read-only state from a previous run.

        Args:
            chunks: Chunked ``Document`` objects from ``PolicyChunker``.
        """
        if os.path.exists(self.persist_directory):
            shutil.rmtree(self.persist_directory)
        self._store = Chroma.from_documents(
            chunks, self.embedding, persist_directory=self.persist_directory
        )

    def load(self) -> Chroma:
        """Load an existing persisted vector store from disk.

        Returns:
            Chroma: The loaded vector store instance.
        """
        if self._store is not None:
            return self._store
        self._store = Chroma(
            persist_directory=self.persist_directory,
            embedding_function=self.embedding,
        )
        return self._store

    def as_retriever(self, search_kwargs: dict | None = None) -> VectorStoreRetriever:
        """Return a LangChain retriever for use inside the agent graph.

        Args:
            search_kwargs: Optional kwargs forwarded to ``VectorStore.as_retriever``.

        Returns:
            VectorStoreRetriever
        """
        return self.load().as_retriever(search_kwargs=search_kwargs or {"k": 6})
