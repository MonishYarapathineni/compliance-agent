"""Human-in-the-loop (HITL) node.

Pauses graph execution and surfaces the current state to a human reviewer
via an interrupt mechanism.  When the reviewer provides a response it is
written into ``AgentState.hitl_response`` and the graph resumes.
"""

from __future__ import annotations

from langgraph.types import interrupt


def human_review(state: dict) -> dict:
    """Pause execution and wait for a human reviewer's input.

    Uses LangGraph's ``interrupt`` primitive to yield control.  The graph
    host (API layer) is responsible for delivering the reviewer's response
    back to the graph via ``graph.update_state``.

    Args:
        state: Current ``AgentState`` dict.

    Returns:
        Partial state update with ``hitl_response`` populated after resume.
    """

    human_response = interrupt({
        "query": state["query"],
        "answer": state.get("answer"),
        "critique_score": state.get("critique_score"),
        "retry_count": state.get("retry_count", 0),
        "message": "Human review required. Please provide a verified answer."
    })

    return {
        "hitl_response": human_response,
        "answer": human_response,
        "needs_hitl": False
    }
