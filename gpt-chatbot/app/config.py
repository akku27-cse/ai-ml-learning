from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "GPT-2 API"
    model_name: str = "gpt2"
    max_length: int = 100
    num_return_sequences: int = 1

    class Config:
        env_file = ".env"

settings = Settings()