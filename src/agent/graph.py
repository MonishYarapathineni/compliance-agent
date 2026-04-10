"""LangGraph graph definition.

Assembles the compliance agent's directed graph by wiring together the
router, retriever, conflict-detector, critic, and HITL nodes.  Exposes a
compiled ``app`` object that can be invoked or streamed.
"""

from __future__ import annotations

from langgraph.graph import StateGraph, END
from src.agent.state import AgentState
from src.agent.nodes.router import route_query
from src.agent.nodes.retriever import retrieve_documents
from src.agent.nodes.conflict import detect_conflicts
from src.agent.nodes.critic import critique_answer
from src.agent.nodes.hitl import human_review

def route_decision(state: AgentState) -> str:
    # router node would write "retriever", "conflict", or "hitl" into state
    return state["routed_to"]

def critic_decision(state: AgentState) -> str:
    if state["critique_score"] is not None and state["critique_score"] < 0.7:
        if state["retry_count"] >= 2:  # max 2 retries
            return "hitl"
        return "retriever"
    if state["needs_hitl"]:
        return "hitl"
    return END

def build_graph(checkpointer=None):
    """Construct and compile the LangGraph ``StateGraph``.

    Returns:
        CompiledGraph: Ready-to-invoke agent application.
    """
    graph = StateGraph(AgentState)
    # Adding Nodes to Graph
    graph.add_node("router", route_query)
    graph.add_node("retriever", retrieve_documents)
    graph.add_node("conflict", detect_conflicts)
    graph.add_node("critic", critique_answer)
    graph.add_node("hitl", human_review)


    # Set entry point
    graph.set_entry_point("router")

    # Wiring edges between nodes
    graph.add_conditional_edges("router", route_decision)
    graph.add_conditional_edges("critic", critic_decision)
    graph.add_edge("retriever", "critic")
    graph.add_edge("conflict", "critic")
    graph.add_edge("hitl", END)

    return graph.compile(checkpointer=checkpointer)


# Module-level compiled app — import and call ``app.invoke(state)``
app = build_graph()  
