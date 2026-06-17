# Projektkontext

RAG-basierter Dokumenten-Chatbot. Nutzer laden PDFs hoch und stellen Fragen dazu in natürlicher Sprache.

Repo: github.com/philscho/rag-document-chatbot

## Stack

- LangChain (LCEL) – RAG-Pipeline-Orchestrierung
- OpenAI – Embeddings (text-embedding-3-small) und LLM (gpt-3.5-turbo)
- ChromaDB – Vector Store
- FastAPI – REST-Backend
- Streamlit – Chat-Frontend
- Docker / docker-compose – Containerisierung
- pytest – Tests
- uv – Paketverwaltung

## Architektur

app/ingest.py              – PDF laden, chunken (1000 Token, 100 Overlap), embedden; speichert Titelseiten in data/document_info.json; löscht ChromaDB vor jedem Lauf (sauberer State)
app/retriever.py           – Vector-Store-Abfrage (Top-6-Chunks)
app/chain.py                – RAG-Chain: Retriever → Prompt → LLM; lädt document_info.json als fixen Kontext (immer im Prompt)
app/api.py                   – FastAPI-Endpunkte
app/cli.py                    – Interaktive Terminal-REPL (`uv run rag-chat`)
frontend/streamlit_app.py – Chat-UI
tests/                          – pytest-Suite
data/document_info.json   – Titelseiten aller ingestierten PDFs (wird bei Ingest neu erzeugt)

## Konventionen

- Paketverwaltung ausschließlich über uv, nicht direkt mit pip
- Vor jedem Commit: `uv run pytest tests/ -v` muss grün sein
- Commit-Messages nach Conventional Commits (feat:, fix:, refactor:, docs:, test:, chore:)
- Ein Branch pro Issue/Feature, kein direktes Arbeiten auf main

## Designentscheidungen – nicht ohne Rückfrage ändern

- Chunk-Größe 1000 Token / 100 Overlap (erhöht von 500/50 wegen schlechter Retrieval-Qualität bei kurzen Chunks)
- Retrieval holt fix 6 Chunks (erhöht von 4)
- Titelseiten werden als fixer Kontext in den Prompt injiziert, nicht per Retrieval geholt – Grund: semantisches Retrieval findet Titelseiten bei Metafragen (Titel, Autor) zuverlässig nicht
- Ingest löscht ChromaDB immer komplett neu, um veraltete Chunks zu vermeiden

## Pflege dieser Datei

Nach Code-Änderungen prüfen: neues Modul/Architekturänderung, 
Tech-Stack-Wechsel, geänderte Konvention, neue oder revidierte 
Designentscheidung. Falls ja, betroffenen Abschnitt knapp 
aktualisieren. Falls nein, Datei unverändert lassen.