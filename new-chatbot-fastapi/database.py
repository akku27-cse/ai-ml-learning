from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "chatbot_db"

# Async client for FastAPI
async def get_async_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    try:
        yield db
    finally:
        client.close()

# Sync client for learning and other sync operations
def get_sync_db():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    try:
        return db
    except Exception as e:
        client.close()
        raise e