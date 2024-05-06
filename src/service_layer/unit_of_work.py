from __future__ import annotations
from src.database.core.connection import DEFAULT_SESSION_FACTORY
from src.repositories import WeatherSQLAlchemyRepository
from src.interfaces.uow import AbstractUnitOfWork
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY) -> None:
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()  # type: AsyncSession
        self.weather = WeatherSQLAlchemyRepository(self.session)

        return await super().__aenter__()

    async def __aexit__(self, *args):
        await super().__aexit__(*args)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
