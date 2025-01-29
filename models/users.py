from datetime import datetime, timezone

import bcrypt
from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_json import mutable_json_type

from .base import AbstractBaseModel
from .tables import Tables


class Users(AbstractBaseModel):
    """
    SQLAlchemy model for storing user information.
    Attributes
    ----------
    login: string
        unique user login (email, not nullable).
    password: string
        hashed user password.
    created_at: datetime
        date account was created (default value).
    deleted: bool
        currant or deleted (default value).
    bot_id: int
        user bot id (default value).
    bot_name: str
        user bot nickname.
    dark_theme: bool
        user web interface theme (default value).
    alert: mutable_json_type(dbtype=JSONB)
        alert schedule jsonb (default value).
    """

    __tablename__ = Tables.USERS

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=True)
    # TODO check for timezone
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    # TODO change deleted to email_confirmed
    deleted: Mapped[bool] = False
    bot_id: Mapped[int] = mapped_column(nullable=True)
    bot_name: Mapped[str] = mapped_column(String(50), nullable=True)
    dark_theme: Mapped[bool] = mapped_column(default=False)
    # TODO add json by default
    alert = Column(mutable_json_type(dbtype=JSONB))

    # TODO change users to wishlist
    users = relationship(
        "Wishlist", back_populates="parent", uselist=True, lazy="joined"
    )
    favorites = relationship(
        "Favorites", back_populates="parent", uselist=False, lazy="joined"
    )
    settings = relationship(
        "Settings", back_populates="parent", uselist=False, lazy="joined"
    )
    hourly = relationship(
        "Hourly", back_populates="parent", uselist=False, lazy="joined"
    )
    daily = relationship("Daily", back_populates="parent", uselist=False, lazy="joined")
    current = relationship(
        "Current", back_populates="parent", uselist=False, lazy="joined"
    )

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Function to hash user's password.
        :param password: string password to hash.
        :return: string password hash.
        """
        salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf8")

    def verify_password(self, password: bytes):
        """
        Function to verify user's password.
        :param password: bytes password to verify.
        :return: whether password matches.
        """
        pwhash: bool = bcrypt.checkpw(password, self.password.encode("utf-8"))
        return pwhash

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"acc_id={self.id}, "
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
