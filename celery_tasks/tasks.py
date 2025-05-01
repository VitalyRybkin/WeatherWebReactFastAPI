from json import JSONDecoder
from typing import Any

import requests
from requests import Response

from .run_celery import celery_app
from utils.settings import settings


@celery_app.task(name="run_tasks.location_by_name", serializer="json")
def location_by_name(location_name) -> Any | None:
    """
    Function. Get locations by name from API.
    :param location_name: location name string
    :return: List of locations
    """
    try:
        result: Response = requests.get(
            f"https://api.weatherapi.com/v1/search.json?key={settings.api_token}&q={location_name}&aqi=no"
        )
        return result.json()
    except requests.exceptions.RequestException as re:
        # logger.warning("Search location error: ", re)
        # TODO exception logger
        print(re)


@celery_app.task(name="run_tasks.get_forecast", serializer="json")
def get_forecast(location_id: int, amount_of_days: int) -> Response | None:
    """
    Function. Get locations by id from API.
    :param amount_of_days: days of forecast
    :param location_id: location id integer
    :return: Location object
    """
    try:
        forecast_weather_result: Response = requests.get(
            f"https://api.weatherapi.com/v1/forecast.json?key={settings.api_token}&q=id:{location_id}&days={amount_of_days if amount_of_days > 1 else 2}&aqi=no&alerts=yes"
        )
        return forecast_weather_result.json()
    except requests.exceptions.RequestException as re:
        # logger.warning("Search location error: ", re)
        print(re)


@celery_app.task(name="run_tasks.get_current_weather", serializer="json")
def get_current_weather(location_id) -> Any | None:
    try:
        current_weather_result: Response = requests.get(
            f"https://api.weatherapi.com/v1/current.json?key={settings.api_token}&q=id:{location_id}&aqi=no"
        )
        return current_weather_result.json()
    except requests.exceptions.RequestException as re:
        # logger.warning("Search location error: ", re)
        print(re)
