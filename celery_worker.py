from celery import Celery
from celery.schedules import crontab
from pymongo import MongoClient
from utils.score_calculator import score_animal_record
from datetime import datetime, timezone

# ✅ FIX 1: Set simple app name
app = Celery('animal_kb_tasks', broker='redis://localhost:6379/0')

# ✅ FIX 2: Define task name explicitly
@app.task(name='animal_kb_tasks.update_scores')
def update_scores():
    """Fetch each document and update the score field using NLP scoring."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["animalDB"]
    collection = db["animals"]

    animals = collection.find()
    for animal in animals:
        score = score_animal_record(animal)
        now = datetime.now(timezone.utc)  # <-- Add UTC timestamp
        result = collection.update_one(
            {"_id": animal["_id"]},
            {"$set": {
                "score": score,
                "score_last_updated": now}}
        )
        """print("[✓] Animal scores updated with timestamps.")"""
        print(f"[Mongo Update] Updated {animal.get('name')} => Score: {score}")
        def update_scores():
            """Fetch each document and update the score field using NLP scoring."""
    client = MongoClient("mongodb://localhost:27017/")
    db = client["animalDB"]
    collection = db["animals"]

    animals = collection.find()
    for animal in animals:
        score = score_animal_record(animal)
        now = datetime.now(timezone.utc).isoformat()  # <-- Add UTC timestamp
        result = collection.update_one(
            {"_id": animal["_id"]},
            {"$set": {
                "score": score,
                "score_last_updated": now}}
        )
        """print("[✓] Animal scores updated with timestamps.")"""
        print(f"[Mongo Update] Updated {animal.get('name')} => Score: {score}")
        print(f"[Mongo Update] Updated {animal.get('score_last_updated')} => Score last updated on : {now}")

# ✅ FIX 3: Beat schedule uses matching task name
app.conf.beat_schedule = {
    'update-animal-scores-every-minute': {
        'task': 'animal_kb_tasks.update_scores',  # Must match the @app.task(name=...)
        'schedule': crontab(minute='*'),
    },
}

# ✅ FIX 4: Timezone
app.conf.timezone = 'UTC'
