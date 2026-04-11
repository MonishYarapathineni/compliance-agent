"""Router node.

Classifies an incoming query and decides which downstream node should handle
it: direct retrieval, conflict detection, or immediate HITL escalation.
The routing decision is written back into ``AgentState.routed_to``.
"""

from __future__ import annotations
from langchain_openai import ChatOpenAI


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.0)

ROUTER_PROMPT = """You are a compliance query classifier.

Given a user question, classify it into exactly one of these categories:
- retriever: A straightforward factual question that can be answered from policy documents
- conflict: The question involves comparing policies, finding contradictions, or reconciling conflicting rules
- hitl: The question is too ambiguous, sensitive, or complex for automated handling and requires human review

Respond with ONLY the category name, nothing else.

Question: {query}"""

def route_query(state: dict) -> dict:
    """Inspect the user query and set ``routed_to`` in state.

    Args:
        state: Current ``AgentState`` dict.

    Returns:
        Partial state update with ``routed_to`` key populated.
    """

    query = state["query"]
    prompt = ROUTER_PROMPT.format(query=query)
    response = llm.invoke(prompt)
    decision = response.content.strip().lower()

    valid = {"retriever", "conflict", "hitl"}
    if decision not in valid:
        print(f"Warning: Router node got invalid response '{response}', defaulting to 'hitl'")
        decision = "hitl"
    return {"routed_to": decision}
