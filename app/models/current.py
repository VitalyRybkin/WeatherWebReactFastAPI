"""
Module. Current weather data SQLAlchemy database model.
"""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import AbstractBaseModel

from app.models.tables import Tables
from app.models.users import UserRelationMixin


class Current(UserRelationMixin, AbstractBaseModel):
    """
    SQLAlchemy model for current weather display settings
    Attributes
    ---------
    acc_id: int
        user account ID
    wind_extended: bool
        wind extended forecast display (default=False)
    pressure: bool
        pressure forecast display (default=False)
    visibility: bool
        visibility forecast display(default=False)
    humidity: bool
        humidity forecast display(default=False)
    """

    __tablename__ = Tables.CURRENT
    _user_back_populates = "current"
    users = Tables.USERS

    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        unique=True,
    )
    wind_extended: Mapped[bool] = mapped_column(default=False)
    pressure: Mapped[bool] = mapped_column(default=False)
    visibility: Mapped[bool] = mapped_column(default=False)
    humidity: Mapped[bool] = mapped_column(default=False)

    def update_current(
        self,
        wind_extended: bool = None,
        pressure: bool = None,
        visibility: bool = None,
        humidity: bool = None,
    ) -> None:
        """
        Function to update current weather display settings.
        :param wind_extended: wind extended forecast display (default=False)
        :param pressure: pressure forecast display (default=False)
        :param visibility: visibility forecast display (default=False)
        :param humidity: humidity forecast display (default=False)
        :return: None
        """
        self.wind_extended = wind_extended
        self.pressure = pressure
        self.visibility = visibility
        self.humidity = humidity

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"acc_id={self.acc_id}, "
            f"wind_extended={self.wind_extended}, "
            f"pressure={self.pressure}, "
            f"visibility={self.visibility}, "
            f"humidity={self.humidity}, "
            f")>"
        )
