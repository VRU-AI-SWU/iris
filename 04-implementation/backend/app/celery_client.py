import os
from celery import Celery

_redis = os.getenv("REDIS_URL", "redis://redis:6379/0")
celery_app = Celery(broker=_redis, backend=_redis)


def enqueue_tqf_extraction(programme_id: int, pdf_path: str) -> str:
    result = celery_app.send_task(
        "tasks.tqf_tasks.extract_tqf",
        args=[programme_id, pdf_path],
    )
    return result.id
