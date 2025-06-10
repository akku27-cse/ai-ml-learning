from fastapi import FastAPI
from app.views.chat_view import init_app
from app.config import settings

app = FastAPI(title=settings.app_name)
init_app(app)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)