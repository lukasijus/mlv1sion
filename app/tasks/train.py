# app/tasks/train.py
from celery import Celery
from time import sleep
from app.config import settings

celery_app = Celery(
    __name__, broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_RESULT_BACKEND
)


@celery_app.task(name="app.tasks.train.run_training", bind=True, acks_late=True)
def run_training(self, job_id: str):
    # fetch job metadata via DB client (not via direct raw SQL inside task)
    # download dataset from MinIO, train, upload artifact, call API to register artifact
    sleep(10)
    return {"job_id": job_id, "status": "done"}
