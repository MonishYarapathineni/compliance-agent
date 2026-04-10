"""Conflict detection node.

Examines the retrieved policy chunks for contradictions or ambiguities across
different policy sections or versions.  Detected conflicts are stored in
``AgentState.conflicts`` and may trigger HITL escalation.
"""

from __future__ import annotations
from langchain_openai import ChatOpenAI
from src.agent.state import AgentState
from src.ingestion.vectorstore import VectorStoreManager
from src.agent.utils import format_docs
import os

CHROMA_PATH = os.getenv("CHROMA_PERSIST_DIR", "../data/processed/chroma")
retrieve = VectorStoreManager(CHROMA_PATH).as_retriever(
    search_kwargs={"k": 8,
                   "filter": None  # could filter by source document
                   })


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

CONFLICT_PROMPT = """You are a compliance policy conflict analyzer.

You will be given a user question and policy excerpts from multiple documents.

Your tasks:
1. Identify any contradictions or inconsistencies between the policy excerpts
2. If conflicts exist, clearly explain what each document says and where they disagree
3. If no conflicts exist, provide a synthesized answer from all sources
4. Always cite sources using [filename, page X] format

Question: {query}

Policy excerpts:
{source_chunks}

Analysis:"""


def detect_conflicts(state: dict) -> dict:
    """Identify policy conflicts in ``retrieved_docs``.

    Args:
        state: Current ``AgentState`` dict containing ``retrieved_docs``.

    Returns:
        Partial state update with ``conflicts`` list and optionally
        ``needs_hitl`` flag set to ``True``.
    """
    
    docs = retrieve.invoke(state["query"])
    print(f"Retriever node found {len(docs)} relevant documents.")
    print("query:", state["query"])
    source_chunks = format_docs(docs)
    query = state["query"]
    prompt = CONFLICT_PROMPT.format(query=query, source_chunks=source_chunks)
    answer = llm.invoke(prompt).content.strip()

    return {"retrieved_docs": docs, "answer": answer}
