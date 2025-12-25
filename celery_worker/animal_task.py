from pymongo import MongoClient
from datetime import datetime

client = MongoClient("mongodb://mongodb:27017")
db = client.animal_kb

def save_animal_record(data):
    data["created_by"] = "nlp_bot"
    data["created_at"] = datetime.utcnow()
    db.animals.insert_one(data)
