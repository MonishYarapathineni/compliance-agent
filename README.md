Five-node LangGraph `StateGraph` with two conditional edges. State flows 
as a typed `AgentState` dict through each node, which returns a partial 
update. The critic loop retries retrieval up to 2 times before escalating 
to human review.

## Tech Stack

- **Agent:** LangGraph (StateGraph, conditional edges, interrupt)
- **LLM:** GPT-4o-mini (router, retriever, conflict, critic — all temp=0)
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector store:** Pinecone (hosted, persistent)
- **API:** FastAPI with Pydantic v2 schemas
- **Evals:** RAGAS (faithfulness, answer relevancy, context recall)
- **Experiment tracking:** MLflow
- **Frontend:** React + Tailwind CSS
- **Infra:** Docker, GitHub Actions CI/CD, Fly.io, Vercel

## Evaluation Results

| Metric | Score |
|--------|-------|
| Faithfulness | 0.84 |
| Answer relevancy | 0.98 |
| Context recall | 0.89 |

Evaluated against 6 golden test cases across 3 OPM policy documents.
Faithfulness gap (0.16) attributed to the conflict node drawing implicit 
conclusions not explicitly stated in source chunks — a known tradeoff in 
cross-document reasoning tasks.

## End-to-End Test Results

| Query type | Route | Critic score | Result |
|------------|-------|--------------|--------|
| "What happens to my pay during a weather emergency?" | retriever | 1.0 | Cited answer, pages 2-4 |
| "How do elder care and emergency leave differ on telework?" | conflict | 1.0 | Cross-document conflict analysis |
| "I have a complicated situation with my leave" | hitl | — | Paused for human review |

## Architecture Decisions

User query
    │
    ▼
[Router] ── classifies query (factual / conflict / ambiguous)
    │
    ├── factual ──► [Retriever] ── RAG + LLM synthesis
    │                    │
    ├── conflict ─► [Conflict] ── cross-document analysis
    │                    │
    └── ambiguous ► [HITL] ◄─────────────────────────┐
                         │                            │
                    [Critic] ── score < 0.7 ──────────┘
                         │
                    score ≥ 0.7 ──► END


Five-node LangGraph `StateGraph` with two conditional edges.

### Chunking strategy
Tested recursive vs character splitting on 96 pages of OPM compliance documents.
Character splitting produced 96 chunks — one per page — exceeding the token 
target and failing to split dense policy text meaningfully. Recursive splitting 
produced 478 chunks by trying paragraph, sentence, and word boundaries in order.

Tested 512/64 vs 1024/128 chunk size and overlap. At 512 characters, government 
policy clauses were cut mid-sentence, making chunks insufficient to answer 
correctly. At 1024/128, complete policy clauses are preserved. Higher token cost 
per retrieval is an acceptable tradeoff for answer reliability in a compliance 
context where incomplete rules produce harmful answers.

Noise filtering drops chunks under 100 characters and page 0 (cover pages). 
TOC detection uses dot-pattern heuristics.

### Retrieval
K=6 for factual queries, K=8 for conflict detection to cast a wider net across 
documents. Embedding model: `text-embedding-3-small` (1536 dimensions).

### Critic loop
Initial implementation returned raw retrieved chunks as the answer — scored 0.4 
on RAGAS faithfulness. Adding an LLM synthesis step brought scores to 1.0. The 
critic loop caught this gap before manual testing would have. Max 2 retries 
before HITL escalation to prevent infinite loops.

### Experiment tracking
MLflow tracks all chunking experiments — chunk size, overlap, strategy, total 
chunks produced, and noise filtered. RAGAS eval scores logged per run enabling 
regression detection on each deploy.

## API

### POST /api/v1/query
```json
// request
{"query": "What happens to my pay during a weather emergency?"}

// response
{
  "answer": "...",
  "citations": [{"source": "emergencybenefits.pdf", "page": 2}],
  "needs_hitl": false,
  "critique_score": 1.0,
  "thread_id": null
}
```

### POST /api/v1/hitl/respond
```json
{"thread_id": "uuid", "response": "Reviewer's verified answer"}
```

### GET /api/v1/health
```json
{"status": "ok"}
```

## Running Locally

```bash
# clone and install
git clone https://github.com/monishy1/compliance-agent
cd compliance-agent
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# configure
cp .env.example .env
# add OPENAI_API_KEY and PINECONE_API_KEY to .env

# run
uvicorn src.api.main:app --reload --port 8000
```

## Docker

```bash
docker build -t compliance-agent:latest .
docker run -p 8000:8000 --env-file .env compliance-agent:latest
```

## CI/CD

GitHub Actions runs on every push to `main`:
1. Ruff lint and format check
2. Pytest unit tests  
3. Docker build verification

## Project Structure

| Path | Purpose |
|------|---------|
| `src/ingestion/` | PDF loading, chunking, Pinecone indexing |
| `src/agent/` | LangGraph graph, state schema, nodes |
| `src/evals/` | RAGAS eval harness, golden test cases |
| `src/api/` | FastAPI routes and Pydantic schemas |
| `frontend/` | React + Tailwind chat UI |
| `tests/` | pytest unit tests |
| `notebooks/` | Chunking experiments, MLflow tracking |

## Known Limitations

- TOC detection uses dot-pattern heuristics — future fix: Docling section-aware splitting
- Critic score is a single float — does not distinguish faithfulness vs completeness failures
- No persistent conversation memory across sessions
- Conflict analysis returned as prose rather than structured objects
