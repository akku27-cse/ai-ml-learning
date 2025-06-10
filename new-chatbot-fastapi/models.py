from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Message(BaseModel):
    content: str
    role: str  # "user" or "assistant"

class Conversation(BaseModel):
    user_id: str
    user_message: str
    bot_response: str
    timestamp: datetime = datetime.utcnow()
    context: Optional[str] = None

class LearnedResponse(BaseModel):
    input_pattern: str
    response: str
    confidence: int = 1
    last_used: datetime = datetime.utcnow()