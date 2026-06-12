from langchain_core.documents import Document
from app.ingest import chunk_documents
from app.retriever import load_vectorstore, get_retriever
from fastapi.testclient import TestClient
from app.api import app

client = TestClient(app)


# --- Unit Test ---

def test_chunk_documents_basic():
    """chunk_documents() gibt bei normalem Input eine nicht-leere Liste zurück."""
    documents = [{"text": "This is a test document. " * 20, "source": "test.pdf", "page": 1}]
    chunks = chunk_documents(documents)
    assert len(chunks) > 0
    assert isinstance(chunks[0], Document)


def test_chunk_documents_empty():
    """chunk_documents() gibt bei leerem Input eine leere Liste zurück."""
    chunks = chunk_documents([])
    assert chunks == []


# --- Integration Tests ---

def test_vectorstore_loads():
    """ChromaDB lässt sich laden."""
    vectorstore = load_vectorstore()
    assert vectorstore is not None


def test_retriever_returns_results():
    """Retriever gibt bei einer bekannten Query mindestens einen Chunk zurück."""
    retriever = get_retriever(k=2)
    results = retriever.invoke("contrastive learning")
    assert len(results) > 0
    assert isinstance(results[0], Document)


def test_query_endpoint():
    """POST /query gibt einen nicht-leeren Answer-String zurück."""
    response = client.post("/query", json={"question": "What is contrastive learning"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert len(response.json()["answer"]) > 0


def test_query_endpoint_empty_question():
    """/query gibt 400 zurück bei leerem String."""
    response = client.post("/query", json={"question": "   "})
    assert response.status_code == 400


def test_health_endpoint():
    """GET /health gibt 200 zurück."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}