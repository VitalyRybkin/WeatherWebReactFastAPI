from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import AbstractBaseModel
from .tables import Tables


class Wishlist(AbstractBaseModel):
    __tablename__ = Tables.WISHLIST

    users = Tables.USERS

    wishlist_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f"{users}.acc_id",
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
    )
    loc_id: Mapped[int] = mapped_column(nullable=False)
    loc_name: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_region: Mapped[str] = mapped_column(String(100), nullable=False)
    loc_country: Mapped[str] = mapped_column(String(100), nullable=False)

    parent = relationship(
        f"{users.title()}", back_populates="users", cascade="all, delete"
    )

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"wishlist_id={self.wishlist_id},"
            f"acc_id={self.acc_id},"
            f"loc_id={self.loc_id},"
            f"loc_name={self.loc_name},"
            f"loc_region={self.loc_region},"
            f"loc_country={self.loc_country}"
            f")>"
        )
