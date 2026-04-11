"""API route definitions.

Registers all HTTP endpoints for the compliance agent service, including
query submission, HITL reviewer callbacks, ingestion triggers, and health
checks.
"""

from __future__ import annotations
import uuid
import re
from fastapi import APIRouter
from langgraph.checkpoint.memory import MemorySaver
from src.api.schemas import (
    QueryRequest,
    QueryResponse,
    HITLReviewRequest,
    Citation,
    IngestResponse,
)
from src.agent.graph import build_graph


router = APIRouter()
checkpointer = MemorySaver()
agent_app = build_graph(checkpointer=checkpointer)


def _extract_citations(answer: str) -> list[Citation]:
    if not answer:
        return []
    pattern = r'\[([^,\]]+),\s*pages?\s*([\d]+(?:\.0)?(?:-[\d]+(?:\.0)?)?)\]'
    matches = re.findall(pattern, answer)
    seen = set()
    citations = []
    for source, page_ref in matches:
        source = source.strip()
        if '-' in page_ref:
            parts = page_ref.split('-')
            start = int(float(parts[0]))
            end = int(float(parts[1]))
            for p in range(start, end + 1):
                key = (source, p)
                if key not in seen:
                    seen.add(key)
                    citations.append(Citation(source=source, page=p))
        else:
            key = (source, int(float(page_ref)))
            if key not in seen:
                seen.add(key)
                citations.append(Citation(source=source, page=int(float(page_ref))))
    return citations


@router.get("/health")
async def health_check() -> dict:
    return {"status": "ok"}


@router.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """Accept a user compliance question and return the agent's answer.

    Args:
        request: ``QueryRequest`` body containing ``query`` string.

    Returns:
        ``QueryResponse`` with answer, citations, and conflict flags.
    """
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    initial_state = {
        "query": request.query,
        "retry_count": 0,
        "needs_hitl": False,
        "routed_to": None,
        "retrieved_docs": None,
        "answer": None,
        "critique": None,
        "critique_score": None,
        "hitl_response": None,
        "messages": [],
    }

    result = agent_app.invoke(initial_state, config=config)

    # when graph hits interrupt(), result may be incomplete
    answer = result.get("answer") or "This query requires human review."
    needs_hitl = result.get("needs_hitl", False) or result.get("answer") is None

    return QueryResponse(
        answer=answer,
        citations=_extract_citations(answer),
        needs_hitl=needs_hitl,
        critique_score=result.get("critique_score"),
        thread_id=thread_id if needs_hitl else None,
    )


@router.post("/hitl/respond")
async def hitl_respond(request: HITLReviewRequest) -> dict:
    """Accept a human reviewer's decision and resume a suspended graph run.

    Args:
        request: ``HITLReviewRequest`` with ``thread_id`` and ``response``.
    """
    config = {"configurable": {"thread_id": request.thread_id}}
    agent_app.invoke({"hitl_response": request.response}, config=config)
    return {"status": "resumed", "thread_id": request.thread_id}


@router.post("/ingest")
async def trigger_ingestion(background_tasks=None) -> dict:
    """Kick off a background document ingestion job."""
    return IngestResponse(
        status="not_implemented",
        message="Ingestion triggered via CLI. API trigger coming soon.",
    )
