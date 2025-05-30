"""
Module. Users data SQLAlchemy database model.
"""

from datetime import datetime, timezone
from typing import TYPE_CHECKING

import bcrypt
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship, declared_attr

from .base import AbstractBaseModel
from .tables import Tables

if TYPE_CHECKING:
    from . import Wishlist


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
    email_conf: bool
        email confirmation.
    bot_id: int
        user bot id (default value).
    bot_name: str
        user bot nickname.
    """

    __tablename__ = Tables.USERS

    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )  # TODO check for timezone # pylint: disable=W0511

    email_conf: Mapped[bool] = False
    bot_id: Mapped[int] = mapped_column(nullable=True)
    bot_name: Mapped[str] = mapped_column(String(50), nullable=True)
    # dark_theme: Mapped[bool] = mapped_column(default=False)
    # alert = Column(mutable_json_type(dbtype=JSONB), default={})

    wishlist: Mapped[list["Wishlist"]] = relationship(
        back_populates="parent",
        lazy="joined",
    )

    favorites = relationship(
        f"{Tables.FAVORITES.title()}",
        back_populates="parent",
        uselist=False,
        lazy="joined",
    )

    settings = relationship(
        f"{Tables.SETTINGS.title()}",
        back_populates="parent",
        uselist=False,
        lazy="joined",
    )

    hourly = relationship(
        f"{Tables.HOURLY.title()}",
        back_populates="parent",
        uselist=False,
        lazy="joined",
    )

    daily = relationship(
        f"{Tables.DAILY.title()}",
        back_populates="parent",
        uselist=False,
        lazy="joined",
    )

    current = relationship(
        f"{Tables.CURRENT.title()}",
        back_populates="parent",
        uselist=False,
        lazy="joined",
    )

    @classmethod
    def hash_password(cls, password: str) -> str:
        """
        Function to hash user's password.
        :param password: String password to hash.
        :return: String password hash.
        """
        salt = bcrypt.gensalt()
        password = password.encode("utf-8")
        hashed = bcrypt.hashpw(password, salt)
        return hashed.decode("utf8")

    def verify_password(self, password: bytes):
        """
        Function to verify user's password.
        :param password: Bytes password to verify.
        :return: Whether the password matches.
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
            f"bot_id={self.bot_id}, "
            f"bot_name={self.bot_name}, "
            f")>"
        )


class UserRelationMixin:
    """
    Class. Mixin class for user relations.
    Attributes
    --------
    _user_back_populates: str | None = None
        back populates variable name
    _user_single_parent: bool = True
        one-to-many relation flag
    """

    _user_back_populates: str | None = None
    _user_single_parent: bool = True

    @declared_attr
    def parent(self) -> Mapped[Users]:
        """
        Function. Return user relationship settings.
        :return:
        """
        return relationship(
            f"{Tables.USERS.title()}",
            single_parent=self._user_single_parent,
            back_populates=self._user_back_populates,
            cascade="all, delete",
        )
