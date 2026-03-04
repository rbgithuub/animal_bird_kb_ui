import os

from celery import Celery
from celery.schedules import crontab

from app import create_app


def make_celery() -> Celery:
    flask_app = create_app()

    celery = Celery(
        flask_app.import_name,
        broker=flask_app.config["CELERY_BROKER_URL"],
        backend=flask_app.config["CELERY_RESULT_BACKEND"],
    )

    celery.conf.update(
        broker_url=flask_app.config["CELERY_BROKER_URL"],
        result_backend=flask_app.config["CELERY_RESULT_BACKEND"],
        timezone=os.getenv("TZ", "UTC"),
        beat_schedule={
            "update-animal-scores-every-minute": {
                "task": "app.tasks.animal_tasks.update_scores",
                "schedule": crontab(minute="*"),
            }
        },
    )

    class FlaskContextTask(celery.Task):
        abstract = True

        def __call__(self, *args, **kwargs):
            with flask_app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = FlaskContextTask
    celery.autodiscover_tasks(["app.tasks"])

    return celery


celery_app = make_celery()
