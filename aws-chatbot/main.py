from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict, List
import boto3
import json

app = FastAPI()

# In-memory user chat memory
chat_memory: Dict[str, List[Dict[str, str]]] = {}

# Claude 3 (Sonnet) config
bedrock = boto3.client("bedrock-runtime", region_name="ap-south-1")

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"

class ChatRequest(BaseModel):
    user_id: str
    message: str

def call_claude_with_memory(prompt: str):
    response = bedrock.invoke_model(
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500,
            "temperature": 0.7,
            "top_k": 250,
            "top_p": 0.9
        }),
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json"
    )
    result = json.loads(response["body"].read())
    return result["content"][0]["text"]

@app.post("/chat")
async def chat_with_bot(request: ChatRequest):
    user_id = request.user_id
    message = request.message

    # Initialize memory for new user
    if user_id not in chat_memory:
        chat_memory[user_id] = []

    # Append user message to memory
    chat_memory[user_id].append({"sender": "user", "text": message})

    # Limit memory to last 10 messages
    history = chat_memory[user_id][-10:]

    # Format prompt with history
    history_text = "\n".join([f"{m['sender']}: {m['text']}" for m in history])
    prompt = f"""The following is a conversation between a user and an AI assistant.
Respond helpfully based on the context.
{history_text}
bot:"""

    # Call Claude
    reply = call_claude_with_memory(prompt)

    # Add bot reply to memory
    chat_memory[user_id].append({"sender": "bot", "text": reply})

    return {"response": reply}
