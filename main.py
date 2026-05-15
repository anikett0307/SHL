from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from services.agent import handle_chat
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ CORS (keep for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Schemas
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

# ✅ Root
@app.get("/")
def home():
    return {"message": "API running 🚀"}

# ✅ Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# ✅ Chat endpoint (ONLY ONE)
@app.post("/chat")
def chat(request: ChatRequest):
    messages = [msg.dict() for msg in request.messages]
    response = handle_chat(messages)
    return response