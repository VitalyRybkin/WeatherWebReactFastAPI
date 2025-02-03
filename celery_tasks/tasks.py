from json import JSONDecoder

import requests
from requests import Response

from .run_celery import celery_app
from utils.settings import settings


@celery_app.task(name="run_tasks.location_by_name", serializer="json")
def location_by_name(location_name) -> JSONDecoder:
    """
    Function. Get locations by name from API.
    :param location_name: location name string
    :return: List of locations
    """
    try:
        result: Response = requests.get(
            f"https://api.weatherapi.com/v1/search.json?key={settings.api_token}&q={location_name}&aqi=no", timeout=10
        )
        return result.json()
    except requests.exceptions.RequestException as re:
        # logger.warning("Search location error: ", re)
        print(re)

