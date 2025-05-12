from celery import Celery

celery_app = Celery(
    "run_tasks",
    broker="redis://redis:6379",
    # broker="redis://localhost:6379",
    # backend="redis://redis:6379",
    backend="redis://localhost:6379",
    include=["celery_tasks.tasks"],
    ignore_result=False,
)
