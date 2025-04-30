from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import Users, Current, Hourly, Daily, UserSettings
from models.tables import Tables
from users.settings_controller import (
    update_user_location,
    add_new_location,
    delete_user_location,
    update_user_settings,
)
from utils import db_engine, to_json
from schemas.setting_schemas import (
    FavoriteLocation,
    UserSettings,
    CurrentSettings,
    HourlySettings,
    DailySettings,
)

settings_router = APIRouter(prefix="/settings", tags=["settings"])


@settings_router.post(
    "/add_location/",
    summary="Add user's favorite location or new location to wishlist",
)
async def add_new_user_location(
    login: EmailStr,
    target: str,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Adds user's favorite location or new location to wishlist.'
    :param login: user's login'
    :param target: operation target - 'favorite' or 'wishlist'
    :param location: location info
    :param session: AsyncSession
    :return: added location info or an HTTP error
    """
    if target not in ["favorite", "wishlist"]:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Target parameter must be 'favorite' or 'wishlist'",
        )

    user_info: Users | InterfaceError | IntegrityError = await add_new_location(
        user_login=login,
        location_info=location,
        session=session,
        target=Tables.FAVORITES if target == "favorite" else Tables.WISHLIST,
    )

    if user_info is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User location could not be added or changed.",
        )

    if user_info is IntegrityError or type(user_info) is IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Location could not be added. Location already exists.",
        )

    if target == "wishlist" and user_info.wishlist:
        wishlist: list = []
        for loc in user_info.wishlist:
            wishlist.append(to_json(loc))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User location added to wishlist.",
                "wishlist": wishlist,
            },
        )
    if target == "favorite":
        location_info = to_json(user_info.favorites)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User location set as favorite.",
                "location_info": location_info,
            },
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@settings_router.patch("/change_location/", summary="Change user favorite location")
async def change_user_location(
    login: EmailStr,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    user_info: Users = await update_user_location(
        user_login=login, location_info=location, session=session
    )

    if isinstance(user_info, Users):
        user_info = to_json(user_info.favorites)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User favorite location changed.",
                "location_info": user_info,
            },
        )

    if user_info is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User favorite location could not be changed.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@settings_router.delete(
    "/remove_location/", summary="Remove user location from wishlist"
)
async def remove_user_location(
    login: EmailStr,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    user_locations: Users | InterfaceError = await delete_user_location(
        login=login, location_info=location, session=session
    )

    if isinstance(user_locations, Users):
        wishlist: list = []
        for loc in user_locations.wishlist:
            wishlist.append(to_json(loc))

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User location removed from wishlist.",
                "wishlist": wishlist,
            },
        )
    if user_locations is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User favorite location could not be removed.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@settings_router.patch("/update_settings/", summary="Update user weather settings")
async def update_user_weather_settings(
    login: EmailStr | None = None,
    bot_name: str | None = None,
    current: CurrentSettings | None = None,
    hourly: HourlySettings | None = None,
    daily: DailySettings | None = None,
    settings: UserSettings | None = None,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    settings_updated: list[Current | Hourly | Daily | UserSettings] | InterfaceError = (
        await update_user_settings(
            login, bot_name, current, hourly, daily, settings, session
        )
    )

    if settings_updated is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User settings could not be updated.",
        )

    if settings_updated:
        user_settings: dict = {}
        for setting in settings_updated:
            user_settings.update({setting.__tablename__: to_json(setting)})

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User settings updated.",
                "user_settings": user_settings,
            },
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )
