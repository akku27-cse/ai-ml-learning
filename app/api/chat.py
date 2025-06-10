from fastapi import APIRouter, HTTPException
from schemas.chat import ChatRequest, ChatResponse
from core.model import generate_response

router = APIRouter()

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    user_message = request.message.strip()
    if not user_message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    bot_response = generate_response(user_message)
    return ChatResponse(reply=bot_response)
