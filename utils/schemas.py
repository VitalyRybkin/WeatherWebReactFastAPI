from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    login: EmailStr | None = None


class UserPassword(BaseModel):
    password: Annotated[str, MinLen(5), MaxLen(15)] | None = None


class UserPublic(UserBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    bot_id: int | None = None
    bot_name: str | None = None


class UserCreate(UserPublic, UserPassword):
    pass


class UserLogin(UserBase, UserPassword):
    model_config = ConfigDict(arbitrary_types_allowed=True)
