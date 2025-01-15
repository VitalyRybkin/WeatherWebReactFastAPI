from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import AbstractBaseModel
from models.tables import Tables


class Current(AbstractBaseModel):
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

    parent = relationship(
        f"{users.title()}",
        back_populates="current",
        single_parent=True,
        cascade="all, delete",
        lazy="joined",
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            # f"current_id={self.current_id}, "
            f"acc_id={self.acc_id}, "
            f"wind_extended={self.wind_extended}, "
            f"pressure={self.pressure}, "
            f"visibility={self.visibility}, "
            f"humidity={self.humidity}, "
            f")>"
        )
