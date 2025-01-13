from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import AbstractBaseModel
from models.tables import Tables


class Daily(AbstractBaseModel):
    __tablename__ = Tables.DAILY

    users = Tables.USERS

    # daily_id = Column(Integer, primary_key=True, autoincrement=True)
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

    parent: Mapped[users] = relationship(
        f"{users.title()}",
        back_populates="daily",
        single_parent=True,
        cascade="all, delete",
        lazy="joined",
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            # f"daily_id={self.daily_id}, "
            f"astro={self.astro}, "
            f"visibility={self.visibility}, "
            f"humidity={self.humidity}, "
            f")>"
        )
