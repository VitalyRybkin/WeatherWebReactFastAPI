from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from utils.settings import settings


class DatabaseEngine:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.db_conn,
            echo=settings.db_echo,
            pool_size=5,
            max_overflow=10,
        )
        self.sessions = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


db_engine = DatabaseEngine()
