from transformers import GPT2LMHeadModel, GPT2Tokenizer
from app.config import settings
import torch

class GPT2Generator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer = GPT2Tokenizer.from_pretrained(settings.model_name)
        self.model = GPT2LMHeadModel.from_pretrained(settings.model_name).to(self.device)
        
        # Set pad token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def generate_text(self, prompt: str):
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
        
        outputs = self.model.generate(
            inputs,
            max_length=settings.max_length,
            num_return_sequences=settings.num_return_sequences,
            no_repeat_ngram_size=2,
            do_sample=True,
            top_k=50,
            top_p=0.95,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        generated_texts = []
        for i, output in enumerate(outputs):
            text = self.tokenizer.decode(output, skip_special_tokens=True)
            generated_texts.append(text)
        
        return generated_texts[0] if len(generated_texts) == 1 else generated_texts

# Singleton instance
gpt2_generator = GPT2Generator()