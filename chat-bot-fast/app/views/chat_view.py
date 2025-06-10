from fastapi import APIRouter
from app.controllers.chat_controller import router as chat_router

router = APIRouter()
router.include_router(chat_router, prefix="/api/v1", tags=["chat"])

def init_app(app):
    app.include_router(router)