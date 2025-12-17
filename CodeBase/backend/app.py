from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import sys

# Add backend directory to sys.path to resolve core imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from core.rag import query_rag

app = FastAPI(title="OmniAssist API")

class ChatRequest(BaseModel):
    query: str
    role: str = "learner"

@app.on_event("startup")
async def startup_event():
    print("OmniAssist Backend Started")

@app.get("/")
async def root():
    return {"message": "OmniAssist API is running"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        response = query_rag(request.query, request.role)
        return {"response": response}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ingest")
async def ingest_endpoint():
    return {"message": "Please run 'python backend/ingestion.py' manually."}
