# OmniAssist API Usage Guide

This guide provides step-by-step instructions to start the Localhost RAG API and interact with it.

## 1. Prerequisites
- Ensure you have the `CodeBase` folder with the `.venv` virtual environment.
- Ensure `CodeBase/.env` contains your `GROQ_API_KEY`.

## 2. Start the Server
Open a terminal in the `CodeBase` directory and run:

### Windows (PowerShell)
```powershell
# 1. Activate Virtual Environment
.\.venv\Scripts\Activate.ps1

# 2. Start Uvicorn Server (Port 8001 recommended)
uvicorn backend.app:app --reload --port 8001
```

*Note: If port 8001 is busy, you can use any other port (e.g., 8000).*

## 3. API Endpoints

### `POST /chat`
Generates a RAG-based response using the local vector store and Groq LLM.

**URL**: `http://localhost:8001/chat`
**Content-Type**: `application/json`

**Request Body parameters:**
- `query` (string): The user's question.
- `role` (string): Contextual role ("learner" or "support").

## 4. Example Usage

### Scenario A: Learner Role
*Goal: Explain concepts clearly.*

**Request (cURL)**:
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the installation prerequisites?", "role": "learner"}'
```

**Request (PowerShell)**:
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/chat" -Method Post -ContentType "application/json" -Body '{"query": "What are the installation prerequisites?", "role": "learner"}'
```

**Example Response**:
```json
{
  "response": "Based on the provided context, the installation prerequisites for working in Microsoft Windows include having the following..."
}
```

---

### Scenario B: Support Role
*Goal: Troubleshoot issues and analyze errors.*

**Request (cURL)**:
```bash
curl -X POST http://localhost:8001/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Error 404 in event logs", "role": "support"}'
```

**Request (PowerShell)**:
```powershell
Invoke-RestMethod -Uri "http://localhost:8001/chat" -Method Post -ContentType "application/json" -Body '{"query": "Error 404 in event logs", "role": "support"}'
```

**Example Response**:

## 5. Shutting Down Gracefully

To stop the API server, you have two options depending on how you started it.

### Option A: Interactive Terminal (Ctrl+C)
If the server is running in a visible terminal window:
1.  Click inside the terminal window.
2.  Press `Ctrl + C`.
3.  The Uvicorn process will catch the signal and shut down gracefully.

### Option B: PowerShell Command (Process Kill)
If the server is running in the background or you want to script the shutdown:
```powershell
Stop-Process -Name "uvicorn" -Force -ErrorAction SilentlyContinue
```
