import uuid
from typing import Type

from pydantic import EmailStr
from sqlalchemy.exc import InterfaceError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user, get_user
from utils.schemas import UserCreate, UserLogin


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
        return {"error": user_created}


async def user_logging(user: UserLogin, session: AsyncSession) -> bool:
    user_found: Users | None = await get_user(session, user_login=user.login)
    if user_found and user_found.verify_password(user.password.encode()):
        return True
    return False


async def linking_accounts(
    user_login: EmailStr, bot_name: str, session: AsyncSession
) -> bool:
    web_user_found: Users | None = await get_user(session, user_login=user_login)
    bot_user_found: Users | None = await get_user(session, bot_name=bot_name)
    if not bot_user_found:
        return False
