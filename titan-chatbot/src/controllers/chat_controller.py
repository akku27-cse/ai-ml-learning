from fastapi import APIRouter
from models.chat_model import ChatRequest, ChatResponse
from services.chat_service import process_chat

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat_endpoint(data: ChatRequest):
    reply = process_chat(data.user_id, data.message)
    return ChatResponse(reply=reply)
