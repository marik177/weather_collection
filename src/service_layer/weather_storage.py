from common.dto.weather import WeatherReportDTO
from src.interfaces.uow import AbstractUnitOfWork


async def save_weather_data(weather_data: dict, uow: AbstractUnitOfWork) -> None:
    async with uow:
        await uow.weather.create(**weather_data)
        await uow.commit()


async def get_weather_data_from_storage(
    uow: AbstractUnitOfWork, limit: int = 10
) -> list[WeatherReportDTO]:
    async with uow:
        weather_data = await uow.weather.select_many(limit=limit)
        return [
            WeatherReportDTO.model_validate(data, from_attributes=True)
            for data in weather_data
        ]
