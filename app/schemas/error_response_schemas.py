"""
Module. Error pydantic models.
"""

from pydantic import BaseModel, ConfigDict


class BadRequestMessage(BaseModel):
    """
    Class. Bad request model.
    """

    message: str = "Something went wrong!"


class DBErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    detail: str = "Database connection error. {msg}"
    headers: dict[str, str] | None = None


class ConflictErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    message: str = "{msg} already exists."
    headers: dict[str, str] | None = None


class UnauthorizedErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    message: str = "Incorrect username or password."
    headers: dict[str, str] | None = None


class NotFoundErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    message: str = "{msg} not found."
    headers: dict[str, str] | None = None


class Ok(BaseModel):
    """
    Class. Error model.
    """

    success: bool = True
    message: str = "{msg}"


class UnprocessableErrorMessage(BaseModel):
    """
    Class. Error model.
    """

    message: str = "{msg}"
    headers: dict[str, str] | None = None
