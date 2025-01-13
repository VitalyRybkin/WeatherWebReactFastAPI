from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import AbstractBaseModel
from models.tables import Tables


class Settings(AbstractBaseModel):
    __tablename__ = Tables.SETTINGS

    users = Tables.USERS

    # set_id = Column(Integer, primary_key=True, autoincrement=True)
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

    parent = relationship(
        f"{users.title()}",
        back_populates="settings",
        single_parent=True,
        cascade="all, delete",
        lazy="joined",
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            # f"set_id={self.set_id},"
            f"acc_id={self.acc_id},"
            f"current={self.current},"
            f"daily={self.daily},"
            f"hourly={self.hourly}"
            f"parent={self.parent.__repr__()}"
            f")>"
        )
