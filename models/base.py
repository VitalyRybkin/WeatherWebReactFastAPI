from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase


class AbstractBaseModel(DeclarativeBase):
    __abstract__ = True

    # @declared_attr.directive
    # def __tablename__(cls):
    #     return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)
