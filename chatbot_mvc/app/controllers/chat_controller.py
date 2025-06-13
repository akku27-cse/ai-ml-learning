from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.services.chat_service import get_response

async def handle_user_message(request: ChatRequest) -> ChatResponse:
    reply = await get_response(request.user_id, request.message)
    return ChatResponse(reply=reply)