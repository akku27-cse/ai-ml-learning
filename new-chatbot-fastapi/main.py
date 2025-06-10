from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from learning import find_best_learned_response, learn_from_conversation
from database import get_async_db
from models import Conversation, Message, LearnedResponse
from nlp_processor import nlp_processor
import os

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def chat_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/api/chat")
async def chat_with_bot(chat_request: ChatRequest, db=Depends(get_async_db)):
    try:
        user_id = chat_request.user_id or "anonymous"
        messages = chat_request.messages
        
        if not messages:
            raise HTTPException(status_code=400, detail="No messages provided")
        
        # Get the last user message
        last_user_message = next((msg.content for msg in reversed(messages) if msg.role == "user"), "")
        
        # First try to find a learned response
        learned_response = await find_best_learned_response(db, last_user_message)
        
        if learned_response:
            # Save conversation with learned response
            new_conversation = Conversation(
                user_id=user_id,
                user_message=last_user_message,
                bot_response=learned_response,
                context=str([msg.dict() for msg in messages])
            )
            await db["conversations"].insert_one(new_conversation.dict())
            
            return JSONResponse({
                "response": learned_response,
                "source": "learned_response"
            })
        
        # If no learned response, use our free NLP model
        openai_format_messages = [{"role": msg.role, "content": msg.content} for msg in messages]
        bot_response = nlp_processor.generate_response(openai_format_messages)
        
        # Save conversation
        new_conversation = Conversation(
            user_id=user_id,
            user_message=last_user_message,
            bot_response=bot_response,
            context=str([msg.dict() for msg in messages])
        )
        await db["conversations"].insert_one(new_conversation.dict())
        
        # Learn from this conversation
        await learn_from_conversation(db, last_user_message, bot_response)
        
        return JSONResponse({
            "response": bot_response,
            "source": "local_model"
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/conversations")
async def get_conversations(user_id: str = "anonymous", limit: int = 20, db=Depends(get_async_db)):
    conversations = await db["conversations"].find(
        {"user_id": user_id}
    ).sort(
        "timestamp", -1
    ).limit(limit).to_list(limit)
    
    return [{
        "user_message": conv["user_message"],
        "bot_response": conv["bot_response"],
        "timestamp": conv["timestamp"].isoformat()
    } for conv in conversations]

@app.get("/api/learned-responses")
async def get_learned_responses(limit: int = 20, db=Depends(get_async_db)):
    responses = await db["learned_responses"].find().sort(
        "confidence", -1
    ).limit(limit).to_list(limit)
    
    return [{
        "input_pattern": resp["input_pattern"],
        "response": resp["response"],
        "confidence": resp["confidence"],
        "last_used": resp["last_used"].isoformat()
    } for resp in responses]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)