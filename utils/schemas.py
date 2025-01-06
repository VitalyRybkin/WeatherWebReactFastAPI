from pydantic import BaseModel, EmailStr, ConfigDict


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    login: EmailStr | None
