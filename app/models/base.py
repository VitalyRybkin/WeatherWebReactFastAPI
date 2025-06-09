"""
Module. Abstract base SQLAlchemy model.
"""

from sqlalchemy import Column, Integer, MetaData
from sqlalchemy.orm import DeclarativeBase
from app.utils import settings


class AbstractBaseModel(DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=settings.db_settings.naming_convention,
    )
    # @declared_attr.directive
    # def __tablename__(cls):
    #     return cls.__name__.lower()

    id = Column(Integer, primary_key=True, autoincrement=True)
