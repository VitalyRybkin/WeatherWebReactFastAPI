from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AbstractBaseModel
from .tables import Tables


class Favorites(AbstractBaseModel):
    """
    SQLAlchemy model for user favorite location
    Attributes
    ----------
    loc_id: int
        user favorite location ID (nullable=False)
    loc_name: str
        user favorite location name (String(100), nullable=False)
    loc_region: str
        user favorite location region (String(100), nullable=False)
    loc_country: str
        user favorite location country (String(100), nullable=False)
    """
    __tablename__ = Tables.FAVORITES

    users = Tables.USERS

    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        unique=True,
    )
    loc_id: Mapped[int] = mapped_column(nullable=False)
    loc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_region: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_country: Mapped[str] = mapped_column(String(100), nullable=False)

    parent = relationship(
        f"{users.title()}",
        back_populates="favorites",
        single_parent=True,
        cascade="all, delete",
        lazy="joined",
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            # f"favorites_id={self.favorites_id}, "
            f"acc_id={self.acc_id}, "
            f"loc_id={self.loc_id}, "
            f"loc_name={self.loc_name}, "
            f"loc_region={self.loc_region}, "
            f"loc_country={self.loc_country}"
            f")>"
        )
