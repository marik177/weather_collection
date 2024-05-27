import asyncio

from src.service_layer import unit_of_work
from src.adapters.draw_plots import MatplotlibPlotterAdapter, PlotlyPlotterAdapter
from src.service_layer.unit_of_work import CSVUnitOfWork
from src.service_layer.weather_plot_service import WeatherPlotterService


async def main():
    weather_plot_service = WeatherPlotterService(
        data_source=unit_of_work.SqlAlchemyUnitOfWork(),
        plotter=PlotlyPlotterAdapter(),
    )
    # weather_plot_service = WeatherPlotterService(
    #     data_source=CSVUnitOfWork("../weather_data.csv"),
    #     plotter=MatplotlibPlotterAdapter(),
    # )

    await weather_plot_service.draw()


if __name__ == "__main__":
    asyncio.run(main())
