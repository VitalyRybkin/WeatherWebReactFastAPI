from datetime import datetime

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy.sql.annotation import Annotated


class User(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    login: EmailStr
    password: Annotated[str, MinLen(8), MaxLen(20)]
    created_at: Annotated[datetime] = datetime.timestamp(datetime.now())
    deleted: Annotated[bool] = False
