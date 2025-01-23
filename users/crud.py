from pydantic import EmailStr
from sqlalchemy import insert, select, Select, Result, delete
from sqlalchemy.exc import IntegrityError, InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users, Current, Daily, Hourly, Settings, Favorites, Wishlist
from models.tables import Tables
from utils.setting_schemas import FavoriteLocation
from utils.utils import handling_integrity_error, handling_interface_error


@handling_integrity_error
@handling_interface_error
async def create_new_user(session, user) -> IntegrityError | InterfaceError | Users:
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
    await session.execute(insert(Settings).values(acc_id=user.id))
    await session.commit()

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
    web_user_found: Users, bot_user_found: Users, session: AsyncSession
) -> Users | InterfaceError:
    """
    Function. Updates user accounts - adding bot account to web account. Deletes user's bot-only account.
    :param bot_user_found: bot user info to delete
    :param web_user_found: web user info to update.
    :param session: SQLAlchemy session.
    :return: user info if successful or an error.
    """
    session.add(web_user_found)
    await session.execute(delete(Users).where(Users.id == bot_user_found.id))
    await session.commit()

    return web_user_found


@handling_interface_error
async def change_user_password(
    user_with_new_password: Users, session: AsyncSession
) -> Users | InterfaceError:
    """
    Function. Deletes a user from the database by account ID.
    :param user_with_new_password:
    :param session: SQLAlchemy session.
    :return: None
    """

    session.add(user_with_new_password)
    await session.commit()

    return user_with_new_password


@handling_interface_error
async def add_location(
    location: FavoriteLocation, session: AsyncSession, target
) -> FavoriteLocation | InterfaceError:
    """
    Function. Adds a new location to the database.
    :param location: location info
    :param session: AsyncSession.
    :param target: operation target (table name)
    :return: location info or an error.
    """
    if target == Tables.FAVORITES:
        location_info = Favorites(**location.model_dump())
    else:
        location_info = Wishlist(**location.model_dump())

    session.add(location_info)
    await session.commit()

    return location


@handling_interface_error
async def get_location(session: AsyncSession, acc_id: int) -> Favorites | None:
    """
    Function. Fetches user's favorite location from the database.
    :param session: AsyncSession.
    :param acc_id: user account ID
    :return: favorite location info or an error.
    """
    get_loc_info: Select = select(Favorites).filter(Favorites.acc_id == acc_id)
    result: Result = await session.execute(get_loc_info)
    location_info: Users = result.scalar()

    return location_info if location_info else None


@handling_interface_error
async def update_location(
    new_location: Favorites, session: AsyncSession
) -> Favorites | InterfaceError:
    """
    Function. Updates user's favorite location.
    :param new_location: new favorite location info.
    :param session: AsyncSession.
    :return: updated favorite location info or an error.
    """
    session.add(new_location)
    await session.commit()

    return new_location

@handling_interface_error
async def delete_location(session: AsyncSession, location_info: FavoriteLocation) -> FavoriteLocation | InterfaceError:
    """
    Function. Deletes user's favorite location from wishlist
    :param session: AsyncSession.
    :param location_info: location to delete.
    :return: location info or an error.
    """
    await session.execute(
        delete(Wishlist).where(Wishlist.acc_id == location_info.acc_id).where(Wishlist.loc_id == location_info.loc_id))
    await session.commit()
    return location_info