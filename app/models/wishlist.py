"""
Module. Wishlist SQLAlchemy database model.
"""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import AbstractBaseModel
from .tables import Tables
from .users import UserRelationMixin


class Wishlist(UserRelationMixin, AbstractBaseModel):
    """
    SQLAlchemy model for storing user's Wishlist.
    Attributes
    ----------
    loc_id: int
        favorite location ID.
    loc_name: str
        favorite location name.
    loc_region: str
        favorite location region.
    loc_country: str
        favorite location country.

    """

    __tablename__ = Tables.WISHLIST
    _user_back_populates = "wishlist"
    _user_single_parent = False
    users = Tables.USERS

    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    loc_id: Mapped[int] = mapped_column(nullable=False)
    loc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_region: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_country: Mapped[str] = mapped_column(String(100), nullable=False)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            # f"wishlist_id={self.wishlist_id},"
            f"acc_id={self.acc_id},"
            f"loc_id={self.loc_id},"
            f"loc_name={self.loc_name},"
            f"loc_region={self.loc_region},"
            f"loc_country={self.loc_country}"
            f")>"
        )
