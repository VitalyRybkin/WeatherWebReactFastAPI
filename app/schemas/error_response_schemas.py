"""
Module. Error pydantic models.
"""

from pydantic import BaseModel


class BadRequestMessage(BaseModel):
    """
    Class. Bad request model.
    """

    message: str = "Something went wrong!"


class ErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    message: str
