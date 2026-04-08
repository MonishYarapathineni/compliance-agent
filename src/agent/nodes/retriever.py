"""Retriever node.

Fetches the most relevant policy document chunks from the vector store for
the current user query.  Retrieved documents are stored in
``AgentState.retrieved_docs`` for use by downstream nodes.
"""

from __future__ import annotations

# TODO: from src.agent.state import AgentState
# TODO: from src.ingestion.vectorstore import VectorStoreManager


def retrieve_documents(state: dict) -> dict:
    """Run a similarity search and populate ``retrieved_docs``.

    Args:
        state: Current ``AgentState`` dict containing ``query``.

    Returns:
        Partial state update with ``retrieved_docs`` list populated.
    """
    # TODO: retriever = VectorStoreManager().as_retriever()
    # TODO: docs = retriever.invoke(state["query"])
    # TODO: return {"retrieved_docs": docs}
    pass
