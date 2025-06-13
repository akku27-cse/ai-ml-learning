from fastapi import FastAPI
from app.routes.chat import router as chat_router

app = FastAPI(title="Memory Chatbot with Correction Store")

app.include_router(chat_router, prefix="/api")