from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import AbstractBaseModel
from models.tablenames import TableNames


class Hourly(AbstractBaseModel):

    __tablename__ = TableNames.HOURLY

    users = TableNames.USERS

    hourly_id = Column(Integer, primary_key=True, autoincrement=True)
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

    parent: Mapped[users] = relationship(back_populates="hourly", single_parent=True, cascade="all")

    def __repr__(self):
        return (f'<{self.__class__.__name__}('
                f'hourly_id={self.hourly_id},'
                f'acc_id={self.acc_id},'
                f'wind_extended={self.wind_extended},'
                f'pressure={self.pressure},'
                f'visibility={self.visibility},'
                f'humidity={self.humidity}'
                f')>')