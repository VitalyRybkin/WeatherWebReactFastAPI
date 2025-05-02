import functools
from typing import Callable

from sqlalchemy.exc import IntegrityError, InterfaceError


def to_json(table):
    """
    Function. Convert table to JSON
    """
    if table:
        return {
            col.name: getattr(table, col.name)
            for col in table.__table__.columns
            if col.name not in ["id", "acc_id"]
        }
    return None


def handling_integrity_error(func) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            print(e)
            return e

    return wrapper


def handling_interface_error(func) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get("session")
        try:
            return await func(*args, **kwargs)
        except InterfaceError as e:
            print(e)
            session.rollback()
            session.flush()
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                print(f"Reconnection failed: {exc}")
            return e

    return wrapper
