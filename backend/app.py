from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="OmniAssist API")

@app.on_event("startup")
async def startup_event():
    print("OmniAssist Backend Started")

@app.get("/")
async def root():
    return {"message": "OmniAssist API is running"}
