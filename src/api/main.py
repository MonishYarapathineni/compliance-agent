"""FastAPI application factory.

Creates and configures the FastAPI ``app`` instance, registers routers,
sets up lifespan events (e.g. loading the vector store on startup), and
attaches middleware for CORS and request logging.
"""

# ruff: noqa: E402
from __future__ import annotations
from dotenv import load_dotenv

load_dotenv()
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
import os


from dotenv import load_dotenv
load_dotenv()

import os
print(f"PINECONE_API_KEY loaded: {bool(os.getenv('PINECONE_API_KEY'))}")
print(f"OPENAI_API_KEY loaded: {bool(os.getenv('OPENAI_API_KEY'))}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting compliance agent...")
    # startup: warm up vector store
    yield
    # shutdown: cleanup
    print("Shutting down...")


def create_app() -> object:
    """Instantiate and configure the FastAPI application.

    Returns:
        FastAPI: Configured application instance.
    """
    app = FastAPI(
        title="Compliance Policy Agent",
        description="LangGraph-powered compliance Q&A with citations",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(router, prefix="/api/v1")
    return app


# Entry point used by uvicorn: ``uvicorn src.api.main:app``
app = create_app()
