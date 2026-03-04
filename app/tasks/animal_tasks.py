from datetime import datetime, timezone

from app.celery_app import celery_app
from app.extensions import mongo_db
from utils.score_calculator import score_animal_record


@celery_app.task(name="app.tasks.animal_tasks.update_scores")
def update_scores():
    if mongo_db is None:
        return "MongoDB connection is not initialized"

    collection = mongo_db["animals"]

    for animal in collection.find():
        score = score_animal_record(animal)
        now = datetime.now(timezone.utc)

        collection.update_one(
            {"_id": animal["_id"]},
            {"$set": {"score": score, "score_last_updated": now}},
        )

    return "Scores updated"
