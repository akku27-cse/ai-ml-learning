from app.utils.mongo import get_collection
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

async def get_response(user_id: str, message: str) -> str:
    col = get_collection()
    query_vec = model.encode([message])[0]

    docs = list(col.find())
    if docs:
        doc_vectors = [doc['embedding'] for doc in docs]
        sims = cosine_similarity([query_vec], doc_vectors)[0]
        max_index = np.argmax(sims)
        if sims[max_index] > 0.85:
            return docs[max_index]['corrected_answer']

    # Fallback response (mocked for now)
    return "Thanks for your question. Our assistant is still learning!"

def save_correction(question: str, corrected_answer: str):
    col = get_collection()
    embedding = model.encode([question])[0].tolist()
    col.insert_one({
        "question": question,
        "corrected_answer": corrected_answer,
        "embedding": embedding
    })