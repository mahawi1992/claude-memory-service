from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import json
from typing import Dict, List
from datetime import datetime

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage (we'll upgrade to persistent storage later)
conversations: Dict[str, List[Dict]] = {}

@app.get("/")
async def root():
    return {"status": "Claude Memory Service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": str(datetime.now())}

@app.post("/memory/{conversation_id}")
async def save_memory(conversation_id: str, message: dict):
    if conversation_id not in conversations:
        conversations[conversation_id] = []
    
    message["timestamp"] = str(datetime.now())
    conversations[conversation_id].append(message)
    
    return {"status": "success", "message": "Memory saved"}

@app.get("/memory/{conversation_id}")
async def get_memory(conversation_id: str):
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return conversations[conversation_id]

@app.get("/conversations")
async def list_conversations():
    return {
        "conversations": list(conversations.keys()),
        "count": len(conversations)
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8283))
    uvicorn.run(app, host="0.0.0.0", port=port)