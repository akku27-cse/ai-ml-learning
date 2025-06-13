from pymongo import MongoClient

def get_collection():
    client = MongoClient("mongodb://localhost:27017")
    db = client["chatbot"]
    return db["corrections"]