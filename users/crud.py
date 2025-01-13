from pydantic import EmailStr
from sqlalchemy import insert, select, Select, Result, exc
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.exc import IntegrityError, InterfaceError

from models import Users, Current, Daily, Hourly, Settings
from utils import UserCreate


async def create_new_user(session, user) -> IntegrityError | InterfaceError | Users:
    try:
        user = Users(**user.model_dump())
        session.add(user)
        await session.commit()

        await session.execute(insert(Current).values(acc_id=user.id))
        await session.execute(insert(Daily).values(acc_id=user.id))
        await session.execute(insert(Hourly).values(acc_id=user.id))
        await session.execute(insert(Settings).values(acc_id=user.id))
        await session.commit()

    except IntegrityError as e:
        print(e)
        await session.rollback()
        return e

    except exc.InterfaceError as e:
        print(e)
        await session.rollback()
        return e

    return user


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
