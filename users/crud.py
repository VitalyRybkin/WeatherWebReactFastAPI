from pydantic import EmailStr
from sqlalchemy import insert, select, Select, Result, exc, delete
from sqlalchemy.exc import IntegrityError, InterfaceError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users, Current, Daily, Hourly, Settings
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
    # TODO make return universal
    return user_info if user_info else None


@handling_interface_error
async def link_user_accounts(
    web_user_found: Users, session: AsyncSession
) -> Users | InterfaceError:
    """
    Function. Updates user accounts - adding bot account to web account.
    :param web_user_found: user info to update.
    :param session: SQLAlchemy session.
    :return: user info if successful or an error.
    """
    session.add(web_user_found)
    await session.commit()
    # TODO make return universal
    return web_user_found


@handling_interface_error
async def delete_user(session, acc_id: int) -> None:
    """
    Function. Deletes a user from the database by account ID.
    :param session: SQLAlchemy session.
    :param acc_id: account ID
    :return: None
    """

    await session.execute(delete(Users).where(Users.id == acc_id))
    await session.commit()
