# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Index documents (required before first use, clears and rebuilds ChromaDB)
uv run python -m app.ingest

# Start API backend
uv run uvicorn app.api:app --reload

# Start Streamlit frontend (separate terminal)
uv run streamlit run frontend/streamlit_app.py

# Interactive CLI
uv run rag-chat

# Run all tests
uv run pytest tests/ -v

# Run a single test
uv run pytest tests/test_chain.py::test_chunk_documents_basic -v

# Run with Docker
docker-compose up
```

Place PDFs in `data/documents/` before ingesting.

## Architecture

The pipeline has three stages that compose into a LangChain LCEL chain:

**Ingest** (`app/ingest.py`) — run once per document set, not at query time. Loads PDFs with PyMuPDF page by page, splits into 1000-token chunks (100 overlap), embeds with `text-embedding-3-small`, stores in ChromaDB. Always wipes ChromaDB first to avoid stale chunks. Also extracts the full text of page 1 of each PDF and saves it to `data/document_info.json` for use as fixed prompt context.

**Retrieval** (`app/retriever.py`) — loads the persisted ChromaDB and returns a LangChain retriever with `k=6` similarity search.

**Chain** (`app/chain.py`) — builds the LCEL chain: `{context: retriever | format_docs, question: passthrough, document_info: lambda} | prompt | ChatOpenAI | StrOutputParser`. The `document_info` key injects the title-page content from `data/document_info.json` into every prompt unconditionally — this is intentional, because semantic retrieval reliably fails to surface title pages for metadata questions (title, author, date).

The FastAPI app (`app/api.py`) and Streamlit frontend (`frontend/streamlit_app.py`) are thin wrappers: the API instantiates the chain once at startup and exposes `POST /query`; the frontend calls the API over HTTP (configurable via `API_URL` env var, defaults to `http://localhost:8000`).

## Environment

Requires a `.env` file with `OPENAI_API_KEY`. Copy `.env.example` to get started.

## Conventions

- Package management exclusively via `uv`, not pip
- `uv run pytest tests/ -v` must pass before every commit
- Conventional Commits (`feat:`, `fix:`, `refactor:`, `docs:`, `test:`, `chore:`)
- One branch per issue/feature, no direct commits to main

## Design decisions — do not change without discussion

- **Chunk size 1000 / overlap 100** — increased from 500/50; shorter chunks produced poor retrieval quality
- **k=6 retrieval** — increased from 4 for better context coverage
- **Title pages injected as fixed context** — semantic retrieval does not reliably find title pages for metadata queries; injecting them unconditionally solves this cleanly
- **Ingest always wipes ChromaDB** — prevents stale chunks from previous ingests from polluting results
