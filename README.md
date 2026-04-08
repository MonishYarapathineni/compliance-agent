# compliance-agent

An agentic system that ingests a company's internal policy documents and answers
employee questions with cited, auditable responses, flags policy conflicts, and
routes ambiguous queries to a human reviewer.

## Architecture

```
User query
    │
    ▼
┌─────────┐    ┌───────────┐    ┌──────────┐    ┌────────┐
│ Router  │───▶│ Retriever │───▶│ Conflict │───▶│ Critic │
└─────────┘    └───────────┘    └──────────┘    └────────┘
                                      │               │
                                      ▼               ▼
                                 ┌─────────┐     Answer / retry
                                 │  HITL   │
                                 └─────────┘
                                      │
                                      ▼
                               Human reviewer
```

All nodes are wired as a `StateGraph` in `src/agent/graph.py`.  State flows
as a typed dict (`AgentState`) through each node, which returns a partial
update.

## Quick start

```bash
# 1. Clone and install
git clone <repo-url>
cd compliance-agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Configure secrets
cp .env.example .env
# edit .env — set OPENAI_API_KEY at minimum

# 3. Ingest policy documents
#    Drop PDFs / DOCX files into data/raw/, then:
# python -m src.ingestion   # TODO: add __main__ entrypoint

# 4. Run the API
uvicorn src.api.main:app --reload

# 5. Query the agent
curl -X POST http://localhost:8000/api/v1/query \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the maximum expense claim per diem?"}'
```

## Running tests

```bash
pytest tests/ -v
```

## Evaluation

```bash
# RAGAS metrics
python -m src.evals.ragas_eval

# LLM-judge batch scoring
python -m src.evals.llm_judge
```

## Docker

```bash
docker compose up
```

API available at `http://localhost:8000`, Chroma at `http://localhost:8001`.

## Project structure

| Path | Purpose |
|---|---|
| `src/ingestion/` | PDF/DOCX loading, chunking, Chroma indexing |
| `src/agent/` | LangGraph graph, state schema, nodes |
| `src/evals/` | RAGAS + LLM-judge eval harness |
| `src/api/` | FastAPI routes and Pydantic schemas |
| `tests/` | pytest test suite |
| `notebooks/` | Exploratory Jupyter notebooks |
| `data/raw/` | Raw policy documents (git-ignored) |
| `data/processed/` | Chroma vector index (git-ignored) |

## Architecture Decisions

### Chunking Strategy
After testing on 96 pages of OPM compliance policy documents across three handbooks
(elder care, emergency benefits, dismissal procedures), two decisions were made:

**Recursive over character splitting:**
Character splitting produced 96 chunks — one per page — consistently exceeding the 
token target and failing to split dense policy text meaningfully. Recursive splitting 
produced 478 chunks by trying paragraph, sentence, and word boundaries in order, 
staying within the token budget while preserving semantic coherence.

**Chunk size 1024/128 over 512/64:**
At 512 characters, dense government policy clauses were cut mid-sentence across chunk 
boundaries. For example, a clause defining advance payment calculation limits was split 
across two chunks, making either chunk insufficient to answer a compliance question 
correctly. At 1024/128, complete policy clauses are preserved in single chunks. The 
higher token cost per retrieval is an acceptable tradeoff for answer reliability in a 
compliance context where incomplete rules can produce harmful answers.

**Noise filtering:**
Chunks under 100 characters are dropped at index time. Cover pages, table of contents 
entries, and section headers were being indexed and polluting retrieval results.
