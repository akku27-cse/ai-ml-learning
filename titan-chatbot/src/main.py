from fastapi import FastAPI
from controllers import chat_controller

app = FastAPI()
app.include_router(chat_controller.router)
