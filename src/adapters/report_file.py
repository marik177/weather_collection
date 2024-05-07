from src.common.dto.weather import WeatherReportDTO
from src.interfaces.report_file import AbstractReportFileAdapter
import pandas as pd


class XLSXReportFileAdapter(AbstractReportFileAdapter):
    def create_report_file(self, weather_data: list[WeatherReportDTO]) -> None:
        weather_dicts = [weather.model_dump() for weather in weather_data]
        df = pd.DataFrame(weather_dicts)
        with pd.ExcelWriter("weather_data.xlsx") as writer:
            df.to_excel(writer, index=False, sheet_name="Weather Data")


class CSVReportFileAdapter(AbstractReportFileAdapter):
    def create_report_file(self, weather_data: list[WeatherReportDTO]) -> None:
        weather_dicts = [weather.model_dump() for weather in weather_data]
        df = pd.DataFrame(weather_dicts)
        df.to_csv("weather_data.csv", index=False)
