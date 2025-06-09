"""
Module.Set database connection class
"""

from typing import Any, AsyncGenerator

from asyncio import current_task

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
    AsyncSession,
)


from app.utils.settings import settings


class DatabaseEngine:
    """
    Class. Database engine class.
    """

    def __init__(self):
        self.engine = create_async_engine(
            url=settings.db_conn,
            echo=settings.db_echo,
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
        )
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    def scoped_session(self) -> async_scoped_session[AsyncSession]:
        """
        Function. Scoped session factory.
        :return:
        """
        return async_scoped_session(
            session_factory=self.session,
            scopefunc=current_task,
        )

    async def dispose(self) -> None:
        await self.engine.dispose()

    async def session_dependency(
        self,
    ) -> AsyncGenerator[async_scoped_session[AsyncSession | Any], Any]:
        """
        Function. Dependency session factory.
        :return:
        """
        session = self.scoped_session()
        yield session
        await session.close()


db_engine = DatabaseEngine()
