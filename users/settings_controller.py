from typing import Type

from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Favorites, Current, Hourly, Daily, Settings
from models.tables import Tables
from users.crud import (
    update_location,
    get_location,
    add_location,
    delete_location,
    update_settings,
)
from utils.setting_schemas import (
    FavoriteLocation,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    UserSettings,
)


async def add_new_location(
    location_info: FavoriteLocation, session: AsyncSession, target: str
) -> Type[IntegrityError] | FavoriteLocation | InterfaceError:
    """
    Function. Handling adding new location to database.
    :param location_info: location information
    :param session: AsyncSession
    :param target: target of the operation (table name)
    :return: location info or an error on adding new location
    """
    if target == Tables.WISHLIST:
        location: Favorites | InterfaceError = await get_location(
            session, location_info=location_info, target=Tables.WISHLIST
        )
        if location:
            return IntegrityError

    location_added: FavoriteLocation | InterfaceError = await add_location(
        location_info, session, target
    )

    return location_added


async def update_user_location(location_info: FavoriteLocation, session: AsyncSession):
    """
    Function. Handling updating user location
    :param location_info: new location information
    :param session: AsyncSession
    :return: new location info or an error on updating new location
    """
    # TODO update user location with class method
    location: Favorites | InterfaceError = await get_location(
        session, location_info=location_info, target=Tables.FAVORITES
    )

    if type(location) is Favorites:
        location.loc_id = location_info.loc_id
        location.loc_name = location_info.loc_name
        location.loc_region = location_info.loc_region
        location.loc_country = location_info.loc_country
        await update_location(location, session)

    return location


async def delete_user_location(
    location_info: FavoriteLocation, session: AsyncSession
) -> FavoriteLocation | InterfaceError:
    """
    Function. Handling deleting user location from wishlist.
    :param location_info: user location information
    :param session:
    :return:
    """
    location: FavoriteLocation | InterfaceError = await delete_location(
        session=session, location_info=location_info
    )

    return location


async def update_user_settings(
    login: EmailStr,
    current: CurrentSettings,
    hourly: HourlySettings,
    daily: DailySettings,
    settings: UserSettings,
    session: AsyncSession,
):
    settings_updated = await update_settings(
        login, current, hourly, daily, settings, session
    )
