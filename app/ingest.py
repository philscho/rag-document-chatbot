from pathlib import Path
import pymupdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

DOCS_DIR = Path("data/documents")
CHROMA_DIR = Path("data/chroma_db")

# TODO: consider using LangChain's PyMuPDFLoader instead of manual PyMuPDF implementation
def load_pdfs(docs_dir: Path) -> list[dict]:
    """Lädt alle PDFs aus dem Verzeichnis. Gibt Liste von {text, source} zurück."""
    documents = []
    for pdf_path in docs_dir.glob("*.pdf"):
        doc = pymupdf.open(pdf_path)
        for page_num, page in enumerate(doc):
            text = page.get_text()
            if text.strip():
                documents.append({
                    "text": text,
                    "source": pdf_path.name,
                    "page": page_num + 1
                })
        print(f"Geladen: {pdf_path.name} ({len(doc)} Seiten)")
        doc.close()
    
    return documents


def chunk_documents(documents: list[dict]) -> list:
    """Splittet Dokumente in Chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", ". ", " ", ""]
    )

    from langchain_core.documents import Document
    langchain_docs = []
    for doc in documents:
        chunks = splitter.split_text(doc["text"])
        for chunk in chunks:
            langchain_docs.append(Document(
                page_content=chunk,
                metadata={"source": doc["source"],  "page": doc["page"]}
            ))
    
    print(f"Chunks erstellt: {len(langchain_docs)}")
    return langchain_docs


def embed_and_store(chunks: list) -> Chroma:
    """Embeddet Chunks und speichert in ChromaDB."""
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )
    
    print(f"In ChromaDB gespeichert: {CHROMA_DIR}")
    return vectorstore


def ingest(docs_dir: Path = DOCS_DIR) -> Chroma:
    documents = load_pdfs(docs_dir)
    if not documents:
        raise ValueError(f"Keine PDFs gefunden in {docs_dir}")
    chunks = chunk_documents(documents)
    
    return embed_and_store(chunks)


if __name__ == "__main__":
    ingest()