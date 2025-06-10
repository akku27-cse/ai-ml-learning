# chatbot_api.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load GPT-2 model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model.eval()

# If GPU is available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# System prompt
SYSTEM_PROMPT = """
You are PPHub Assistant, a friendly and knowledgeable AI assistant for the PPHub pet care mobile application. 
Your role is to help users with all pet-related questions including:

- Pet care advice (dogs, cats, birds, etc.)
- Understanding PPHub services (boarding, grooming, vet services)
- General pet health questions
- Pet training tips
- Recommendations for local pet services

Always be polite, empathetic, and professional. If you don't know an answer, say so and suggest consulting a veterinarian for health-related questions.

Keep responses concise and to the point (2-3 sentences max when possible).
"""

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: str

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    try:
        # Combine messages into a single prompt
        user_prompt = SYSTEM_PROMPT.strip() + "\n\n"
        for msg in request.messages:
            prefix = "User:" if msg.role == "user" else "Assistant:"
            user_prompt += f"{prefix} {msg.content}\n"
        user_prompt += "Assistant:"

        # Tokenize and generate
        input_ids = tokenizer.encode(user_prompt, return_tensors="pt").to(device)
        output_ids = model.generate(
            input_ids,
            max_length=input_ids.shape[1] + 100,
            temperature=0.7,
            top_p=0.9,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id,
        )

        # Decode output
        output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
        response_text = output_text[len(user_prompt):].strip().split("\n")[0]

        return {
            "response": response_text,
            "message_id": None  # GPT-2 doesn't return message IDs
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
