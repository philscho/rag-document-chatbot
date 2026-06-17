from pathlib import Path
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.vectorstores import VectorStoreRetriever
from dotenv import load_dotenv

load_dotenv()

CHROMA_DIR = Path("data/chroma_db")


def load_vectorstore() -> Chroma:
    """Lädt bestehende ChromaDB vom Disk."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embeddings
    )


def get_retriever(k: int = 6) -> VectorStoreRetriever:
    """Gibt einen Retriever zurück, der die k relevantesten Chunks findet."""
    vectorstore = load_vectorstore()
    return vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )


if __name__ == "__main__":
    retriever = get_retriever()
    #query = "What is contrastive learning?"
    #query = "What are multi-modal models?"
    query = "What are the findings of the thesis?"
    results = retriever.invoke(query)

    print(f"Query: {query}")
    for i, doc in enumerate(results):
        print(f"\n--- Chunk {i+1} (Seite {doc.metadata["page"]}, {doc.metadata["source"]}) ---")
        print(doc.page_content)
