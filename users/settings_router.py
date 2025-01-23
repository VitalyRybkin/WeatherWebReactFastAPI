from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from models import Favorites
from models.tables import Tables
from users.settings_controller import update_user_location, add_new_location, delete_user_location
from utils import db_engine
from utils.setting_schemas import FavoriteLocation

settings_router = APIRouter(prefix="/settings", tags=["settings"])

@settings_router.post(
    "/add_location/",
    summary="Add user's favorite location or new location to wishlist",
)
async def add_new_user_location(
    target: str,
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    """
    Function. Adds user's favorite location or new location to wishlist.'
    :param target: operation target - 'favorite' or 'wishlist'
    :param location: location info
    :param session: AsyncSession
    :return: added location info or an HTTP error
    """
    match target:
        case "wishlist":
            loc_added: FavoriteLocation | InterfaceError = await add_new_location(
                location_info=location, session=session, target=Tables.WISHLIST
            )
        case "favorite":
            loc_added: FavoriteLocation | InterfaceError = await add_new_location(
                location_info=location, session=session, target=Tables.FAVORITES
            )
        case _:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Target parameter was not found.",
            )

    if type(loc_added) is FavoriteLocation:
        location_info = location.model_dump(mode="json")
        detail: str = (
            "User favorite location added."
            if target == "favorite"
            else "User wishlist location added."
        )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": detail,
                "location_info": location_info,
            },
        )

    if type(loc_added) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User password could not be changed.",
        )

    if type(loc_added) is IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Location could not be added. Location already exists.",
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Something went wrong.",
    )


@settings_router.patch("/change_location/", summary="Change user favorite location")
async def change_user_location(
    location: FavoriteLocation,
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> JSONResponse:
    location_updated: FavoriteLocation | InterfaceError = await update_user_location(
        location_info=location, session=session
    )

    if type(location_updated) is Favorites:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User favorite location changed.",
                "location_info": location.model_dump(mode="json"),
            }
        )
    elif type(location_updated) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User favorite location could not be changed.",
        )
    elif location_updated is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "success": False,
                "detail": "User favorite location could not be found.",
            }
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )

@settings_router.delete("/remove_location/", summary="Remove user location from wishlist")
async def remove_user_location(location: FavoriteLocation, session: AsyncSession = Depends(db_engine.session_dependency),) -> JSONResponse:
    location_deleted: FavoriteLocation | InterfaceError = await delete_user_location(location_info=location, session=session)

    if type(location_deleted) is FavoriteLocation:
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "detail": "User favorite location removed from wishlist.",
                "location_info": location.model_dump(mode="json"),
            }
        )
    elif type(location_deleted) is InterfaceError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database connection error. User favorite location could not be removed.",
        )

    raise HTTPException(
        status_code=status.HTTP_404_BAD_REQUEST,
        detail="Something went wrong.",
    )