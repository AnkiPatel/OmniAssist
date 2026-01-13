# implementation_plan.md

## Objective
Build a Localhost RAG API (Phase 1a) using **Groq** (LLM), **ChromaDB** (Vector Store), and **FastAPI** (Backend).
The solution must be "Agent-Ready" - deterministic, clear, and using the existing `CodeBase` with preserved `.venv`.

## Constraints & Context
- **Root Directory**: `CodeBase`
- **Virtual Environment**: `.venv` (Existing, must be preserved)
- **Data Source**: `../KnowledgeBase` (Contains PDF/DOCX) -> copy to `CodeBase/contextsource/data`
- **Vector DB**: `ChromaDB` (Local persistence: `./backend/chroma_db`)
- **LLM**: `Groq` (Free Tier usage)
- **Embeddings**: `HuggingFace` (Local)
- **Chunking**: Custom strategy per file type (as per `PDF_Chunking_Strategy.md`)

## Directory Structure
```
CodeBase/
├── backend/
│   ├── app.py                # FastAPI Entry Point
│   ├── requirements.txt      # Python Dependencies
│   ├── ingestion.py          # ETL Script (Custom Chunking)
│   ├── core/
│   │   ├── __init__.py
│   │   ├── rag.py           # RAG Logic (ChromaDB + Groq)
│   │   └── roles.py         # System Prompts
│   └── data/                 # Local Documents (Copied)
├── frontend/                 # (Reserved for Phase 1b)
└── .env                      # Environment Variables
```

## Step-by-Step Execution Plan

### 1. Environment & Cleanup
**Action**: Clean `CodeBase` (rm `app.py`, `core`, etc) but **KEEP** `.venv`.
**Action**: Create directories `backend/core`, `backend/data`, `frontend`.

### 2. Dependencies (`backend/requirements.txt`)
**Content**:
```text
fastapi
uvicorn
python-dotenv
langchain
langchain-groq
langchain-community
langchain-huggingface
chromadb
sentence-transformers
pypdf
docx2txt
tiktoken
```
**Action**: `pip install -r backend/requirements.txt` (using `.venv`).

### 3. Data Setup
**Action**: Copy contents of `../KnowledgeBase` to `CodeBase/contextsource/data/`.
**Verify**: List `CodeBase/contextsource/data/` to confirm files.

### 4. Implementation Specs

#### A. `backend/core/roles.py`
**Ref**: System Prompts.
- **Learner**: "Explain concepts clearly, step-by-step."
- **Support**: "Troubleshoot issues, check logs, error codes."
- **Function**: `get_prompt_by_role(role_str) -> ChatPromptTemplate`

#### B. `backend/core/rag.py`
**Ref**: RAG Chain.
- **Imports**: `Chroma`, `ChatGroq`, `HuggingFaceEmbeddings`.
- **Setup**:
  - LLM: `ChatGroq(model="llama3-70b-8192")`
  - Embeddings: `HuggingFaceEmbeddings(model="all-MiniLM-L6-v2")`
  - VectorStore: `Chroma(persist_directory="./backend/chroma_db", embedding_function=embeddings)`
- **Function**: `query_rag(message, role) -> str`

#### C. `backend/ingestion.py`
**Ref**: ETL Pipeline with Multi-Strategy Chunking.
- **Imports**: `PyPDFLoader`, `Docx2txtLoader`, `RecursiveCharacterTextSplitter`.
- **Logic**:
  - Iterate files in `data/`.
  - **Determine Splitter**:
    - `CLI Reference`: Chunk=600, Overlap=50, Separators=`["\n\n", "\nget_", ...]`
    - `Events Guide`: Chunk=500, Overlap=100.
    - `Security Guide`: Chunk=800, Overlap=150.
    - `Install Guide`: Chunk=1000, Overlap=200.
    - `Admin Guide`: Chunk=1200, Overlap=200.
    - `Product Guide`: Chunk=900, Overlap=250.
    - Default: Chunk=1000, Overlap=200.
  - Split content using the selected splitter.
  - Enrich Metadata (filename, doc_type).
  - Store: `Chroma.from_documents(chunks, embeddings, persist_directory="./backend/chroma_db")`.

#### D. `backend/app.py`
**Ref**: API Surface.
- `POST /chat`: `{"query": "...", "role": "..."}` -> calls `query_rag`.
- `POST /ingest`: Trigger ingestion (sync for MVP).

### 5. Verification
1. **Ingest**: Run `python backend/ingestion.py`. Check `backend/chroma_db` created.
2. **Start**: `uvicorn backend.app:app --reload` (Run from CodeBase).
3. **Test**:
   ```bash
   curl -X POST http://localhost:8000/chat -d '{"query":"Subject?", "role":"learner"}'
   ```
