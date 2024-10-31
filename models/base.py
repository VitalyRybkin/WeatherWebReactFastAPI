from sqlalchemy.orm import DeclarativeBase


class AbstractBaseModel(DeclarativeBase):
    __abstract__ = True
