from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from services.agent import handle_chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# request schema
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]


# ✅ health endpoint
@app.get("/health")
def health():
    return {"status": "ok"}


# ✅ chat endpoint
@app.post("/chat")
def chat(request: ChatRequest):
    messages = [msg.dict() for msg in request.messages]
    response = handle_chat(messages)
    return response