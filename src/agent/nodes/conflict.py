"""Conflict detection node.

Examines the retrieved policy chunks for contradictions or ambiguities across
different policy sections or versions.  Detected conflicts are stored in
``AgentState.conflicts`` and may trigger HITL escalation.
"""

from __future__ import annotations

# TODO: from langchain_openai import ChatOpenAI
# TODO: from src.agent.state import AgentState


def detect_conflicts(state: dict) -> dict:
    """Identify policy conflicts in ``retrieved_docs``.

    Args:
        state: Current ``AgentState`` dict containing ``retrieved_docs``.

    Returns:
        Partial state update with ``conflicts`` list and optionally
        ``needs_hitl`` flag set to ``True``.
    """
    # TODO: build conflict-detection prompt from retrieved_docs
    # TODO: call LLM, parse structured conflict list
    # TODO: set needs_hitl=True if conflicts are unresolvable
    # TODO: return {"conflicts": [...], "needs_hitl": bool}
    pass
