from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import AbstractBaseModel
from models.tables import Tables


class Daily(AbstractBaseModel):
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
    ):
        self.astro = astro
        self.visibility = visibility
        self.humidity = humidity

    parent: Mapped[users] = relationship(
        f"{users.title()}",
        back_populates="daily",
        single_parent=True,
        cascade="all, delete",
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"astro={self.astro}, "
            f"visibility={self.visibility}, "
            f"humidity={self.humidity}, "
            f")>"
        )
