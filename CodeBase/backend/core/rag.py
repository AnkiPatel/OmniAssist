import os
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from core.roles import get_prompt_by_role

# Initialize Global Components
# Using local persistence for ChromaDB
DB_PATH = "./backend/chroma_db" if os.path.exists("./backend/chroma_db") else "./chroma_db"

embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory=DB_PATH, 
    embedding_function=embedding_function
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
