import functools
from typing import Callable

from sqlalchemy.exc import IntegrityError, InterfaceError

from app.logger.logging_handler import database_logger


def to_json(table):
    """
    Function. Convert table to JSON
    """
    if table:
        return {
            col.name: getattr(table, col.name)
            for col in table.__table__.columns
            # if col.name not in ["id", "acc_id"]
        }
    return None


def handling_integrity_error(func) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            func_args: list = [arg for arg in args]
            func_kwargs: dict = {k: v for k, v in kwargs.items()}
            database_logger.error(
                exc_info=e, func_args=func_args, func_kwargs=func_kwargs
            )
            return e

    return wrapper


def handling_interface_error(func) -> Callable:
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get("session")
        try:
            return await func(*args, **kwargs)
        except InterfaceError as e:
            func_args: list = [arg for arg in args]
            func_kwargs: dict = {k: v for k, v in kwargs.items()}
            database_logger.error(
                exc_info=e,
                func_args=func_args,
                func_kwargs=func_kwargs,
            )
            await session.rollback()
            await session.flush()
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                func_args: list = [arg for arg in args]
                func_kwargs: dict = {k: v for k, v in kwargs.items()}
                database_logger.error(
                    msg=f"Reconnection failed!",
                    exc_info=exc,
                    func_args=func_args,
                    func_kwargs=func_kwargs,
                )
            return e

    return wrapper
