"""
Module. Get data from DB and API and prepare it to be passed to the router.
"""

import uuid
from typing import Annotated, Any, Coroutine

from fastapi import Depends, Form
from fastapi.security import HTTPBasic
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.exceptions import HTTPException

from app.models import Users
from app.schemas.user_schemas import (
    UserCreate,
    UserLogin,
    UserAccountsLink,
    UserChangePassword,
)
from app.users.crud import (
    create_new_user,
    get_user,
    link_user_accounts,
    change_user_password,
)
from app.utils import db_engine


async def create_user(
    session: AsyncSession, new_user: UserCreate
) -> Users | IntegrityError | InterfaceError:
    """
    Function. Handling creation of a new user or an error on existing one.
    :param session: AsyncSession
    :param new_user: new user information
    :return:  Whether a new user was created or an error on existing one
    """

    if new_user.password:
        new_user.password = Users.hash_password(new_user.password)
    else:
        new_user.login = f"{uuid.uuid4()}@bot.com"

    user_created: Users = await create_new_user(session=session, user=new_user)

    return user_created


# security = HTTPBasic()


async def user_logging(
    # user: UserLogin, session: AsyncSession
    # user: Annotated[UserLogin, Depends(security)],
    login: str = Form(...),
    password: str = Form(...),
    # session: AsyncSession
    session: AsyncSession = Depends(db_engine.session_dependency),
) -> Users | None | type[InterfaceError]:
    """
    Function. Handling user logging in.
    :param user: user information (login, password)
    :param session: AsyncSession
    :return: whether user was logged in or an error on incorrect login or password
    """

    user_found: Users | InterfaceError | None = await get_user(
        session=session, user_login=login
    )

    if (
        user_found
        and type(user_found) is Users
        and user_found.verify_password(password.encode())
    ):
        return user_found

    if type(user_found) is InterfaceError:
        return InterfaceError

    return None


async def linking_accounts(
    user: UserAccountsLink, session: AsyncSession
) -> Users | InterfaceError | None:
    """
    Function. Handling of user's accounts linkage.'
    :param user: user accounts information (login, bot_name)
    :param session: AsyncSession
    :return: whether user's accounts were linked or an error on linking accounts
    """
    web_user_info: Users | InterfaceError | None = await get_user(
        session=session, user_login=user.login
    )
    bot_user_info: Users | InterfaceError | None = await get_user(
        session=session, bot_name=user.bot_name
    )

    if not bot_user_info:
        return None

    # if type(bot_user_info) is Users and type(web_user_info) is Users:
    if isinstance(bot_user_info, Users) and isinstance(web_user_info, Users):
        web_user_info.bot_id = bot_user_info.bot_id
        web_user_info.bot_name = bot_user_info.bot_name

        web_user_info: Users | InterfaceError = await link_user_accounts(
            session=session,
            web_user=web_user_info,
            bot_user=bot_user_info,
        )

    return web_user_info


async def change_password(
    user: UserChangePassword, session: AsyncSession
) -> None | Users | InterfaceError:
    """
    Function. Handling user change password.
    :param user: user information (login, old password, new password)
    :param session: AsyncSession
    :return: new user information, an error on new password, None if user was not found
    """
    user_info: Users | InterfaceError | None = await get_user(
        session=session, user_login=user.login
    )

    # if type(user_info) is Users:
    if isinstance(user_info, Users):
        if user_info.verify_password(user.password.encode()):
            user_info.password = Users.hash_password(user.new_password)
            user_info: Users = await change_user_password(
                session=session, user_with_new_password=user_info
            )
        else:
            return None

    return user_info
