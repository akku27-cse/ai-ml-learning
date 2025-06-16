from pymongo import MongoClient
import numpy as np
from datetime import datetime
from .bedrock_service import get_embedding, get_llm_response
from .config_loader import config

client = MongoClient(config["DB_CONNECTION_STRING"])
db = client["chatbot"]
collection = db["chat_logs"]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_similar_chats(query_embedding, top_n=3):
    all_chats = list(collection.find())
    scored = []
    for chat in all_chats:
        sim = cosine_similarity(query_embedding, chat['embedding'])
        scored.append((sim, chat))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [chat for _, chat in scored[:top_n]]

def build_prompt(user_question, related_chats):
    memory = ""
    for chat in related_chats:
        memory += f"\nQ: {chat['question']}\nA: {chat['answer']}"
    return f"""You are a helpful chatbot. Use the following memory and answer the new question.

Memory:{memory}

New Question: {user_question}
Answer:"""

def save_chat(user_id, question, answer, embedding):
    collection.insert_one({
        "user_id": user_id,
        "question": question,
        "answer": answer,
        "embedding": embedding,
        "timestamp": datetime.now()
    })

def process_chat(user_id, message):
    embed = get_embedding(message)
    similar_chats = find_similar_chats(embed)
    prompt = build_prompt(message, similar_chats)
    answer = get_llm_response(prompt)
    save_chat(user_id, message, answer, embed)
    return answer
