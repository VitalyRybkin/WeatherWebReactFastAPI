from sqlalchemy import Column, Integer
from sqlalchemy.orm import Mapped, declared_attr, mapped_column

from .base import AbstractBaseModel


class Accounts(AbstractBaseModel):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    acc_id = Column(Integer, primary_key=True, autoincrement=True)
    login: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = False
