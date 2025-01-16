import functools

from sqlalchemy.exc import IntegrityError


def to_json(table):
    """
    Function. Convert table to json
    """
    if table:
        return {col.name: getattr(table, col.name) for col in table.__table__.columns if col.name not in ["id", "acc_id"]}


def handling_integrity_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            print(e)
            return e

    return wrapper


def handling_interface_error(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            print(e)
            return e

    return wrapper
