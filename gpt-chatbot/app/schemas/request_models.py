from pydantic import BaseModel

class TextGenerationRequest(BaseModel):
    prompt: str
    max_length: int = None
    num_return_sequences: int = None