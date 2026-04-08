"""Router node.

Classifies an incoming query and decides which downstream node should handle
it: direct retrieval, conflict detection, or immediate HITL escalation.
The routing decision is written back into ``AgentState.routed_to``.
"""

from __future__ import annotations

# TODO: from langchain_openai import ChatOpenAI
# TODO: from src.agent.state import AgentState


def route_query(state: dict) -> dict:
    """Inspect the user query and set ``routed_to`` in state.

    Args:
        state: Current ``AgentState`` dict.

    Returns:
        Partial state update with ``routed_to`` key populated.
    """
    # TODO: call LLM with a routing prompt
    # TODO: parse response into one of: "retriever", "conflict", "hitl"
    # TODO: return {"routed_to": <decision>}
    pass
