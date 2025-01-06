from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import mutable_json_type

from .base import AbstractBaseModel
from .current import Current
from .daily import Daily
from .favorites import Favorites
from .hourly import Hourly
from .settings import Settings
from .tablenames import TableNames
from .wishlist import Wishlist


class Users(AbstractBaseModel):

    __tablename__ = TableNames.USERS

    acc_id = Column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    created_at: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = False
    bot_id: Mapped[int] = mapped_column()
    bot_name: Mapped[str] = mapped_column(String(50))
    dark_theme: Mapped[bool] = mapped_column(default=False)
    alert = Column(mutable_json_type(dbtype=JSONB))

    users: Mapped[List["Wishlist"]] = relationship()
    favorites: Mapped["Favorites"] = relationship(back_populates="parent")
    settings: Mapped["Settings"] = relationship(back_populates="parent")
    hourly: Mapped["Hourly"] = relationship(back_populates="parent")
    daily: Mapped["Daily"] = relationship(back_populates="parent")
    current: Mapped["Current"] = relationship(back_populates="parent")


    def __repr__(self):
        return (f"<{self.__class__.__name__}("
                f"acc_id={self.acc_id}, "
                f"login={self.login}, "
                f"password={self.password}, "
                f"created_at={self.created_at}, "
                f"deleted={self.deleted}, "
                f"bot_id={self.bot_id}, "
                f"bot_name={self.bot_name}, "
                f"dark_theme={self.dark_theme}, "
                f"alert={self.alert}"
                f')>')