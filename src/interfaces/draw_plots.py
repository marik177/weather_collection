from abc import ABC, abstractmethod
from datetime import datetime


class AbstractPlotterAdapter(ABC):
    """Adapter for plotting weather data."""

    @abstractmethod
    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        pass
