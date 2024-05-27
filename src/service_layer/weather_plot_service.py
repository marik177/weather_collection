from src.common.dto.weather import WeatherPlotDTO
from src.interfaces.draw_plots import AbstractPlotterAdapter
from src.interfaces.uow import AbstractUnitOfWork

LIMIT_SELECT_MANY = 20


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
