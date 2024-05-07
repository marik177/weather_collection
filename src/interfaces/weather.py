from abc import ABC, abstractmethod

from src.common.coordinates import Coordinates
from src.common.dto.weather import WeatherDTO


class AbstractWeatherProvider(ABC):
    @abstractmethod
    async def get_weather(self, coordinates: Coordinates) -> WeatherDTO:
        pass
