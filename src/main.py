import asyncio

from service_layer.weather_service import WeatherService
from src.adapters.report_file import XLSXReportFileAdapter
from src.adapters.weather import OpenMeteoWeatherProvider
from src.common.coordinates import Coordinates
from src.common.utils import run_script
from src.service_layer import unit_of_work
from src.service_layer.report_service import WeatherReportService


async def main():
    skolkovo_coordinates = Coordinates(55.695626, 37.373635)

    # Initialize components
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    weather_service = WeatherService(weather_provider=OpenMeteoWeatherProvider())
    report_service = WeatherReportService(report_file_adapter=XLSXReportFileAdapter())

    # Run script
    await run_script(skolkovo_coordinates, report_service, weather_service, uow)


if __name__ == "__main__":

    asyncio.run(main())
