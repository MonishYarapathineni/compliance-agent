"""Human-in-the-loop (HITL) node.

Pauses graph execution and surfaces the current state to a human reviewer
via an interrupt mechanism.  When the reviewer provides a response it is
written into ``AgentState.hitl_response`` and the graph resumes.
"""

from __future__ import annotations

# TODO: from langgraph.types import interrupt
# TODO: from src.agent.state import AgentState


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
    # TODO: payload = build_review_payload(state)
    # TODO: response = interrupt(payload)   # suspends execution here
    # TODO: return {"hitl_response": response}
    pass
