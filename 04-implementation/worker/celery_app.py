import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "iris",
    broker=redis_url,
    backend=redis_url,
    include=[
        "tasks.tqf_tasks",
        "tasks.job_tasks",
        "tasks.analysis_tasks",
        "tasks.report_tasks",
    ],
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="Asia/Bangkok",
    task_track_started=True,
)
