from typing import Any

from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from api_v1.views.location_controller import get_location
from utils import FavoriteLocation

location_router = APIRouter(prefix="/api_v1")


@location_router.get(
    "/{location_name}",
    summary="Get location by name&",
)
def get_location_by_name(location_name: str) -> JSONResponse:
    """
    Function to get location by name.
    :param location_name: location name string.
    :return: List of locations found.
    """
    locations: list[dict[str, Any]] | None = get_location(location_name)
    if locations:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "Locations found",
                "locations": locations,
            },
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"success": False, "detail": "Location not found."},
        )
