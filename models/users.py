from datetime import datetime, timezone

import bcrypt
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import mutable_json_type

from .base import AbstractBaseModel
from .tables import Tables


class Users(AbstractBaseModel):
    __tablename__ = Tables.USERS

    acc_id = Column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    deleted: Mapped[bool] = False
    bot_id: Mapped[int] = mapped_column(nullable=True)
    bot_name: Mapped[str] = mapped_column(String(50), nullable=True)
    dark_theme: Mapped[bool] = mapped_column(default=False)
    alert = Column(mutable_json_type(dbtype=JSONB))

    users = relationship("Wishlist", back_populates="parent", uselist=True)
    favorites = relationship("Favorites", back_populates="parent", uselist=False)
    settings = relationship("Settings", back_populates="parent", uselist=False)
    hourly = relationship("Hourly", back_populates="parent", uselist=False)
    daily = relationship("Daily", back_populates="parent", uselist=False)
    current = relationship("Current", back_populates="parent", uselist=False)

    @classmethod
    def hash_password(cls, password: str) -> str:
        salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf8")

    def verify_password(self, password):
        pwhash = bcrypt.checkpw(password, self.password.encode("utf-8"))
        return pwhash

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"acc_id={self.acc_id}, "
            f"login={self.login}, "
            f"password={self.password}, "
            f"created_at={self.created_at}, "
            f"deleted={self.deleted}, "
            f"bot_id={self.bot_id}, "
            f"bot_name={self.bot_name}, "
            f"dark_theme={self.dark_theme}, "
            f"alert={self.alert}"
            f")>"
        )
