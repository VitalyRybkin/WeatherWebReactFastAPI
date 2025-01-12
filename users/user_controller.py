import uuid
from typing import Any

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user, get_user
from utils.schemas import UserCreate, UserLogin


async def create_user(
    session: AsyncSession, new_user: UserCreate
) -> dict[str, Any] | None:

    if new_user.password:
        new_user.password = Users.hash_password(new_user.password)
    else:
        new_user.login = f"{uuid.uuid4()}@bot.com"

    user_created: bool = await create_new_user(session, new_user)
    return new_user.model_dump() if user_created else None


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
