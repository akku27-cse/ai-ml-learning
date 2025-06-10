from transformers import BlenderbotTokenizer, BlenderbotForConditionalGeneration
import torch
from app.config import settings

class ChatModelService:
    def __init__(self):
        self.model_name = settings.model_name
        self.tokenizer = BlenderbotTokenizer.from_pretrained(self.model_name)
        self.model = BlenderbotForConditionalGeneration.from_pretrained(self.model_name)
        
    def generate_response(self, message: str) -> str:
        inputs = self.tokenizer([message], return_tensors='pt')
        reply_ids = self.model.generate(**inputs)
        return self.tokenizer.batch_decode(reply_ids, skip_special_tokens=True)[0]

model_service = ChatModelService()