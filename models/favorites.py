from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseModel
from .tables import Tables
from .users import UserRelationMixin


class Favorites(UserRelationMixin, AbstractBaseModel):
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
    _user_back_populates = "favorites"
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

    def update_location(
        self, loc_id: int, loc_name: str, loc_region: str, loc_country: str
    ):
        self.loc_id = loc_id
        self.loc_name = loc_name
        self.loc_region = loc_region
        self.loc_country = loc_country

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
