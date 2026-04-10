"""Pydantic request and response schemas.

Defines the data contracts for all API endpoints.  Using Pydantic ensures
automatic validation, serialisation, and OpenAPI documentation generation.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


class QueryRequest(BaseModel):
    """Request body for POST /query."""
    query: str = Field(..., description="The user's compliance question")
    session_id: Optional[str] = Field(None, description="Optional session identifier")



class Citation(BaseModel):
    """A single policy source cited in the answer."""

    source: str
    page: int



class QueryResponse(BaseModel):
    """Response body for POST /query."""

    answer: str
    citations: list[Citation]
    needs_hitl: bool
    critique_score: Optional[float]
    thread_id: Optional[str]


class HITLReviewRequest(BaseModel):
    """Request body for POST /hitl/respond."""

    thread_id: str
    response: str

class IngestResponse(BaseModel):
    
    status: str
    message: str