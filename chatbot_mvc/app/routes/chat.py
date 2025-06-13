from fastapi import APIRouter, Body
from app.controllers.chat_controller import handle_user_message
from app.schemas.chat_schema import ChatRequest, ChatResponse

router = APIRouter(tags=["Chatbot"])

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest = Body(...)):
    return await handle_user_message(request)