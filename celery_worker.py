import os
from celery import Celery
from celery.schedules import crontab
from pymongo import MongoClient
from utils.score_calculator import score_animal_record
from datetime import datetime, timezone


# -----------------------------
# Celery Configuration
# -----------------------------
app = Celery(
    'animal_kb_tasks',
    broker=os.environ.get("CELERY_BROKER_URL")
)

app.conf.timezone = 'UTC'

app.conf.beat_schedule = {
    'update-animal-scores-every-minute': {
        'task': 'animal_kb_tasks.update_scores',
        'schedule': crontab(minute='*'),
    },
}


# -----------------------------
# Mongo Configuration (ENV BASED)
# -----------------------------
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")

client = MongoClient(mongo_uri)
db = client[mongo_db_name]
collection = db["animals"]


# -----------------------------
# Celery Task
# -----------------------------
@app.task(name='animal_kb_tasks.update_scores')
def update_scores():
    """Fetch each document and update the score field using NLP scoring."""

    animals = collection.find()

    for animal in animals:
        score = score_animal_record(animal)
        now = datetime.now(timezone.utc)

        collection.update_one(
            {"_id": animal["_id"]},
            {
                "$set": {
                    "score": score,
                    "score_last_updated": now
                }
            }
        )

        print(f"[Mongo Update] {animal.get('name')} => Score: {score}")
