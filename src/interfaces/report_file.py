from abc import ABC, abstractmethod

from src.common.dto.weather import WeatherReportDTO


class AbstractReportFileAdapter(ABC):
    @abstractmethod
    def create_report_file(self, weather_data: list[WeatherReportDTO]) -> None:
        pass
