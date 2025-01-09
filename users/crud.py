from sqlalchemy import insert, select, Select
from sqlalchemy.dialects.postgresql import Insert
from sqlalchemy.exc import IntegrityError

from models import Users, Current, Daily, Hourly, Settings


async def create_new_user(session, user):
    try:
        insert_new_user: Insert = insert(Users).values(
            login=user.login, password=user.password.decode("utf-8")
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
    except IntegrityError:
        await session.rollback()
        return False

    return True
