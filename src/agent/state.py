"""Agent state schema.

Defines the ``AgentState`` TypedDict that flows through every node in the
LangGraph graph.  All fields are optional at construction; nodes populate
them progressively as the graph executes.
"""

from __future__ import annotations

# TODO: from typing import Annotated, TypedDict, Optional
# TODO: from langchain_core.documents import Document
# TODO: from langgraph.graph.message import add_messages
from __future__ import annotations
from typing import TypedDict, Optional, Annotated
from langchain_core.documents import Document
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

class AgentState(TypedDict):
    """Shared state object passed between LangGraph nodes.

    Attributes:
        query:           The raw user question.
        routed_to:       Which node the router directed the query to.
        retrieved_docs:  Documents fetched by the retriever node.
        conflicts:       Any detected policy conflicts (list of dicts).
        answer:          The final drafted answer string.
        critique:        Critique / quality assessment from the critic node.
        needs_hitl:      Flag indicating human-in-the-loop review is required.
        hitl_response:   Human reviewer's response (populated externally).
        messages:        Full conversation message history (LangGraph managed).
    """
    query: str
    routed_to: Optional[str]
    retrieved_docs: Optional[list[Document]]
    conflicts: Optional[list[dict]]
    answer: Optional[str]
    critique: Optional[str]
    needs_hitl: bool
    hitl_response: Optional[str]
    messages: Annotated[list[BaseMessage], add_messages]

    # TODO: convert to TypedDict with proper Annotated fields
    pass
