import asyncio

from src.adapters.report_file import XLSXReportFileAdapter, CSVReportFileAdapter
from src.service_layer.report_service import WeatherReportService
from src.service_layer.weather import OpenMeteoWeatherProvider, get_weather
from src.common.coordinates import Coordinates
from src.common.dto.weather import WeatherDTO
from src.common.utils import get_pause_time, parse_terminal_args
from src.service_layer import unit_of_work
from src.service_layer.weather_storage import save_weather_data


async def main():

    skolkovo_coordinates = Coordinates(55.695626, 37.373635)
    uow = unit_of_work.SqlAlchemyUnitOfWork()
    open_meteo_provider = OpenMeteoWeatherProvider()
    sleep_time = get_pause_time()
    args = parse_terminal_args()
    if args.make_report:
        report_service = WeatherReportService(
            report_file_adapter=XLSXReportFileAdapter()
        )
        await report_service.make_report(uow)
    else:
        while True:
            weather: WeatherDTO = await get_weather(
                open_meteo_provider, skolkovo_coordinates
            )
            await save_weather_data(weather.model_dump(), uow)
            await asyncio.sleep(sleep_time)


if __name__ == "__main__":

    asyncio.run(main())
