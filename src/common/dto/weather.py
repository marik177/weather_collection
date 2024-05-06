from datetime import datetime

from src.common.enums import WindDirection
from src.common.dto.base import DTO


class WeatherDTO(DTO):
    measurement_time: datetime
    temperature: float
    wind_speed: float
    wind_direction: WindDirection
    pressure: float
    rain: float
    showers: float
    snowfall: float
    address: str = "Сколково"


class WeatherReportDTO(WeatherDTO):
    id: int
