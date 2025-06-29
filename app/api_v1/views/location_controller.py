"""
Module. Get data from DB and API and prepare it to be passed to the router.
"""

import json
from datetime import datetime
from typing import Any, List, Dict

import redis
from redis import Redis

from app.celery_tasks.tasks import location_by_name, get_forecast
from app.schemas.setting_schemas import (
    LocationPublic,
    CurrentSettings,
    DailySettings,
    HourlySettings,
    UserSettings,
)
from app.schemas.weather_schemas import (
    HourlyWeatherBritish,
    HourlyWeatherMetric,
    exclude_fields,
    DailyWeatherBritish,
    DailyWeatherMetric,
    DailyWeather,
    CurrentWeatherMetric,
    CurrentWeatherBritish,
    Location,
    CurrentWeatherPublic,
    DailyWeatherPublic,
    Astro,
    DailyForecastPublic,
    HourlyForecastPublic,
    Conditions,
)
from app.utils import settings


def get_locations(location_name: str) -> List[LocationPublic]:
    """
    Function. Get a list of locations by name based on user request.
    :param location_name: Name of location.
    :return: List of locations found.
    """
    result: Any = location_by_name.apply_async(args=[location_name])

    return [LocationPublic(**location) for location in result.get()]


def get_location_weather(
    location_id: int,
    current_settings: CurrentSettings,
    daily_settings: DailySettings,
    hourly_settings: HourlySettings,
    user_settings: UserSettings,
) -> Dict[str, Any] | None:
    """
    Function. Fetch weather data for a given location bsed on user settings.
    :param user_settings: User settings.
    :param hourly_settings: Hourly user settings
    :param daily_settings: daily user settings
    :param location_id: location id
    :param current_settings: current weather user settings
    :return: current weather data
    """
    current_datetime = datetime.now()
    time_to: int = 30 if current_datetime.minute < 30 else 60

    expiration_time: int = (time_to - current_datetime.minute) * 60

    redis_client: Redis = redis.Redis(host=settings.REDIS_LOCALHOST)

    if redis_client.get(str(location_id)):
        location_weather: Dict[str, Any] = json.loads(
            redis_client.get(str(location_id))
        )
    else:
        weather_forecast = get_forecast.apply_async(
            args=[location_id, user_settings.daily]
        )
        location_weather: Dict[str, Any] = weather_forecast.get()
        redis_client.set(str(location_id), json.dumps(location_weather))
        redis_client.expire(str(location_id), expiration_time)

    location_weather_response: dict[str, Location | CurrentWeatherPublic | Dict] = {}
    location_weather_response.update(location=Location(**location_weather["location"]))

    # Current weather filtering based on user settings.

    location_weather["current"]["condition"] = Conditions(
        **location_weather["current"]["condition"]
    )
    current_weather_filter: Dict[str, Any] = (
        CurrentWeatherMetric(**location_weather["current"]).model_dump(
            exclude=exclude_fields(current=current_settings)
        )
        if user_settings.units == "C"
        else CurrentWeatherBritish(**location_weather["current"]).model_dump(
            exclude=exclude_fields(current=current_settings)
        )
    )

    location_weather_response.update(
        current=CurrentWeatherPublic.model_validate(current_weather_filter)
    )

    # Daily weather filtering based on user settings.

    sample_forecast_day = []
    forecast_hour_list: list = []
    local_time: datetime = datetime.strptime(
        location_weather["location"]["localtime"], "%Y-%m-%d %H:%M"
    )

    for day in range(user_settings.daily):
        location_weather["forecast"]["forecastday"][day]["day"]["condition"] = (
            Conditions(
                **location_weather["forecast"]["forecastday"][day]["day"]["condition"]
            )
        )

        daily_weather_filter: Dict[str, Any] = (
            DailyWeatherMetric(
                **location_weather["forecast"]["forecastday"][day]["day"]
            ).model_dump(exclude=exclude_fields(daily=daily_settings))
            if user_settings.units == "C"
            else DailyWeatherBritish(
                **location_weather["forecast"]["forecastday"][day]["day"]
            ).model_dump(exclude=exclude_fields(daily=daily_settings))
        )

        day_weather: DailyWeather = DailyWeather(
            date=location_weather["forecast"]["forecastday"][day]["date"],
            day=DailyWeatherPublic.model_validate(daily_weather_filter),
            astro=Astro.model_validate(
                location_weather["forecast"]["forecastday"][day]["astro"]
            ),
        )

        sample_forecast_day.append(
            DailyForecastPublic.model_validate(
                day_weather.model_dump(exclude=exclude_fields(daily=daily_settings))
            )
        )

        forecast_hour_list.extend(
            location_weather["forecast"]["forecastday"][day]["hour"]
        )

    location_weather_response.update(forecast={})
    location_weather_response["forecast"].update(forecastday=sample_forecast_day)

    # Hourly weather filtering based on user settings.

    location_weather_response["forecast"].update(forecasthour=[])

    for hour in forecast_hour_list[
        local_time.hour : local_time.hour + user_settings.daily
    ]:
        hour["condition"] = Conditions(**hour["condition"])
        hour_weather_filter: Dict[str, Any] = (
            HourlyWeatherMetric(**hour).model_dump(
                exclude=exclude_fields(hourly=hourly_settings)
            )
            if user_settings.units == "C"
            else HourlyWeatherBritish(**hour).model_dump(
                exclude=exclude_fields(hourly=hourly_settings)
            )
        )

        location_weather_response["forecast"]["forecasthour"].append(
            HourlyForecastPublic.model_validate(hour_weather_filter)
        )

    location_weather_response.update(alerts=location_weather["alerts"])

    return location_weather_response
