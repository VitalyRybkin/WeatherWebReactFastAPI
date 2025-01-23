import uuid

from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import (
    create_new_user,
    get_user,
    link_user_accounts,
    change_user_password,
)
from utils.user_schemas import (
    UserCreate,
    UserLogin,
    UserAccountsLink,
    UserChangePassword,
)


async def create_user(
    session: AsyncSession, new_user: UserCreate
) -> Users | IntegrityError | InterfaceError:
    """
    Function. Handling creation of a new user or an error on existing one.
    :param session: AsyncSession
    :param new_user: new user information
    :return: whether new user was created or an error on existing one
    """

    if new_user.password:
        new_user.password = Users.hash_password(new_user.password)
    else:
        new_user.login = f"{uuid.uuid4()}@bot.com"

    user_created: IntegrityError | InterfaceError | Users = await create_new_user(
        session, new_user
    )

    if type(user_created) is not Users:
        await session.rollback()

    return user_created


async def user_logging(user: UserLogin, session: AsyncSession) -> Users | None:
    """
    Function. Handling user logging in.
    :param user: user information (login, password)
    :param session: AsyncSession
    :return: whether user was logged in or an error on incorrect login or password
    """

    user_found: Users | InterfaceError | None = await get_user(
        session, user_login=user.login
    )
    if (
        type(user_found) is Users
        and user_found.verify_password(user.password.encode())
        or type(user_found) is InterfaceError
    ):
        return user_found

    return None


async def linking_accounts(
    user: UserAccountsLink, session: AsyncSession
) -> Users | None:
    """
    Function. Handling of user's accounts linkage.'
    :param user: user accounts information (login, bot_name)
    :param session: AsyncSession
    :return: whether user's accounts were linked or an error on linking accounts
    """

    web_user_found: Users | InterfaceError | None = await get_user(
        session, user_login=user.login
    )
    bot_user_found: Users | InterfaceError | None = await get_user(
        session, bot_name=user.bot_name
    )

    if not bot_user_found:
        return None

    if type(bot_user_found) is Users and type(web_user_found) is Users:
        web_user_found.bot_id = bot_user_found.bot_id
        web_user_found.bot_name = bot_user_found.bot_name

        web_user_found: Users | InterfaceError = await link_user_accounts(
            web_user_found, bot_user_found, session
        )

    return web_user_found


# TODO change password with user id stored in frontend (exclude user_found)
async def change_password(
    user: UserChangePassword, session: AsyncSession
) -> None | Users | InterfaceError:
    """
    Function. Handling user change password.
    :param user: user information (login, old password, new password)
    :param session: AsyncSession
    :return: new user information, an error on new password, None if user was not found
    """
    user_found: Users | InterfaceError | None = await get_user(
        session, user_login=user.login
    )

    if type(user_found) is Users and user_found.verify_password(user.password.encode()):
        user_found.password = Users.hash_password(user.new_password)
        return await change_user_password(user_found, session)
    else:
        return None
