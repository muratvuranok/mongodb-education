from celery import Celery
import os
from core.config import settings

REDIS_URL = settings.REDIS_URL


celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["tasks.email_tasks"],
)


celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],  # Ignore other content
    result_serializer="json",
)
