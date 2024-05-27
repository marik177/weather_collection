from __future__ import annotations

from typing import Any, Optional, Sequence, TypeVar

from sqlalchemy import ColumnExpressionArgument, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
import pandas as pd

from src.common.dto.weather import WeatherReportDTO
from src.database import Weather
from src.database.models.base.core import Base
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
        """Select and retrieve multiple entries from the data
        storage based on the provided clauses and pagination
        options.
        """
        stmt = (
            select(Weather)
            .where(*clauses)
            .order_by(Weather.measurement_time.desc())
            .offset(offset)
            .limit(limit)
        )
        res = (await self._session.execute(stmt)).scalars().all()
        return res


class CSVRepository(AbstractRepository):
    """Repository for working with CSV files."""

    def __init__(self, path):
        self._weather_path = path
        self._weather_data = []
        self._load_data(self._weather_path)

    async def select_many(self, limit=None) -> list[WeatherReportDTO]:
        return self._weather_data

    def _load_data(self, path):
        """Load weather data from a CSV file."""
        df = pd.read_csv(path)
        for d in df.to_dict(orient="records"):
            self._weather_data.append(WeatherReportDTO(**d))
