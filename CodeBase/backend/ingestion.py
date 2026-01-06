import os
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import re

# Get absolute path to backend directory
BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BACKEND_DIR, "backend", "data")
DB_PATH = os.path.join(BACKEND_DIR, "backend", "chroma_db")

def get_splitter_for_document(filename):
    """Return appropriate splitter based on document type."""
    filename_lower = filename.lower()
    
    if 'cli reference' in filename_lower:
        # CLI Reference - small chunks, custom separators for commands
        print(f"Strategy: CLI Reference for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=50,
            separators=["\n\n\n", "\n\n", "\nget_", "\nset_", "\nadd_", "\n"]
        )
    
    elif 'events reference' in filename_lower:
        # Events Guide - table-focused
        print(f"Strategy: Events Reference for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100,
            separators=["\n\n\n", "\nTable ", "\n\n", "\n"]
        )
    
    elif 'security' in filename_lower:
        # Security Guide
        print(f"Strategy: Security Guide for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=800,
            chunk_overlap=150,
            separators=["\n\n\n", "\nTable ", "\n## ", "\n\n"]
        )
    
    elif 'install' in filename_lower or 'deploy' in filename_lower:
        # Installation Guide
        print(f"Strategy: Installation Guide for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=["\nChapter ", "\n## ", "\nStep ", "\n\n", "\n"]
        )
    
    elif 'admin' in filename_lower:
        # Admin Guide - larger chunks
        print(f"Strategy: Admin Guide for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=1200,
            chunk_overlap=200,
            separators=["\nChapter ", "\n## ", "\nNOTE:", "\n\n"]
        )
    
    elif 'product guide' in filename_lower:
        # Product Guide - conceptual
        print(f"Strategy: Product Guide for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=900,
            chunk_overlap=250,
            separators=["\n\n\n", "\n## ", "\n\n"]
        )
    
    else:
        # Default
        print(f"Strategy: Default for {filename}")
        return RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

def ingest_docs():
    all_chunks = []
    
    if not os.path.exists(DATA_PATH):
        print(f"Data directory {DATA_PATH} not found.")
        return

    print(f"Scanning {DATA_PATH} for documents...")
    for file in os.listdir(DATA_PATH):
        file_path = os.path.join(DATA_PATH, file)
        documents = []
        
        # Load
        if file.endswith(".pdf"):
            loader = PyPDFLoader(file_path)
            documents = loader.load()
        elif file.endswith(".docx"):
            loader = Docx2txtLoader(file_path)
            documents = loader.load()
        else:
            continue
            
        if not documents:
            continue
            
        # Split using custom strategy
        splitter = get_splitter_for_document(file)
        chunks = splitter.split_documents(documents)
        
        # Enrich Metadata
        for chunk in chunks:
            chunk.metadata['source_req_file'] = file
            # Simple content tagging
            if 'port' in chunk.page_content.lower():
                chunk.metadata['topic'] = 'networking'
            if any(cmd in chunk.page_content for cmd in ['get_', 'set_', 'add_']):
                chunk.metadata['topic'] = 'cli_command'
        
        all_chunks.extend(chunks)
        print(f"Processed {file}: {len(chunks)} chunks")
    
    if not all_chunks:
        print("No chunks to ingest.")
        return

    print(f"Total chunks to ingest: {len(all_chunks)}")
    
    embedding_function = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    print(f"Creating/Updating Vector Store in {DB_PATH}...")
    vectorstore = Chroma.from_documents(
        documents=all_chunks,
        embedding=embedding_function,
        persist_directory=DB_PATH,
        collection_name="omniassist_rag"
    )
    print(f"Successfully ingested into {DB_PATH}")

if __name__ == "__main__":
    ingest_docs()
