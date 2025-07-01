__all__ = [
    "settings",
    "db_engine",
    "location_by_name",
    "get_forecast",
    "redis_client",
]

import redis
from redis import Redis

from .celery_tasks.tasks import location_by_name, get_forecast
from .utils.settings import settings
from .utils.db_engine import db_engine

redis_client: Redis = redis.Redis(host=settings.REDIS_DOCKER_HOST)
