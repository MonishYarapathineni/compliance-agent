"""Vector store module.

Manages embedding and persistence of document chunks into Pinecone.
Provides a retriever interface consumed by the agent's retriever node.
"""

from __future__ import annotations
import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings
from pinecone import Pinecone


class VectorStoreManager:
    """Creates, populates, and exposes a Pinecone vector store."""

    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
        self.index_name = os.getenv("PINECONE_INDEX_NAME", "compliance-agent")
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index = pc.Index(self.index_name)

    def build(self, chunks: list) -> None:
        """Embed chunks and upsert into Pinecone."""
        PineconeVectorStore.from_documents(
            chunks, self.embeddings, index_name=self.index_name
        )
        print(f"Upserted {len(chunks)} chunks to Pinecone index '{self.index_name}'")

    def load(self) -> PineconeVectorStore:
        """Connect to existing Pinecone index."""
        return PineconeVectorStore(index=self.index, embedding=self.embeddings)

    def as_retriever(self, search_kwargs: dict | None = None):
        """Return a LangChain retriever for use inside the agent graph."""
        return self.load().as_retriever(search_kwargs=search_kwargs or {"k": 6})
