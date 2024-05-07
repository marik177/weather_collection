import pandas as pd

from src.interfaces.report_file import AbstractReportFileAdapter
from src.common.dto.weather import WeatherReportDTO
from src.interfaces.uow import AbstractUnitOfWork
from src.service_layer.weather_storage import get_weather_data_from_storage


class WeatherReportService:
    def __init__(self, report_file_adapter: AbstractReportFileAdapter):
        self.report_file_adapter = report_file_adapter

    async def make_report(self, uow: AbstractUnitOfWork):
        weather_data = await get_weather_data_from_storage(uow)
        weather_data.reverse()
        self.report_file_adapter.create_report_file(weather_data)
        return True
