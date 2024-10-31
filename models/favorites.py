from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr

from .base import AbstractBaseModel
from .accounts import Accounts


class Favorites(AbstractBaseModel):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    fav_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{Accounts.__tablename__}.acc_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    location_id: Mapped[int] = mapped_column(nullable=False)
