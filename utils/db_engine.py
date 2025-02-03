from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)


from asyncio import current_task

from utils.settings import settings


class DatabaseEngine:
    def __init__(self):
        self.engine = create_async_engine(
            url=settings.db_conn,
            echo=settings.db_echo,
            pool_size=5,
            max_overflow=10,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def scoped_session(self):
        return async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )

    async def session_dependency(self) -> AsyncSession:
        session = self.scoped_session()
        yield session
        await session.close()


db_engine = DatabaseEngine()
