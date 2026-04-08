"""LangGraph graph definition.

Assembles the compliance agent's directed graph by wiring together the
router, retriever, conflict-detector, critic, and HITL nodes.  Exposes a
compiled ``app`` object that can be invoked or streamed.
"""

from __future__ import annotations

# TODO: from langgraph.graph import StateGraph, END
# TODO: from src.agent.state import AgentState
# TODO: from src.agent.nodes.router import route_query
# TODO: from src.agent.nodes.retriever import retrieve_documents
# TODO: from src.agent.nodes.conflict import detect_conflicts
# TODO: from src.agent.nodes.critic import critique_answer
# TODO: from src.agent.nodes.hitl import human_review


def build_graph():
    """Construct and compile the LangGraph ``StateGraph``.

    Returns:
        CompiledGraph: Ready-to-invoke agent application.
    """
    # TODO: graph = StateGraph(AgentState)
    # TODO: graph.add_node("router", route_query)
    # TODO: graph.add_node("retriever", retrieve_documents)
    # TODO: graph.add_node("conflict", detect_conflicts)
    # TODO: graph.add_node("critic", critique_answer)
    # TODO: graph.add_node("hitl", human_review)
    # TODO: wire edges and conditional edges
    # TODO: graph.set_entry_point("router")
    # TODO: return graph.compile()
    pass


# Module-level compiled app — import and call ``app.invoke(state)``
app = None  # TODO: app = build_graph()
