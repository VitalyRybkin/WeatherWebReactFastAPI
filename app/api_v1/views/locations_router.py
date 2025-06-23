"""
Module. Location API routes.
"""

from typing import Any, List

from fastapi import APIRouter, Depends

from app.schemas.setting_schemas import (
    UserSettings,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    LocationPublic,
)
from app.schemas.weather_schemas import ForecastPublic
from .location_controller import get_locations, get_location_weather
from ...utils.auth import user_auth

location_router = APIRouter(prefix="/api_v1")


@location_router.get(
    "/name/{location_name}/",
    summary="Get location / list of locations by name.",
    response_model=List[LocationPublic],
)
def get_location_by_name(location_name: str) -> list[LocationPublic] | None:
    """
    Function to get location by name.
    :param location_name: Location name string.
    :return: List of locations found.
    """
    locations_found: List[LocationPublic] = get_locations(location_name)

    return locations_found


@location_router.post(
    "/id/{location_id}/",
    summary="Get location by ID.",
    dependencies=[Depends(user_auth)],
    response_model=ForecastPublic,
    response_model_exclude_none=True,
)
def get_forecast_by_id(
    location_id: int,
    settings: UserSettings | None = None,
    current: CurrentSettings | None = None,
    hourly: HourlySettings | None = None,
    daily: DailySettings | None = None,
) -> dict[str, Any] | None:
    """
    Function to get forecast by ID.
    :param location_id: location ID.
    :param settings: user settings.
    :param current: current weather user settings.
    :param hourly: hourly weather user settings.
    :param daily: daily weather user settings.
    :return: forecast info
    """

    forecast_info = get_location_weather(
        location_id,
        current,
        daily,
        hourly,
        settings,
    )

    return forecast_info
