"""
Module. Daily forecast data SQLAlchemy database model.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AbstractBaseModel

from app.models.tables import Tables
from app.models.users import UserRelationMixin


class Daily(UserRelationMixin, AbstractBaseModel):
    """
    SQLAlchemy model for Daily weather display settings
    Attributes
    ----------
    acc_id: int
        user account ID
    astro: bool
        astro forecast display (default=False)
    visibility: bool
        visibility forecast display (default=False)
    humidity: bool
        humidity forecast display (default=False)
    """

    __tablename__ = Tables.DAILY
    _user_back_populates = "daily"

    users = Tables.USERS

    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        unique=True,
    )
    astro: Mapped[bool] = mapped_column(default=False)
    visibility: Mapped[bool] = mapped_column(default=False)
    humidity: Mapped[bool] = mapped_column(default=False)

    def update_daily(
        self,
        astro: bool = None,
        visibility: bool = None,
        humidity: bool = None,
    ) -> None:
        """
        Function to update daily display settings.
        :param astro: astro info display (default=False)
        :param visibility: visibility forecast display (default=False)
        :param humidity: humidity forecast display (default=False)
        :return: None
        """
        self.astro = astro
        self.visibility = visibility
        self.humidity = humidity

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"astro={self.astro}, "
            f"visibility={self.visibility}, "
            f"humidity={self.humidity}, "
            f")>"
        )
