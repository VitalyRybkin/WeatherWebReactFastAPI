from pydantic import EmailStr
from sqlalchemy import insert, select, Select
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.exc import IntegrityError

from models import Users, Current, Daily, Hourly, Settings
from utils import UserCreate


async def create_new_user(session, user) -> bool:
    try:
        insert_new_user: Insert = insert(Users).values(
            login=user.login,
            password=user.password,
            bot_id=user.bot_id,
            bot_name=user.bot_name,
        )

        await session.execute(insert_new_user)
        await session.commit()

        select_acc_id: Select = select(Users.acc_id).filter(Users.login == user.login)
        result = await session.execute(select_acc_id)

        get_acc_id: int = result.scalar()

        await session.execute(insert(Current).values(acc_id=get_acc_id))
        await session.execute(insert(Daily).values(acc_id=get_acc_id))
        await session.execute(insert(Hourly).values(acc_id=get_acc_id))
        await session.execute(insert(Settings).values(acc_id=get_acc_id))

        await session.commit()
    except IntegrityError as e:
        print(e)
        await session.rollback()
        return False

    return True


async def get_user(
    session, user_login: EmailStr = None, bot_name: str = None
) -> UserCreate | None:
    if user_login:
        get_user_info: Select = select(Users).filter(Users.login == user_login)
    else:
        get_user_info: Select = select(Users).filter(Users.bot_name == bot_name)
    result = await session.execute(get_user_info)
    user: UserCreate = result.scalar()
    return user if user else None
