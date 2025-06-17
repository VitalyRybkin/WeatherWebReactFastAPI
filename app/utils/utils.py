"""
Module. Functions to handle application operations.
"""

import functools
from typing import Callable, Any

from sqlalchemy.exc import IntegrityError, InterfaceError

from app.logger.logging_handler import database_logger


def to_json(table) -> dict[Any, Any] | None:
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
    """
    Function. Handle IntegrityError decorator
    :param func: callable function
    :return: function
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            database_logger.error(
                msg="Database integrity error.",
                exc_info=e,
            )
            return e

    return wrapper


def handling_interface_error(func) -> Callable:
    """
    Function. Handle InterfaceError decorator
    :param func: callable function
    :return: function
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get("session")
        try:
            return await func(*args, **kwargs)
        except InterfaceError as e:
            database_logger.error(
                msg="Database connection error",
                exc_info=e,
            )
            await session.rollback()
            await session.flush()
            try:
                return await func(*args, **kwargs)
            except Exception as exc:
                database_logger.error(
                    msg="Reconnection failed!",
                    exc_info=exc,
                )
            return e

    return wrapper
