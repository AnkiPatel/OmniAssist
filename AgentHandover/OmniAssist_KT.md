# OmniAssist Knowledge Transfer (KT) Material

## 1. Project Overview
**OmniAssist** is a locally-hosted RAG (Retrieval-Augmented Generation) application designed to serve as an intelligent assistant for specific domain knowledge (stored in PDF/DOCX files).

The system is built to be **"Agent-Ready"**, meaning it is self-contained, deterministic, and easy for AI Agents (like the one currently assisting you) to pick up, understand, and extend.

---

## 2. Technology Stack

### Backend & API
*   **Language**: Python 3.x
*   **Framework**: **FastAPI**
    *   *Reason*: High performance, automatic Swagger UI documentation for easy API testing, and native async support.
*   **Server**: Uvicorn (ASGI server)

### AI & Orchestration
*   **Orchestrator**: **LangChain**
    *   *Reason*: Industry standard for building RAG chains, handling prompt templates, and managing vector store interactions.
*   **LLM Provider**: **Groq**
    *   *Model*: `llama3-70b-8192`
    *   *Reason*: Extremely fast inference speeds (critical for chat interfaces) and a generous free tier for prototyping.
*   **Embeddings**: **HuggingFace** (`langchain-huggingface`)
    *   *Model*: `all-MiniLM-L6-v2`
    *   *Reason*: Runs locally (no API cost), lightweight, and fast. Ensures the "retrieval side" of the RAG pipeline is fully private and cost-free.

### Database & Storage
*   **Vector Database**: **ChromaDB**
    *   *Persistence*: Local file storage (`./backend/chroma_db`)
    *   *Reason*: No need for external server setup (like Pinecone/Qdrant cloud). Keeps the project self-contained and easy to clone/run.

### Document Processing
*   **Libraries**: `pypdf`, `docx2txt`, `tiktoken`
*   **Chunking**: RecursiveCharacterTextSplitter (LangChain)

---

## 3. AI Components & Architecture

### A. The RAG Pipeline (`rag.py`)
The core logic follows the standard RAG pattern:
1.  **Ingest**: Documents are loaded and split into chunks.
2.  **Embed**: Chunks are converted to vector embeddings using HuggingFace.
3.  **Store**: Vectors are saved in ChromaDB.
4.  **Retrieve**: User queries are embedded and matched against stored vectors (Semantic Search).
5.  **Generate**: Top matches + User Query are sent to Groq (Llama3) to generate the answer.

### B. Intelligent Ingestion (`ingestion.py`)
Unlike simple RAG setups, OmniAssist implements **Content-Aware Chunking**.
*   **Logic**: The system detects the *type* of document being ingested (e.g., a "CLI Reference" vs "User Guide") by analyzing the filename or content.
*   **Adaptive Strategy**:
    *   *Reference Manuals*: Smaller chunk sizes with strictly defined separators (preserving command syntax).
    *   *Narrative Guides*: Larger chunk sizes with high overlap to maintain context flow.
*   **Benefit**: This significantly improves retrieval accuracy. Technical facts aren't cut in half, and conceptual explanations aren't fragmented.

### C. Role-Based Personality (`roles.py`)
The system uses "System Prompts" to switch personas based on user needs.
*   **Learner Role**: Explains concepts simply, step-by-step, avoiding jargon.
*   **Support Role**: Focuses on troubleshooting, error codes, and direct solutions.
*   **Benefit**: Makes the same underlying data useful for different user intents (learning vs. fixing).

---

## 4. Architectural Decision Reasoning

| Decision | Why it was made | Trade-offs |
| :--- | :--- | :--- |
| **Local Vector Store (Chroma)** | Privacy & Simplicity. A developer can clone the repo and run it immediately without signing up for a cloud vector DB. | Harder to scale to millions of docs compared to a managed cloud solution. |
| **Groq (Llama3)** | **Speed**. RAG apps often feel slow due to retrieval + generation latency. Groq provides near-instant generation. | Dependency on Groq API availability (vs running a local LLM via Ollama, which would be slower on non-GPU laptops). |
| **LangChain Framework** | Abstraction. Allows swapping components (e.g., changing Chroma to FAISS or Groq to OpenAI) with minimal code changes. | Adds a layer of complexity/dependency management compared to raw API calls. |
| **"AgentHandover" Folder** | **Continuity**. Explicitly separating code from *instructional meta-data* helps future AI agents understand the project faster than reading code alone. | Requires maintenance to keep documentation in sync with code changes. |
| **Custom Chunking Strategies** | **Accuracy**. "One size fits all" chunking (e.g., just 1000 tokens) is the #1 cause of bad RAG performance on technical docs. | Adds logic complexity to the ingestion pipeline. |

---

## 5. Next Steps for Handover
1.  **Verify**: Run `backend/ingestion.py` to populate your local database.
2.  **Run**: Start the server to test the API.
3.  **Extend**: If adding a Frontend (Phase 1b), consume the `POST /chat` endpoint documented in Swagger UI.
