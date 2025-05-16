__all__ = [
    "settings",
]
from .celery_tasks.tasks import location_by_name, get_forecast
from .utils.settings import settings
