from __future__ import annotations

from src.database import Weather


from typing import (
    Any,
    Optional,
    Sequence,
    TypeVar,
)

from sqlalchemy import ColumnExpressionArgument, insert
from src.database.models.base.core import Base

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from src.interfaces.repository import AbstractRepository

ModelType = TypeVar("ModelType", bound=Base)


class WeatherSQLAlchemyRepository(AbstractRepository):

    __slots__ = ("_session",)

    def __init__(self, session: AsyncSession) -> None:

        self._session = session

    async def create(self, **values: Any) -> Optional[ModelType]:
        """Create a new entry in the data storage using the provided values."""
        stmt = insert(Weather).values(**values).returning(Weather)
        return (await self._session.execute(stmt)).scalars().first()

    async def select_many(
        self,
        *clauses: ColumnExpressionArgument[bool],
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[ModelType]:
        """Select and retrieve multiple entries from the data storage based on the provided clauses and pagination
        options.
        """
        stmt = select(Weather).where(*clauses).offset(offset).limit(limit)
        res = (await self._session.execute(stmt)).scalars().all()
        return res
