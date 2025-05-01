from datetime import datetime
from typing import Any, List, Dict

from celery_tasks.tasks import location_by_name, get_forecast
from schemas.setting_schemas import (
    LocationPublic,
    CurrentSettings,
    DailySettings,
    HourlySettings, UserSettings,
)
from schemas.weather_schemas import (
    HourlyWeatherBritish,
    HourlyWeatherMetric,
    exclude_fields,
    DailyWeatherBritish,
    DailyWeatherMetric,
    DailyWeather,
    CurrentWeatherMetric,
    CurrentWeatherBritish,
)


def get_locations(location_name: str) -> List[LocationPublic]:
    """
    Function. Get list of locations by name based on user request.
    :param location_name: Name of location.
    :return: List of locations found.
    """
    result = location_by_name.apply_async(args=[location_name])

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
    :param hourly_settings: hourly user settings
    :param daily_settings: daily user settings
    :param location_id: location id
    :param current_settings: current weather user settings
    :return: current weather data
    """
    # TODO retry logic

    weather_forecast = get_forecast.apply_async(args=[location_id, user_settings.daily])
    location_weather: Dict[str, Any] = weather_forecast.get()

    # Current weather filtering based on user settings.

    current_weather_filter: Dict[str, Any] = (
        CurrentWeatherMetric(**location_weather["current"]).model_dump(
            exclude=exclude_fields(current=current_settings)
        )
        if user_settings.units == "C"
        else CurrentWeatherBritish(**location_weather["current"]).model_dump(
            exclude=exclude_fields(current=current_settings)
        )
    )

    location_weather["current"] = current_weather_filter

    forecast_day: list[DailyWeather] = []
    forecast_hour_list: list = []

    local_time: datetime = datetime.strptime(
        location_weather["location"]["localtime"], "%Y-%m-%d %H:%M"
    )

    # Daily weather filtering based on user settings.

    for day in range(user_settings.daily):
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
            day=daily_weather_filter,
            astro=location_weather["forecast"]["forecastday"][day]["astro"],
        )
        forecast_day.append(
            day_weather.model_dump(exclude=exclude_fields(daily=daily_settings))
        )
        forecast_hour_list.extend(
            location_weather["forecast"]["forecastday"][day]["hour"]
        )

    location_weather["forecast"]["forecastday"] = forecast_day

    # Hourly weather filtering based on user settings.

    location_weather["forecast"]["forecasthour"] = []

    for hour in forecast_hour_list[local_time.hour : local_time.hour + user_settings.daily]:
        hour_weather_filter: Dict[str, Any] = (
            HourlyWeatherMetric(**hour).model_dump(
                exclude=exclude_fields(hourly=hourly_settings)
            )
            if user_settings.units == "C"
            else HourlyWeatherBritish(**hour).model_dump(
                exclude=exclude_fields(hourly=hourly_settings)
            )
        )

        location_weather["forecast"]["forecasthour"].append(hour_weather_filter)

    return location_weather
