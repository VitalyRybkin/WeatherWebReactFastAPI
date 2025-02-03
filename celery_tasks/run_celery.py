from celery import Celery

celery_app = Celery(
    "run_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
    include=["celery_tasks.tasks"],
    ignore_result=False,
)

# if __name__ == "__main__":
#     celery_app.start()
