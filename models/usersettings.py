from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_json import mutable_json_type
from sqlalchemy.dialects.postgresql import JSONB

from models import AbstractBaseModel
from models.tables import Tables
from models.users import UserRelationMixin


class Settings(UserRelationMixin, AbstractBaseModel):
    """
    SQLAlchemy user settings model
    Attributes
    ----------
    acc_id: int
        user account id.
    current: bool
        display current weather (default=True)
    daily: int
        number of days displayed (default=3)
    hourly: int
        number of hours displayed default=6)
    """

    __tablename__ = Tables.SETTINGS
    _user_back_populates = "settings"
    users = Tables.USERS

    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        unique=True,
    )
    current: Mapped[bool] = mapped_column(default=True)
    daily: Mapped[int] = mapped_column(default=3)
    hourly: Mapped[int] = mapped_column(default=6)
    units: Mapped[str] = mapped_column(default="F", server_default="F")
    dark_theme: Mapped[bool] = mapped_column(default=False, server_default="False")
    notifications = Column(
        mutable_json_type(dbtype=JSONB), default={}, server_default="{}"
    )
    alerts: Mapped[bool] = mapped_column(default=False, server_default="False")

    def update_user_settings(
        self,
        current: bool = None,
        daily: int = None,
        hourly: int = None,
        units: str = None,
    ):
        self.current = current
        self.daily = daily
        self.hourly = hourly
        self.units = units

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"acc_id={self.acc_id},"
            f"current={self.current},"
            f"daily={self.daily},"
            f"hourly={self.hourly},"
            f"units={self.units}>"
            f"parent={self.parent.__repr__()}"
            f")>"
        )
