"""API route definitions.

Registers all HTTP endpoints for the compliance agent service, including
query submission, HITL reviewer callbacks, ingestion triggers, and health
checks.
"""

from __future__ import annotations

# TODO: from fastapi import APIRouter, HTTPException, BackgroundTasks
# TODO: from src.api.schemas import QueryRequest, QueryResponse, HITLReviewRequest
# TODO: from src.agent.graph import app as agent_app

router = None  # TODO: router = APIRouter()


# TODO: @router.get("/health")
async def health_check() -> dict:
    """Return service liveness status."""
    # TODO: return {"status": "ok"}
    pass


# TODO: @router.post("/query", response_model=QueryResponse)
async def query(request=None) -> dict:
    """Accept a user compliance question and return the agent's answer.

    Args:
        request: ``QueryRequest`` body containing ``query`` string.

    Returns:
        ``QueryResponse`` with answer, citations, and conflict flags.
    """
    # TODO: state = {"query": request.query}
    # TODO: result = agent_app.invoke(state)
    # TODO: return QueryResponse(**result)
    pass


# TODO: @router.post("/hitl/respond")
async def hitl_respond(request=None) -> dict:
    """Accept a human reviewer's decision and resume a suspended graph run.

    Args:
        request: ``HITLReviewRequest`` with ``thread_id`` and ``response``.
    """
    # TODO: agent_app.update_state({"configurable": {"thread_id": request.thread_id}},
    #                               {"hitl_response": request.response})
    pass


# TODO: @router.post("/ingest")
async def trigger_ingestion(background_tasks=None) -> dict:
    """Kick off a background document ingestion job."""
    # TODO: background_tasks.add_task(run_ingestion_pipeline)
    # TODO: return {"status": "ingestion started"}
    pass
