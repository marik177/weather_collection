from common.coordinates import Coordinates
from common.dto.weather import WeatherDTO
from src.interfaces.uow import AbstractUnitOfWork
from src.interfaces.weather import AbstractWeatherProvider


class WeatherService:
    def __init__(self, weather_provider: AbstractWeatherProvider):
        self.weather_provider = weather_provider

    async def _get_weather_from_api(self, coordinates: Coordinates) -> WeatherDTO:
        return await self.weather_provider.get_weather(coordinates)

    async def save_weather(self, coordinates: Coordinates, uow: AbstractUnitOfWork):
        weather = await self._get_weather_from_api(coordinates)
        async with uow:
            await uow.weather.create(**weather.model_dump())
            await uow.commit()
