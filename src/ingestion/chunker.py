"""Document chunking module.

Splits loaded ``Document`` objects into smaller, semantically coherent chunks
suitable for embedding and vector-store indexing.  Supports recursive
character splitting and semantic/sentence-boundary strategies.
"""

from __future__ import annotations

from langchain_text_splitters import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain_core.documents import Document

class PolicyChunker:
    """Wraps LangChain text splitters with project-specific defaults."""

    def __init__(
        self,
        chunk_size: int = 1024,
        chunk_overlap: int = 128,
        strategy: str = "recursive",
    ) -> None:
        # TODO: validate strategy, instantiate the appropriate splitter
        if strategy == "character":
            self.splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        elif strategy == "recursive":
            self.splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        else:
            raise ValueError(f"Unknown strategy '{strategy}'. Choose 'recursive' or 'character'.")

        

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
        """Attach chunk index and parent document ID to each chunk's metadata."""
        filtered = []
        for i, chunk in enumerate(chunks):
            if len(chunk.page_content.strip()) < 100:  # drop noise chunks, assuming mostly these are from headers/footers or boilerplate or titles
                continue
            chunk.metadata["chunk_index"] = i
            filtered.append(chunk)
        return filtered
