import asyncio
from datetime import datetime

import aiohttp

import config
from src.common.coordinates import Coordinates
from src.common.dto.weather import WeatherDTO
from src.common.enums import WindDirection
from src.common.exceptions import ApiServiceError
from src.interfaces.weather import AbstractWeatherProvider


class OpenMeteoWeatherProvider(AbstractWeatherProvider):
    def __init__(self):
        self._api_url = config.OPEN_METEO_URL

    async def get_weather(self, coordinates: Coordinates) -> WeatherDTO:
        try:
            open_meteo_response = await self._get_open_meteo_response(coordinates)
        except Exception as e:
            raise ApiServiceError("Can't get response from open-meteo") from e
        weather = await self._parse_open_meteo_response(open_meteo_response)
        return weather

    async def _parse_open_meteo_response(self, open_meteo_response):
        try:
            weather = WeatherDTO(
                measurement_time=datetime.now(),
                temperature=open_meteo_response["current"]["temperature_2m"],
                wind_speed=open_meteo_response["current"]["wind_speed_10m"],
                wind_direction=self._parse_wind_direction(open_meteo_response),
                pressure=open_meteo_response["current"]["surface_pressure"],
                rain=open_meteo_response["current"]["rain"],
                showers=open_meteo_response["current"]["showers"],
                snowfall=open_meteo_response["current"]["snowfall"],
            )
        except KeyError:
            raise ApiServiceError("Can't get weather from response")
        return weather

    async def _get_open_meteo_response(self, coordinates: Coordinates) -> dict:
        url = self._api_url.format(
            latitude=coordinates.latitude, longitude=coordinates.longitude
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.json()

    @staticmethod
    def _parse_degrees_to_direction(d: float) -> WindDirection:
        dirs = list(WindDirection)
        ix = round(d / (360 / len(dirs)))
        return dirs[ix % len(dirs)]

    def _parse_wind_direction(self, open_meteo_response: dict) -> WindDirection:
        try:
            return self._parse_degrees_to_direction(
                open_meteo_response["current"]["wind_direction_10m"]
            )
        except KeyError:
            raise ApiServiceError("Can't get wind direction from response")


async def get_weather(
    weather_provider: AbstractWeatherProvider, coordinates: Coordinates
) -> WeatherDTO:
    return await weather_provider.get_weather(coordinates)


if __name__ == "__main__":
    open_meteo = OpenMeteoWeatherProvider()
    asyncio.run(open_meteo.get_weather(Coordinates(52.52, 13.405)))
