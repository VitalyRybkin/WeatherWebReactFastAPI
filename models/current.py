from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models import AbstractBaseModel
from models.tablenames import TableNames


class Current(AbstractBaseModel):

    __tablename__ = TableNames.CURRENT

    users = TableNames.USERS

    current_id = Column(Integer, primary_key=True, autoincrement=True)
    acc_id: Mapped[int] = mapped_column(
        ForeignKey(
            f'{users}.acc_id',
            ondelete='CASCADE',
            onupdate='CASCADE',
        ),
    )
    wind_extended: Mapped[bool] = mapped_column(default=False)
    pressure: Mapped[bool] = mapped_column(default=False)
    visibility: Mapped[bool] = mapped_column(default=False)
    humidity: Mapped[bool] = mapped_column(default=False)

    parent: Mapped[users] = relationship(back_populates='current', cascade='all', single_parent=True)

    def __repr__(self):
        return (f'<{self.__class__.__name__}('
                f'current_id={self.current_id}, '
                f'acc_id={self.acc_id}, '
                f'wind_extended={self.wind_extended}, '
                f'pressure={self.pressure}, '
                f'visibility={self.visibility}, '
                f'humidity={self.humidity}, '
                f')>')