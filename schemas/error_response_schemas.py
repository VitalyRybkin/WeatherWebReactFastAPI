from pydantic import BaseModel


class BadRequestMessage(BaseModel):
    message: str = "Something went wrong!"


class Message(BaseModel):
    message: str
