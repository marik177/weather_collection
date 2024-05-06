import pandas as pd

from src.common.dto.weather import WeatherReportDTO
from src.interfaces.uow import AbstractUnitOfWork
from src.service_layer.weather_storage import get_weather_data_from_storage


async def write_to_excel_file(weather_data: list[WeatherReportDTO]) -> None:
    weather_dicts = [weather.model_dump() for weather in weather_data]
    df = pd.DataFrame(weather_dicts)
    with pd.ExcelWriter("weather_data.xlsx") as writer:
        df.to_excel(writer, index=False, sheet_name="Weather Data")


async def make_excel_report(uow: AbstractUnitOfWork):
    weather_data = await get_weather_data_from_storage(uow)
    weather_data.reverse()
    await write_to_excel_file(weather_data)
    return True
