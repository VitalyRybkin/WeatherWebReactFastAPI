from pydantic import BaseModel, EmailStr, ConfigDict


class UserOut(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    login: EmailStr | None = None
    bot_id: int | None = None
    bot_name: str | None = None


class User(UserOut):
    password: str | None = None


class UserLogin(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    email: EmailStr | None
    password: str | None
