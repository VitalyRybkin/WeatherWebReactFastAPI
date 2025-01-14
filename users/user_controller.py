import uuid

from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user, get_user, link_user_accounts, delete_user
from utils.schemas import UserCreate, UserLogin, UserAccountsLink


async def create_user(
    session: AsyncSession, new_user: UserCreate
) -> Users | dict[str, IntegrityError | InterfaceError]:

    if new_user.password:
        new_user.password = Users.hash_password(new_user.password)
    else:
        new_user.login = f"{uuid.uuid4()}@bot.com"

    user_created: IntegrityError | InterfaceError | Users = await create_new_user(
        session, new_user
    )
    if type(user_created) is Users:
        return user_created
    else:
        await session.rollback()
        return {"error": user_created}


async def user_logging(user: UserLogin, session: AsyncSession) -> Users | None:
    user_found: Users | None = await get_user(session, user_login=user.login)
    if user_found and user_found.verify_password(user.password.encode()):
        return user_found
    return None


async def linking_accounts(
    user: UserAccountsLink, session: AsyncSession
) -> bool | Users | None:
    web_user_found: Users | None = await get_user(session, user_login=user.login)
    bot_user_found: Users | None = await get_user(session, bot_name=user.bot_name)
    if not bot_user_found:
        return False
    web_user_found.bot_id = bot_user_found.bot_id
    web_user_found.bot_name = bot_user_found.bot_name

    accounts_linked: Users | InterfaceError = await link_user_accounts(
        web_user_found, session
    )
    await delete_user(session, bot_user_found.id)
    await session.refresh(web_user_found)

    return web_user_found if type(accounts_linked) is Users else None
