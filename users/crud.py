from typing import List

from pydantic import EmailStr
from sqlalchemy import insert, select, Select, Result, delete
from sqlalchemy.exc import InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users, Current, Daily, Hourly, UserSettings, Favorites, Wishlist
from utils.setting_schemas import (
    FavoriteLocation,
    CurrentSettings,
    HourlySettings,
    DailySettings,
    UserSettings,
)
from utils.utils import handling_integrity_error, handling_interface_error


@handling_integrity_error
@handling_interface_error
async def create_new_user(session, user) -> Users:
    """
    Function. Adds a new user to the database.
    :param session: SQLAlchemy session.
    :param user: user to create.
    :return: user if successful or an error.
    """

    user = Users(**user.model_dump())
    session.add(user)
    await session.commit()

    await session.execute(insert(Current).values(acc_id=user.id))
    await session.execute(insert(Daily).values(acc_id=user.id))
    await session.execute(insert(Hourly).values(acc_id=user.id))
    await session.execute(insert(UserSettings).values(acc_id=user.id))
    await session.commit()
    await session.refresh(user)

    return user


@handling_interface_error
async def get_user(
    session, user_login: EmailStr = None, bot_name: str = None
) -> Users | None:
    """
    Function. Fetches a user from the database by login or bot name.
    :param session: SQLAlchemy session.
    :param user_login: user login
    :param bot_name: bot name
    :return: user info if successful or an error.
    """
    if user_login:
        get_user_info: Select = select(Users).filter(Users.login == user_login)
    else:
        get_user_info: Select = select(Users).filter(Users.bot_name == bot_name)

    result: Result = await session.execute(get_user_info)
    user_info: Users = result.scalar()

    return user_info if user_info else None


@handling_interface_error
async def link_user_accounts(
    session: AsyncSession, web_user: Users, bot_user: Users
) -> Users | InterfaceError:
    """
    Function. Updates user accounts - adding bot account to web account. Deletes user's bot-only account.
    :param bot_user: bot user info to delete
    :param web_user: web user info to update.
    :param session: SQLAlchemy session.
    :return: user info if successful or an error.
    """
    session.add(web_user)
    await session.execute(delete(Users).where(Users.id == bot_user.id))
    await session.commit()

    return web_user


@handling_interface_error
async def change_user_password(
    session: AsyncSession, user_with_new_password: Users
) -> Users | InterfaceError:
    """
    Function. Deletes a user from the database by account ID.
    :param user_with_new_password:
    :param session: SQLAlchemy session.
    :return: None
    """

    session.add(user_with_new_password)
    await session.commit()
    await session.refresh(user_with_new_password)

    return user_with_new_password


@handling_interface_error
@handling_integrity_error
async def alter_location(
    session: AsyncSession, new_location: Favorites | Wishlist, user: Users
) -> Users:
    """
    Function. Adds a new location to the database or changes existing.
    :param user: user information.
    :param new_location: location info
    :param session: AsyncSession.
    :return: location info or an error.
    """
    session.add(new_location)
    await session.commit()
    await session.refresh(user)

    return user


@handling_interface_error
async def delete_location(
    session: AsyncSession, location_info: FavoriteLocation, user_info
) -> Users:
    """
    Function. Deletes user's favorite location from wishlist
    :param user_info: user info.
    :param session: AsyncSession.
    :param location_info: location to delete.
    :return: location info or an error.
    """
    await session.execute(
        delete(Wishlist)
        .where(Wishlist.acc_id == user_info.id)
        .where(Wishlist.loc_id == location_info.loc_id)
    )
    await session.commit()
    await session.refresh(user_info)

    return user_info


@handling_interface_error
async def update_settings(
    session: AsyncSession,
    user_info: Users,
    current_settings: CurrentSettings,
    hourly_settings: HourlySettings,
    daily_settings: DailySettings,
    user_settings: UserSettings,
) -> List[Current | Hourly | Daily | UserSettings]:
    updated_settings: List[Current | Hourly | Daily | UserSettings] = []

    if user_settings:
        user_info.settings.update_user_settings(
            **user_settings.model_dump(exclude_none=True)
        )
        session.add(user_info.settings)
        updated_settings.append(user_info.settings)

    if current_settings:
        user_info.current.update_current(
            **current_settings.model_dump(exclude_none=True)
        )
        session.add(user_info.current)
        updated_settings.append(user_info.current)

    if hourly_settings:
        user_info.hourly.update_hourly(**hourly_settings.model_dump(exclude_none=True))
        session.add(user_info.hourly)
        updated_settings.append(user_info.hourly)

    if daily_settings:
        user_info.daily.update_daily(**daily_settings.model_dump(exclude_none=True))
        session.add(user_info.daily)
        updated_settings.append(user_info.daily)

    await session.commit()

    return updated_settings
