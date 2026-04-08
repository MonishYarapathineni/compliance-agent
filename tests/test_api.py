"""Tests for the FastAPI layer (src/api/).

Uses FastAPI's ``TestClient`` to send HTTP requests against the application
and asserts correct status codes, response shapes, and error handling.
"""

from __future__ import annotations

import pytest

# TODO: from fastapi.testclient import TestClient
# TODO: from src.api.main import create_app

# TODO: @pytest.fixture
# TODO: def client():
#     app = create_app()
#     return TestClient(app)


class TestHealthEndpoint:
    """Tests for GET /api/v1/health."""

    def test_health_returns_200(self, client=None):
        """Health endpoint should return HTTP 200 with status ok."""
        # TODO: response = client.get("/api/v1/health")
        # TODO: assert response.status_code == 200
        # TODO: assert response.json()["status"] == "ok"
        pass


class TestQueryEndpoint:
    """Tests for POST /api/v1/query."""

    def test_query_returns_answer(self, client=None):
        """A well-formed query should return an answer with citations."""
        # TODO: payload = {"query": "What is the PTO accrual policy?"}
        # TODO: response = client.post("/api/v1/query", json=payload)
        # TODO: assert response.status_code == 200
        # TODO: data = response.json()
        # TODO: assert "answer" in data
        # TODO: assert "citations" in data
        pass

    def test_empty_query_returns_422(self, client=None):
        """An empty query body should fail Pydantic validation with HTTP 422."""
        # TODO: response = client.post("/api/v1/query", json={})
        # TODO: assert response.status_code == 422
        pass


class TestHITLEndpoint:
    """Tests for POST /api/v1/hitl/respond."""

    def test_hitl_respond_accepts_reviewer_input(self, client=None):
        """A valid HITL response should return HTTP 200."""
        # TODO: payload = {"thread_id": "abc-123", "response": "Approved per legal review."}
        # TODO: response = client.post("/api/v1/hitl/respond", json=payload)
        # TODO: assert response.status_code == 200
        pass
