"""Pydantic request and response schemas.

Defines the data contracts for all API endpoints.  Using Pydantic ensures
automatic validation, serialisation, and OpenAPI documentation generation.
"""

from __future__ import annotations

# TODO: from pydantic import BaseModel, Field
# TODO: from typing import Optional


class QueryRequest:
    """Request body for POST /query."""

    # TODO: query: str = Field(..., description="The user's compliance question")
    # TODO: session_id: Optional[str] = Field(None, description="Optional session identifier")
    pass


class Citation:
    """A single policy source cited in the answer."""

    # TODO: source: str      — document filename
    # TODO: section: str     — section heading or page reference
    # TODO: snippet: str     — verbatim text excerpt
    pass


class ConflictSummary:
    """Summary of a detected policy conflict."""

    # TODO: description: str
    # TODO: affected_sources: list[str]
    pass


class QueryResponse:
    """Response body for POST /query."""

    # TODO: answer: str
    # TODO: citations: list[Citation]
    # TODO: conflicts: list[ConflictSummary]
    # TODO: needs_hitl: bool
    # TODO: thread_id: Optional[str]   — present when needs_hitl is True
    pass


class HITLReviewRequest:
    """Request body for POST /hitl/respond."""

    # TODO: thread_id: str
    # TODO: response: str    — reviewer's decision or clarification
    pass
