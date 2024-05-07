from src.common.dto.weather import WeatherReportDTO
from src.interfaces.report_file import AbstractReportFileAdapter
from src.interfaces.uow import AbstractUnitOfWork


class WeatherReportService:
    def __init__(self, report_file_adapter: AbstractReportFileAdapter):
        self.report_file_adapter = report_file_adapter

    @staticmethod
    async def _get_weather_data_from_storage(uow: AbstractUnitOfWork, limit: int = 10):
        async with uow:
            weather_data = await uow.weather.select_many(limit=limit)
            return [
                WeatherReportDTO.model_validate(data, from_attributes=True)
                for data in weather_data
            ]

    async def make_report(self, uow: AbstractUnitOfWork) -> str:
        weather_data = await self._get_weather_data_from_storage(uow)
        weather_data.reverse()
        return await self.report_file_adapter.create_report_file(weather_data)
