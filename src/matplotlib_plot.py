import asyncio
from abc import ABC, abstractmethod
from datetime import datetime

from matplotlib import pyplot as plt
import plotly.graph_objects as go
import pandas as pd

from src.interfaces.repository import AbstractRepository
from src.common.dto.weather import WeatherReportDTO, WeatherPlotDTO
from src.interfaces.uow import AbstractUnitOfWork
from src.service_layer import unit_of_work

LIMIT_SELECT_MANY = 20


class AbstractPlotterAdapter(ABC):
    """Adapter for plotting weather data."""

    @abstractmethod
    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        pass


class MatplotlibPlotterAdapter(AbstractPlotterAdapter):
    """Adapter for plotting weather data using Matplotlib."""

    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        """Draw a plot of the weather data."""
        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(days, temperatures, marker="o", linestyle="-", color="b")
        ax.set_title("Temperature Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)
        plt.show()


class PlotlyPlotterAdapter(AbstractPlotterAdapter):
    """Adapter for plotting weather data using Plotly."""

    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        """Draw a plot of the weather data."""
        # Plot the data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=temperatures, mode="lines+markers"))
        fig.update_layout(
            title="Temperature Over Time",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",
        )
        fig.show()


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


class CSVUnitOfWork(AbstractUnitOfWork):
    """Unit of work for working with CSV files."""

    def __init__(self, path: str) -> None:
        self.weather = CSVRepository(path)

    async def commit(self):
        pass

    async def rollback(self):
        pass


class WeatherPlotterService:
    """Service for plotting weather data."""

    def __init__(
        self, data_source: AbstractUnitOfWork, plotter: AbstractPlotterAdapter
    ):
        self.data_source = data_source
        self.plotter = plotter

    async def read_data(self, limit: int = LIMIT_SELECT_MANY) -> list[WeatherPlotDTO]:
        """Read weather data from the data source."""
        async with self.data_source:
            weather_data = await self.data_source.weather.select_many(limit=limit)
            return [
                WeatherPlotDTO.model_validate(data, from_attributes=True)
                for data in weather_data
            ]

    async def draw(self) -> None:
        """Draw a plot of the weather data."""
        weather_data = await self.read_data()
        days = [data.measurement_time for data in weather_data]
        temperatures = [data.temperature for data in weather_data]
        await self.plotter.draw(days, temperatures)


async def main():
    # weather_plot_service = WeatherPlotterService(
    #     data_source=unit_of_work.SqlAlchemyUnitOfWork(),
    #     plotter=PlotlyPlotterAdapter(),
    # )
    weather_plot_service = WeatherPlotterService(
        data_source=CSVUnitOfWork("../weather_data.csv"),
        plotter=MatplotlibPlotterAdapter(),
    )

    await weather_plot_service.draw()


if __name__ == "__main__":
    asyncio.run(main())
