from typing import Any
import requests
from requests import Response

from .run_celery import celery_app

from .config import API_TOKEN as TOKEN

# import os
# import sys
# sys.path.insert(1, os.path.join(sys.path[0], ".."))
from app.utils.retry import RetryTask, APIRetryHandler


@celery_app.task(name="run_tasks.location_by_name", serializer="json")
@APIRetryHandler(max_retries=5, delay=1)
def location_by_name(location_name) -> Any | None:
    """
    Function. Get locations by name from API.
    :param location_name: Location name string
    :return: List of locations
    """
    result: Response = requests.get(
        f"https://api.weatherapi.com/v1/search.json?key={TOKEN}&q={location_name}&aqi=no"
    )
    return result.json()


@celery_app.task(name="run_tasks.get_forecast", serializer="json", base=RetryTask)
@APIRetryHandler(max_retries=5, delay=1)
def get_forecast(location_id: int, amount_of_days: int) -> Response | None:
    """
    Function. Get locations by id from API.
    :param amount_of_days: days of forecast
    :param location_id: location id integer
    :return: Location object
    """
    forecast_weather_result: Response = requests.get(
        f"https://api.weatherapi.com/v1/forecast.json?key={TOKEN}&q=id:{location_id}&days={amount_of_days if amount_of_days > 1 else 2}&aqi=no&alerts=yes"
    )
    return forecast_weather_result.json()


@celery_app.task(name="run_tasks.get_current_weather", serializer="json")
@APIRetryHandler(max_retries=5, delay=1)
def get_current_weather(location_id) -> Any | None:
    current_weather_result: Response = requests.get(
        f"https://api.weatherapi.com/v1/current.json?key={TOKEN}&q=id:{location_id}&aqi=no"
    )
    return current_weather_result.json()
