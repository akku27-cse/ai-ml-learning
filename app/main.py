from fastapi import FastAPI
from api.chat import router as chat_router

app = FastAPI(title="Open-Source Chatbot API")

app.include_router(chat_router, prefix="/chat", tags=["chat"])
