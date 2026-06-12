from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.chain import build_chain
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="RAG Document Chatbot")
chain = build_chain()


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    answer = chain.invoke(request.question)
    return QueryResponse(answer=answer)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
