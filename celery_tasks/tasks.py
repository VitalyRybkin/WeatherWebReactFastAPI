import json

import requests

from .run_celery import celery_app
from utils.settings import settings


@celery_app.task(name="run_tasks.location_by_name", serializer="json")
def location_by_name(location_name):
    try:
        result = requests.get(
            f"https://api.weatherapi.com/v1/search.json?key={settings.api_token}&q={location_name}&aqi=no"
        )

        return result.json()
    except requests.exceptions.RequestException as re:
        # logger.warning("Search location error: ", re)
        print(re)
