from pydantic import BaseModel


class BadRequestMessage(BaseModel):
    message: str = "Something went wrong!"


class ErrorMessage(BaseModel):
    message: str
