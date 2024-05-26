import asyncio
from abc import ABC, abstractmethod
from datetime import datetime

from matplotlib import pyplot as plt

from common.dto.weather import WeatherReportDTO
from src.interfaces.uow import AbstractUnitOfWork
from src.service_layer import unit_of_work

LIMIT_SELECT_MANY = 20


class AbstractPlotterAdapter(ABC):
    """Adapter for plotting weather data."""

    @abstractmethod
    async def draw(self, days: tuple[datetime], temperatures: tuple[float]) -> None:
        pass


class MatplotlibPlotterAdapter(AbstractPlotterAdapter):
    """Adapter for plotting weather data using Matplotlib."""

    async def draw(self, days: tuple[datetime], temperatures: tuple[float]) -> None:
        """Draw a plot of the weather data."""
        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(days, temperatures, marker="o", linestyle="-", color="b")
        ax.set_title("Temperature Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)
        plt.show()


class WeatherPlotterService:
    """Service for plotting weather data."""

    def __init__(
        self, data_source: AbstractUnitOfWork, plotter: AbstractPlotterAdapter
    ):
        self.data_source = data_source
        self.plotter = plotter

    async def read_data(self, limit: int = LIMIT_SELECT_MANY) -> list[WeatherReportDTO]:
        """Read weather data from the data source."""
        async with self.data_source:
            weather_data = await self.data_source.weather.select_many(limit=limit)
            return [
                WeatherReportDTO.model_validate(data, from_attributes=True)
                for data in weather_data
            ]

    async def draw(self) -> None:
        """Draw a plot of the weather data."""
        weather_data = await self.read_data()
        data = [[data.measurement_time, data.temperature] for data in weather_data]
        days, temperatures = zip(*data)
        await self.plotter.draw(days, temperatures)


async def main():
    weather_plot_service = WeatherPlotterService(
        data_source=unit_of_work.SqlAlchemyUnitOfWork(),
        plotter=MatplotlibPlotterAdapter(),
    )
    await weather_plot_service.draw()


if __name__ == "__main__":
    asyncio.run(main())
