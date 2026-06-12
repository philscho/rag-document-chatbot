from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from app.retriever import get_retriever

load_dotenv()

PROMPT_TEMPLATE = """
You are an assistant that answers questions based strictly on the provided context.
If the answer is not in the context, say "I could not find an answer in the provided documents."
Always mention which page(s) you found the information on.

Context:
{context}

Question:
{question}
"""


def format_docs(docs) -> str:
    """Formatiert Chunks zu einem einzelnen Kontext-String mit Quellenangaben."""
    return "\n\n".join(
        f"[Page {doc.metadata["page"]}, {doc.metadata["source"]}]\n{doc.page_content}"
        for doc in docs
    )


def build_chain():
    """Baut die RAG-Chain zusammen."""
    retriever = get_retriever()
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain


if __name__ == "__main__":
    chain = build_chain()
    #query = "What are the main findings regarding the CLIP loss function?"
    query = "What was the research question or purpose of the thesis?"
    print(f"Query: {query}\n")
    response = chain.invoke(query)
    print(response)
