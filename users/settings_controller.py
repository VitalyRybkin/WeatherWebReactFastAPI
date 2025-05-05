from typing import Type

from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Favorites, Users, Wishlist, Settings, Daily, Hourly, Current
from models.tables import Tables
from users.crud import (
    alter_location,
    delete_location,
    update_settings,
    get_user,
)
from utils import to_json
from schemas.setting_schemas import (
    FavoriteLocation,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    UserSettings,
)


async def add_new_location(
    user_login: EmailStr,
    location_info: FavoriteLocation,
    session: AsyncSession,
    target: str,
) -> Type[IntegrityError] | Users:
    """
    Function. Handling adding new location to database.
    :param user_login: user login email.
    :param location_info: location information.
    :param session: AsyncSession.
    :param target: target of the operation (table name).
    :return: location info or an error on adding new location.
    """
    user_info: Users | InterfaceError | None = await get_user(
        session=session, user_login=user_login
    )

    if isinstance(user_info, Users):
        if target == Tables.WISHLIST:
            for loc in user_info.wishlist:
                loc_info = to_json(loc)
                if loc_info["loc_id"] == location_info.loc_id:
                    return IntegrityError
            location_to_add: Wishlist = Wishlist(
                **location_info.model_dump(exclude_unset=True)
            )
        else:
            location_to_add: Favorites = Favorites(
                **location_info.model_dump(exclude_unset=True)
            )

        location_to_add.acc_id = user_info.id
        user_info: Users = await alter_location(
            session=session, new_location=location_to_add, user=user_info
        )

    return user_info


async def update_user_location(
    user_login: EmailStr, location_info: FavoriteLocation, session: AsyncSession
) -> Users:
    """
    Function. Handling updating user location.
    :param user_login: user's login.
    :param location_info: new location information.
    :param session: AsyncSession.
    :return: new location info or an error on updating new location.
    """
    user_info: Users | InterfaceError | None = await get_user(
        session=session, user_login=user_login
    )

    if isinstance(user_info, Users):
        user_info.favorites.update_location(
            **location_info.model_dump(exclude_unset=True)
        )
        user_info: Users = await alter_location(
            session=session, new_location=user_info.favorites, user=user_info
        )

    return user_info


async def delete_user_location(
    login, location_info: FavoriteLocation, session: AsyncSession
) -> Users:
    """
    Function. Handling deleting user location from wishlist.
    :param login: user login.
    :param location_info: user location information
    :param session: AsyncSession.
    :return: deleted location info or an error on deleting location.
    """
    user_info: Users | InterfaceError | None = await get_user(session, login)

    if isinstance(user_info, Users):
        user_info: Users = await delete_location(
            session=session, location_info=location_info, user_info=user_info
        )

    return user_info


async def update_user_settings(
    login: EmailStr,
    bot_name: str,
    current: CurrentSettings,
    hourly: HourlySettings,
    daily: DailySettings,
    settings: UserSettings,
    session: AsyncSession,
) -> list[Current | Hourly | Daily | UserSettings] | InterfaceError | None:
    user_info: Users | InterfaceError | None = await get_user(
        session=session, user_login=login, bot_name=bot_name
    )

    # TODO change to dict update (setattr)
    if isinstance(user_info, Users):
        settings_updated: list[Current | Hourly | Daily | Settings] = (
            await update_settings(
                session=session,
                user_info=user_info,
                current_settings=current,
                hourly_settings=hourly,
                daily_settings=daily,
                user_settings=settings,
            )
        )
        return settings_updated

    return user_info
