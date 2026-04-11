"""Document chunking module.

Splits loaded ``Document`` objects into smaller, semantically coherent chunks
suitable for embedding and vector-store indexing.  Supports recursive
character splitting and semantic/sentence-boundary strategies.
"""

from __future__ import annotations
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
)


class PolicyChunker:
    """Wraps LangChain text splitters with project-specific defaults."""

    def __init__(
        self,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        strategy: str = "recursive",
    ) -> None:

        if strategy == "character":
            self.splitter = CharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )
        elif strategy == "recursive":
            self.splitter = RecursiveCharacterTextSplitter(
                chunk_size=chunk_size, chunk_overlap=chunk_overlap
            )

        else:
            raise ValueError(
                f"Unknown strategy '{strategy}'. Choose 'recursive' or 'character'."
            )

    def split(self, documents: list) -> list:
        """Split a list of Documents into smaller chunks.

        Args:
            documents: Raw documents from ``PolicyDocumentLoader``.

        Returns:
            list[Document]: Chunked documents with updated metadata.
        """

        chunks = self.splitter.split_documents(documents)
        return self._add_chunk_metadata(chunks)

    def _add_chunk_metadata(self, chunks: list) -> list:
        filtered = []
        for i, chunk in enumerate(chunks):
            content = chunk.page_content.strip()
            if len(content) < 100:
                continue
            if chunk.metadata.get("page") == 0:
                continue
            if content.count('. . .') > 2 or content.count('......') > 1:
                continue
            chunk.metadata["chunk_index"] = i
            # ensure page is stored as int not float
            if "page" in chunk.metadata:
                chunk.metadata["page"] = int(chunk.metadata["page"])
            filtered.append(chunk)
        return filtered
