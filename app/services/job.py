# app/services/job.py
from app.db import repositories
from app.utils.idempotency import check_idempotency
from app.tasks import celery_app


def submit_training_job(
    db, tenant_id: str, dataset_id: str, idempotency_key: str, user_id: str
):
    if not check_idempotency(db, idempotency_key):
        return {"status": "duplicate"}

    job = repositories.JobRepo.create_pending(
        db, tenant_id, dataset_id, created_by=user_id
    )
    # publish to broker
    celery_app.send_task("app.tasks.train.run_training", args=[job.id], kwargs={})
    return {"job_id": job.id, "status": "queued"}
