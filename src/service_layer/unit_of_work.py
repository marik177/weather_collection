from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from src.database.core.connection import DEFAULT_SESSION_FACTORY
from src.interfaces.uow import AbstractUnitOfWork
from src.repositories import WeatherSQLAlchemyRepository, CSVRepository


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.weather = WeatherSQLAlchemyRepository(self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


class CSVUnitOfWork(AbstractUnitOfWork):
    """Unit of work for working with CSV files."""

    def __init__(self, path: str) -> None:
        self.weather = CSVRepository(path)

    async def commit(self):
        pass

    async def rollback(self):
        pass
