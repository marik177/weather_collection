import pandas as pd

from src.common.dto.weather import WeatherReportDTO
from src.interfaces.report_file import AbstractReportFileAdapter


class XLSXReportFileAdapter(AbstractReportFileAdapter):
    async def create_report_file(self, weather_data: list[WeatherReportDTO]) -> str:
        weather_dicts = [weather.model_dump() for weather in weather_data]
        df = pd.DataFrame(weather_dicts)
        path = "weather_data.xlsx"
        with pd.ExcelWriter(path) as writer:
            df.to_excel(writer, index=False, sheet_name="Weather Data")
            return path


class CSVReportFileAdapter(AbstractReportFileAdapter):
    async def create_report_file(self, weather_data: list[WeatherReportDTO]) -> str:
        weather_dicts = [weather.model_dump() for weather in weather_data]
        df = pd.DataFrame(weather_dicts)
        path = "weather_data.csv"
        df.to_csv(path, index=False)
        return path
