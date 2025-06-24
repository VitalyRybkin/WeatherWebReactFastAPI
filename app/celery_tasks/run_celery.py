from celery import Celery

# from app.utils.settings import settings

celery_app = Celery(
    "run_tasks",
    broker="redis://localhost:6379",
    # broker=settings.REDIS_DOCKER_CONN,
    # backend=settings.REDIS_DOCKER_CONN,
    backend="redis://localhost:6379",
    include=["celery_tasks.tasks"],
    ignore_result=False,
)
