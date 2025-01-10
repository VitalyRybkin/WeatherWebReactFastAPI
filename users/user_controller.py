import uuid

from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user, get_user_by_login
from utils.schemas import User, UserOut, UserLogin


async def create_user(session: AsyncSession, new_user: User) -> UserOut | None:
    user: User = User(**new_user.model_dump())

    if user.password:
        user.password = Users.hash_password(user.password)
    else:
        user.login = f"{uuid.uuid4()}@bot.com"

    user_created: bool = await create_new_user(session, user)
    if user_created:
        new_user: UserOut = UserOut(**user.model_dump())
        return new_user

    return None


async def user_logging(user: UserLogin, session: AsyncSession) -> bool:
    user_found: Users | None = await get_user_by_login(user.email, session)
    if user_found and user_found.verify_password(user.password.encode()):
        return True

    return False
