import uuid

from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user, get_user, link_user_accounts
from utils.schemas import UserCreate, UserLogin, UserAccountsLink


async def create_user(
    session: AsyncSession, new_user: UserCreate
) -> Users | dict[str, IntegrityError | InterfaceError]:
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

    user_found: Users | None = await get_user(session, user_login=user.login)
    if user_found and user_found.verify_password(user.password.encode()):
        return user_found
    return None


async def linking_accounts(
    user: UserAccountsLink, session: AsyncSession
) -> bool | Users | None:
    """
    Function. Handling of user's accounts linkage.'
    :param user: user accounts information (login, bot_name)
    :param session: AsyncSession
    :return: whether user's accounts were linked or an error on linking accounts
    """

    web_user_found: Users | None = await get_user(session, user_login=user.login)
    bot_user_found: Users | None = await get_user(session, bot_name=user.bot_name)
    if not bot_user_found:
        return False
    web_user_found.bot_id = bot_user_found.bot_id
    web_user_found.bot_name = bot_user_found.bot_name

    accounts_linked: Users | InterfaceError = await link_user_accounts(
        web_user_found, bot_user_found, session
    )
    # await delete_user(session, bot_user_found.id)
    await session.refresh(web_user_found)

    return web_user_found if type(accounts_linked) is Users else None
