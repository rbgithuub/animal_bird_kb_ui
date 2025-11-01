import os
from celery import Celery

# Simple Celery app definition for Flower
app = Celery('animal_kb_tasks', broker=os.environ.get("CELERY_BROKER_URL", "redis://redis:6379/0"))

# Optional: You can still keep your tasks, Flower will discover them automatically
# Example task (no change needed)
@app.task(name='animal_kb_tasks.update_scores')
def update_scores():
    pass  # Task implementation is ignored by Flower for now
