# Changelog

## [Unreleased]

## [0.3.0] - 2026-06-18
### Added
- CI-Pipeline mit GitHub Actions: `ruff`-Lint + Offline-Unit-Tests bei jedem Push/PR auf `master`, Status-Badge im README
- Tests in offline-Unit (`test_chunk_*`, `test_health_*`, `test_query_empty`) vs. `@pytest.mark.integration` (brauchen `OPENAI_API_KEY` + ChromaDB) aufgeteilt

### Fixed
- Lazy Initialization der RAG-Chain in `app/api.py`: Chain wird erst bei der ersten Anfrage gebaut, nicht beim Import — verhindert `OpenAIError` beim Starten ohne Key

### Removed
- Obsolete `[tool.vercel]`-Config aus `pyproject.toml` entfernt (Deployment-Ziel: AWS)

## [0.2.0] - 2026-06-17
### Added
- CLI (`app/cli.py`): interaktive Terminal-REPL, startbar via `uv run rag-chat`
- Titelseiten-Extraktion beim Ingest: erste Seite jedes PDFs wird in `data/document_info.json` gespeichert und als fixer Kontext in jeden Prompt injiziert

### Changed
- Chunk-Größe von 500 auf 1000 Token erhöht, Overlap von 50 auf 100 Token
- Retrieval von k=4 auf k=6 Chunks erhöht
- Ingest löscht ChromaDB vor jedem Lauf, um veraltete Chunks zu vermeiden

## [0.1.0] - 2026-06-12
### Added
- RAG-Pipeline mit LangChain, ChromaDB, OpenAI (Embeddings + GPT-3.5-turbo)
- FastAPI-Backend, Streamlit-Frontend
- Docker/docker-compose-Setup
- pytest-Testsuite