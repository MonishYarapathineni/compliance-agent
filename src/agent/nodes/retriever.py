"""Retriever node.

Fetches the most relevant policy document chunks from the vector store for
the current user query.  Retrieved documents are stored in
``AgentState.retrieved_docs`` for use by downstream nodes.
"""

from __future__ import annotations

from src.agent.state import AgentState
from src.ingestion.vectorstore import VectorStoreManager
from langchain_openai import ChatOpenAI
from src.agent.utils import format_docs
import os

CHROMA_PATH = os.getenv("CHROMA_PERSIST_DIR","../data/processed/chroma")
print(f"Initializing retriever with Chroma path: {CHROMA_PATH}")
retrieve = VectorStoreManager(CHROMA_PATH).as_retriever()


ANSWER_PROMPT = """You are a compliance policy assistant.

Using ONLY the provided policy excerpts, answer the user's question clearly and concisely.
Always cite your sources using the format [filename, page X].
Do not include any information not found in the excerpts.

Question: {query}

Policy excerpts:
{source_chunks}

Answer:"""

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

def retrieve_documents(state: dict) -> dict:
    """Run a similarity search and populate ``retrieved_docs``.

    Args:
        state: Current ``AgentState`` dict containing ``query``.

    Returns:
        Partial state update with ``retrieved_docs`` list populated.
    """

    docs = retrieve.invoke(state["query"])
    print(f"Retriever node found {len(docs)} relevant documents.")
    print("query:", state["query"])
    source_chunks = format_docs(docs)
    query = state["query"]
    prompt = ANSWER_PROMPT.format(query=query, source_chunks=source_chunks)
    answer = llm.invoke(prompt).content.strip()


    return {"retrieved_docs": docs, "answer": answer}
