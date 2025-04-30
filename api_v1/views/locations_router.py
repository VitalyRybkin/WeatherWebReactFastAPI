from typing import Any, List

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from api_v1.views.location_controller import (
    get_locations,
    get_location_weather,
)
from schemas.setting_schemas import (
    UserSettings,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    LocationPublic,
)

location_router = APIRouter(prefix="/api_v1")


@location_router.get(
    "/{location_name}/",
    summary="Get location / list of locations by name.",
    response_model=List[LocationPublic],
)
def get_location_by_name(location_name: str) -> list[LocationPublic] | None:
    """
    Function to get location by name.
    :param location_name: location name string.
    :return: List of locations found.
    """
    locations_found: List[LocationPublic] = get_locations(location_name)

    return locations_found


@location_router.post("/{location_id}/", summary="Get location by ID.")
def get_forecast_by_id(
    location_id: int,
    settings: UserSettings,
    current: CurrentSettings,
    hourly: HourlySettings,
    daily: DailySettings,
) -> JSONResponse:

    forecast_info = get_location_weather(
        location_id,
        current,
        daily,
        hourly,
        settings.units,
        settings.daily,
        settings.hourly,
    )

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "detail": "Location found",
            "location": forecast_info["location"],
            "current": forecast_info["current"] if settings.current else None,
            "forecast": forecast_info["forecast"],
            "alerts": forecast_info["alerts"],
        },
    )
