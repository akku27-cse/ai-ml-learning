from fastapi import APIRouter
from app.models.chat_model import ChatRequest, ChatResponse
from app.services.model_service import model_service

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    response = model_service.generate_response(request.message)
    return ChatResponse(
        response=response,
        conversation_id=request.conversation_id or "new-conversation"
    )