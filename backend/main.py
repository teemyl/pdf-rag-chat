import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_anthropic import ChatAnthropic
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from qdrant_client import QdrantClient

# Load env variables
load_dotenv()

app = FastAPI(title="RAG Demo API")

# Setup CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
COLLECTION_NAME = "ebooks"
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class ChatRequest(BaseModel):
    query: str

def get_rag_chain():
    # Setup Vector Store connection
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    try:
        client = QdrantClient(url=QDRANT_URL)
        qdrant = QdrantVectorStore(client=client, collection_name=COLLECTION_NAME, embedding=embeddings)
        retriever = qdrant.as_retriever(search_kwargs={"k": 5})
    except Exception as e:
        print(f"Error connecting to Qdrant: {e}")
        return None

    # Setup LLM
    if not ANTHROPIC_API_KEY or ANTHROPIC_API_KEY == "your_anthropic_api_key_here":
        raise ValueError("ANTHROPIC_API_KEY is not set or invalid.")

    llm = ChatAnthropic(
        model="claude-sonnet-4-6",
        temperature=0,
        max_tokens=1024,
        timeout=None,
        max_retries=2,
    )

    # Setup Prompt
    template = """Answer the question based ONLY on the following context:

<context>
{context}
</context>

Question:

{question}

Answer the question based on the context and the following guidelines:
<answer_guidelines>
- If you don't know the answer based on the context, say "I cannot answer this based on the provided ebooks."
- Never start an answer with "Based on the" or "According to the" or any similar phrase that indicates that you are answering based on the provided context.
- Answer the question in a concise and informative manner.
</answer_guidelines>
"""
    prompt = ChatPromptTemplate.from_template(template)

    # Setup Chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        chain = get_rag_chain()
        if not chain:
            raise HTTPException(status_code=500, detail="Failed to initialize RAG chain. Ensure Qdrant is running and ingested.")

        response = chain.invoke(request.query)
        return {"answer": response}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok"}
