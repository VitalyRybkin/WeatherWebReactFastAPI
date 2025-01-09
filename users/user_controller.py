from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from users.crud import create_new_user
from utils.schemas import User, UserOut


async def create_user(session: AsyncSession, new_user: User) -> UserOut | None:
    user: User = User(**new_user.model_dump())
    user.password = Users.hash_password(user.password)
    is_user_created: bool = await create_new_user(session, user)
    if is_user_created:
        new_user: UserOut = UserOut(**user.model_dump())
        return new_user

    return None
