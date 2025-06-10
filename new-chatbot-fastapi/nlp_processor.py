from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import torch
import numpy as np
from typing import Optional

# Initialize a small, free model for chat
class FreeChatModel:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-small"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModelForCausalLM.from_pretrained(self.model_name)
        
        # For similarity comparisons
        self.similarity_model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def generate_response(self, conversation_history: list[dict]) -> str:
        # Format the conversation history for the model
        input_text = ""
        for msg in conversation_history:
            if msg['role'] == 'user':
                input_text += f"User: {msg['content']}\n"
            else:
                input_text += f"Bot: {msg['content']}\n"
        
        # Encode the inputs
        input_ids = self.tokenizer.encode(input_text + "Bot:", return_tensors='pt')
        
        # Generate a response
        chat_output = self.model.generate(
            input_ids,
            max_length=1000,
            pad_token_id=self.tokenizer.eos_token_id,
            no_repeat_ngram_size=3,
            do_sample=True,
            top_k=100,
            top_p=0.7,
            temperature=0.8
        )
        
        # Decode the response
        response = self.tokenizer.decode(chat_output[:, input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        return response
    
    def calculate_similarity(self, text1: str, text2: str) -> float:
        embeddings = self.similarity_model.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
        return float(similarity)

# Global instance
nlp_processor = FreeChatModel()