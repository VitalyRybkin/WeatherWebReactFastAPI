import os
import sys

from celery import Celery

sys.path.insert(1, os.path.join(sys.path[0], ".."))

from app.utils.settings import settings

celery_app = Celery(
    "run_tasks",
    broker=settings.REDIS_DOCKER_CONN,
    backend=settings.REDIS_DOCKER_CONN,
    include=["celery_tasks.tasks"],
    ignore_result=False,
)
