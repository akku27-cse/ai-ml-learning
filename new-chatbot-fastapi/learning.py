from datetime import datetime
from typing import Optional
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
import string
import nltk
from database import get_sync_db
from models import LearnedResponse
import nlp_processor

# Download NLTK data (run once)
nltk.download('punkt')
nltk.download('stopwords')

ps = PorterStemmer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text: str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(text)
    processed = [ps.stem(word) for word in tokens if word not in stop_words]
    return ' '.join(processed)

async def find_best_learned_response(db, user_input: str, threshold: float = 0.6) -> Optional[str]:
    best_match = None
    highest_score = 0
    
    learned_responses = await db["learned_responses"].find().to_list(1000)
    
    for response in learned_responses:
        score = nlp_processor.calculate_similarity(user_input, response["input_pattern"])
        if score > highest_score and score >= threshold:
            highest_score = score
            best_match = response
    
    if best_match:
        # Update confidence and last used
        await db["learned_responses"].update_one(
            {"_id": best_match["_id"]},
            {"$inc": {"confidence": 1}, "$set": {"last_used": datetime.utcnow()}}
        )
        return best_match["response"]
    
    return None

async def learn_from_conversation(db, user_input: str, bot_response: str):
    processed_input = preprocess_text(user_input)
    
    # Check for similar existing responses
    existing = await db["learned_responses"].find_one({
        "input_pattern": {"$regex": processed_input[:20], "$options": "i"}
    })
    
    if existing:
        # Update existing response
        await db["learned_responses"].update_one(
            {"_id": existing["_id"]},
            {"$inc": {"confidence": 1}, "$set": {"last_used": datetime.utcnow()}}
        )
    else:
        # Create new learned response
        new_response = LearnedResponse(
            input_pattern=processed_input,
            response=bot_response
        )
        await db["learned_responses"].insert_one(new_response.dict())