"""Document loader module.

Responsible for reading raw policy documents from disk or remote sources
(PDF, DOCX, HTML, plain text) and returning them as a uniform list of
LangChain ``Document`` objects ready for chunking.
"""

from __future__ import annotations

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader, TextLoader
from langchain_core.documents import Document


class PolicyDocumentLoader:
    """Loads one or more policy documents from a local directory or URI."""

    def __init__(self, source_dir: str) -> None:
        # TODO: store source_dir, configure supported extensions
        self.source_dir = Path(source_dir)
        self.supported = {".pdf": self._load_pdf, ".docx": self._load_docx, ".txt": self._load_text}

    def load(self) -> list:
        """Discover and load all supported documents under ``source_dir``.

        Returns:
            list[Document]: Raw documents with populated ``metadata``.
        """
        # TODO: iterate files, dispatch to the correct loader, collect results
        documents = []
        for entry in self.source_dir.iterdir():
            s = entry.suffix.lower()
            if s in self.supported:
                documents.extend(self.supported[s](entry))
            else:
                print(f"Skipping unsupported file type: {entry}")
        return documents

    def _load_pdf(self, path: str) -> list:
        """Load a single PDF file using PyPDFLoader."""
        # TODO: implement
        loader = PyPDFLoader(path)
        return loader.load()

    def _load_docx(self, path: str) -> list:
        """Load a single DOCX file using UnstructuredWordDocumentLoader."""
        # TODO: implement
        raise NotImplementedError("DOCX support coming soon")

    def _load_text(self, path: str) -> list:
        """Load a plain-text or markdown file."""
        # TODO: implement
        loader = TextLoader(str(path), encoding="utf-8")
        return loader.load()
        
