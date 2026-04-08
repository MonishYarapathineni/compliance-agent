# CLAUDE.md — Compliance Policy Agent

This file gives Claude Code the context it needs to work effectively in this repo.
project uses a venv at ./venv

## Project overview

A LangGraph-based agentic system that ingests company policy documents, answers
employee compliance questions with cited responses, detects policy conflicts, and
routes ambiguous queries to a human reviewer (HITL).

## Repo layout

```
src/
  ingestion/   — document loading, chunking, vector store (Chroma)
  agent/       — LangGraph graph + nodes (router, retriever, conflict, critic, hitl)
  evals/       — RAGAS + LLM-judge evaluation harness
  api/         — FastAPI app served via uvicorn
tests/         — pytest suite mirroring src/
notebooks/     — Jupyter experiments (not production code)
data/raw/      — drop raw policy PDFs/DOCX here (git-ignored)
data/processed/— Chroma persisted index (git-ignored)
```

## Key commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API locally
uvicorn src.api.main:app --reload

# Run tests
pytest tests/ -v

# Lint + format
ruff check src/ tests/
ruff format src/ tests/

# Start all services via Docker
docker compose up
```

## Tech stack

| Layer | Library |
|---|---|
| Agent framework | LangGraph |
| LLM calls | LangChain + OpenAI |
| Vector store | Chroma |
| API | FastAPI + Pydantic v2 |
| Evaluation | RAGAS, custom LLM-judge |
| Testing | pytest |
| Linting | ruff, mypy |

## Environment variables

Copy `.env.example` → `.env` and fill in values.  The minimum required key is
`OPENAI_API_KEY`.  LangSmith tracing keys are optional but recommended.

## Development conventions

- Every node function takes a plain `dict` (AgentState) and returns a partial
  state dict — never mutate the input dict in place.
- All LLM calls go through LangChain abstractions so the model can be swapped
  via env var without code changes.
- Tests that touch LLM or vector-store APIs must mock those calls.
- `data/` directories are git-ignored; run the ingestion pipeline locally after
  cloning to populate the vector store.
