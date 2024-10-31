from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import declared_attr, Mapped, mapped_column

from .base import AbstractBaseModel
from .accounts import Accounts


class Settings(AbstractBaseModel):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()

    set_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{Accounts.__tablename__}.acc_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    dark: Mapped[bool] = mapped_column(default=False)
    day_amount: Mapped[int] = mapped_column(default=3)
    hour_amount: Mapped[int] = mapped_column(default=12)
    astro: Mapped[bool] = mapped_column(default=False)
    marine: Mapped[bool] = mapped_column(default=False)
    telegram_account: Mapped[str] = mapped_column(default=None)
    telegram_notification: Mapped[datetime] = mapped_column(default=None)
