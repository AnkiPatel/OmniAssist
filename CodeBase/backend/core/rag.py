import os
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from core.roles import get_prompt_by_role

# Initialize Global Components
# Using local persistence for ChromaDB
# rag.py is in backend/core/rag.py
# We need to reach backend/chroma_db
CORE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.dirname(CORE_DIR)
DB_PATH = os.path.join(BACKEND_DIR, "chroma_db")

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=DB_PATH, 
    embedding_function=embedding_function,
    collection_name="omniassist_rag"
)
retriever = vectorstore.as_retriever()

llm = ChatGroq(
    temperature=0,
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def get_rag_chain(role: str):
    prompt = get_prompt_by_role(role)
    document_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(retriever, document_chain)
    return retrieval_chain

def query_rag(message: str, role: str):
    chain = get_rag_chain(role)
    response = chain.invoke({"input": message})
    return response["answer"]
