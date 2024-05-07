import argparse
import asyncio

import config
from src.common.coordinates import Coordinates
from src.interfaces.uow import AbstractUnitOfWork
from src.service_layer.report_service import WeatherReportService
from src.service_layer.weather_service import WeatherService


def parse_terminal_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Process weather data and generate Excel report"
    )
    parser.add_argument(
        "--make_report", action="store_true", help="Generate Excel report"
    )
    return parser.parse_args()


def get_pause_time() -> float:
    requests_per_hour = config.REQUESTS_PER_HOUR
    return 60 / requests_per_hour * 60


async def make_pause():
    sleep_time = get_pause_time()
    await asyncio.sleep(sleep_time)


async def run_script(
    coordinates: Coordinates,
    report_service: WeatherReportService,
    weather_service: WeatherService,
    uow: AbstractUnitOfWork,
):
    args = parse_terminal_args()
    if args.make_report:
        await report_service.make_report(uow)
    else:
        while True:
            await weather_service.save_weather(coordinates, uow)
            await make_pause()
