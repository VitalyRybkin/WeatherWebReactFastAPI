"""
Module. Settings operations API routes.
"""

from typing import List, Union

from fastapi import APIRouter, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.models import Users, Current, Hourly, Daily, Settings
from app.models.tables import Tables
from app.schemas.error_response_schemas import (
    DBErrorMessage,
    BadRequestMessage,
    ConflictErrorMessage,
    NotFoundErrorMessage,
    UnprocessableErrorMessage,
)
from app.schemas.setting_schemas import (
    FavoriteLocation,
    UserSettings,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    SettingsPublic,
)
from app.schemas.user_schemas import LocationPublic
from app.users.settings_controller import (
    update_user_location,
    add_new_location,
    delete_user_location,
    update_user_settings,
)
from app.utils import db_engine, to_json
from app.utils.exeption_handler import (
    DatabaseInterfaceError,
    DatabaseIntegrityError,
    NotFoundError,
    UnprocessableEntityError,
)

settings_router = APIRouter(prefix="/settings", tags=["settings"])


@settings_router.post(
    "/add_location/",
    summary="Add user's favorite location or new location to wishlist",
    response_model=Union[List[LocationPublic], LocationPublic],
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
        status.HTTP_422_UNPROCESSABLE_ENTITY: {
            "model": UnprocessableErrorMessage,
            "description": "Wrong target request.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ConflictErrorMessage,
            "description": "Location exists.",
        },
    },
)
async def add_new_user_location(
    login: EmailStr,
    target: str,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse | list[LocationPublic] | LocationPublic:
    """
    Function. Adds user's favorite location or new location to wishlist.'
    :param login: User's login
    :param target: operation target - 'favorite' or 'wishlist'
    :param location: location info
    :param session: AsyncSession
    :return: added location info or an HTTP error
    """
    if target not in ["favorite", "wishlist"]:
        raise UnprocessableEntityError(
            "Target parameter must be 'favorite' or 'wishlist'"
        )

    user_info: Users | InterfaceError | IntegrityError = await add_new_location(
        user_login=login,
        location_info=location,
        session=session,
        target=Tables.FAVORITES if target == "favorite" else Tables.WISHLIST,
    )

    if user_info is InterfaceError:
        raise DatabaseInterfaceError(
            message="User location could not be added or changed."
        )

    if isinstance(user_info, IntegrityError):
        raise DatabaseIntegrityError(
            (
                "Location already exists."
                if target == "wishlist"
                else "User location already set."
            ),
            {"X-Error-Code": "LOCATION_EXISTS"},
        )

    if target == "wishlist" and user_info.wishlist:
        return [LocationPublic(**to_json(loc)) for loc in user_info.wishlist]

    location_info = LocationPublic(**to_json(user_info.favorites))
    return location_info


@settings_router.patch(
    "/change_location/",
    summary="Change user favorite location",
    response_model=LocationPublic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundErrorMessage,
            "description": "User not found.",
        },
    },
)
async def change_user_location(
    login: EmailStr,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> LocationPublic | JSONResponse:
    """
    Function. Changes favorite user's location.
    :param login: user's login
    :param location: location to change
    :param session: a Database session
    :return: set location
    """
    user_info: Users = await update_user_location(
        user_login=login, location_info=location, session=session
    )

    if user_info is None:
        raise NotFoundError("User not found.", {"X-Error-Code": "USER_NOT_FOUND"})

    if user_info is InterfaceError:
        raise DatabaseInterfaceError(
            message="User favorite location could not be changed."
        )

    return LocationPublic(**to_json(user_info.favorites))


@settings_router.delete(
    "/remove_location/",
    summary="Remove user location from wishlist",
    response_model=List[LocationPublic],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundErrorMessage,
            "description": "User not found.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
    },
)
async def remove_user_location(
    login: EmailStr,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> list[LocationPublic] | JSONResponse:
    """
    Function to remove user location from wishlist.
    :param login: User login
    :param location: location to remove
    :param session: DB session
    :return: user wishlist locations
    """
    user_locations: Users | InterfaceError = await delete_user_location(
        login=login, location_info=location, session=session
    )

    if user_locations is None:
        raise NotFoundError("User not found.", {"X-Error-Code": "USER_NOT_FOUND"})

    if user_locations is InterfaceError:
        raise DatabaseInterfaceError(message="User location cannot be removed.")

    return [LocationPublic(**to_json(location)) for location in user_locations.wishlist]


@settings_router.patch(
    "/update_settings/",
    summary="Update user weather settings",
    response_model=SettingsPublic,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": NotFoundErrorMessage,
            "description": "User not found.",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "model": DBErrorMessage,
            "description": "Database connection error.",
        },
    },
)
async def update_user_weather_settings(
    login: EmailStr | None = None,
    bot_name: str | None = None,
    current: CurrentSettings | None = None,
    hourly: HourlySettings | None = None,
    daily: DailySettings | None = None,
    settings: UserSettings | None = None,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse | SettingsPublic:
    """
    Function to update user weather settings
    :param login: user login
    :param bot_name: user bot name
    :param current: user current weather settings
    :param hourly: user hourly weather settings
    :param daily: user daily weather settings
    :param settings: user settings
    :param session: Database session
    :return: user weather settings
    """
    settings_updated: list[Current | Hourly | Daily | Settings] | InterfaceError = (
        await update_user_settings(
            login, bot_name, current, hourly, daily, settings, session
        )
    )

    if settings_updated is InterfaceError:
        raise DatabaseInterfaceError(
            message="Database connection error. User settings cannot be updated."
        )

    if settings_updated is None:
        raise NotFoundError("User not found.")

    user_settings: dict = {}
    for setting in settings_updated:
        user_settings.update({setting.__tablename__: to_json(setting)})

    user_settings_response: SettingsPublic = SettingsPublic(**user_settings)

    return user_settings_response
