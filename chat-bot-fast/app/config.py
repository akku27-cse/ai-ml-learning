# Old version (causing error)
# from pydantic import BaseSettings

# New version (correct)
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Chatbot API"
    model_name: str = "facebook/blenderbot-400M-distill"
    
    class Config:
        env_file = ".env"

settings = Settings()