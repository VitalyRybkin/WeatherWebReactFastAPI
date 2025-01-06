from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import AbstractBaseModel
from models.tablenames import TableNames


class Settings(AbstractBaseModel):

    __tablename__ =TableNames.SETTINGS

    users = TableNames.USERS

    set_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.acc_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    current: Mapped[bool] = mapped_column(default=True)
    daily: Mapped[int] = mapped_column(default=3)
    hourly: Mapped[int] = mapped_column(default=6)

    parent: Mapped[users] = relationship(back_populates="settings", single_parent=True)

    def __repr__(self):
        return (f"<{self.__class__.__name__}("
                f"set_id={self.set_id},"
                f"acc_id={self.acc_id},"
                f"current={self.current},"
                f"daily={self.daily},"
                f"hourly={self.hourly}"
                f"parent={self.parent.__repr__()}"
                f')>')

