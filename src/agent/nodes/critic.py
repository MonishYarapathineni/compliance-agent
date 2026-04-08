"""Critic node.

Reviews the drafted answer for accuracy, completeness, citation quality, and
compliance with policy.  Stores a critique summary in ``AgentState.critique``
and can trigger a re-draft loop or HITL escalation.
"""

from __future__ import annotations

# TODO: from langchain_openai import ChatOpenAI
# TODO: from src.agent.state import AgentState


def critique_answer(state: dict) -> dict:
    """Evaluate the current draft answer and return a critique.

    Args:
        state: Current ``AgentState`` dict containing ``answer`` and
               ``retrieved_docs``.

    Returns:
        Partial state update with ``critique`` string and optionally
        ``needs_hitl`` flag.
    """
    # TODO: build critique prompt from answer + source docs
    # TODO: call LLM, extract structured critique (score, reasoning, flag)
    # TODO: return {"critique": <str>, "needs_hitl": bool}
    pass
