from datetime import datetime

import plotly.graph_objects as go
from matplotlib import pyplot as plt

from src.interfaces.draw_plots import AbstractPlotterAdapter


class PlotlyPlotterAdapter(AbstractPlotterAdapter):
    """Adapter for plotting weather data using Plotly."""

    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        """Draw a plot of the weather data."""
        # Plot the data
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days, y=temperatures, mode="lines+markers"))
        fig.update_layout(
            title="Temperature Over Time",
            xaxis_title="Date",
            yaxis_title="Temperature (°C)",
            template="plotly_dark",
        )
        fig.show()


class MatplotlibPlotterAdapter(AbstractPlotterAdapter):
    """Adapter for plotting weather data using Matplotlib."""

    async def draw(self, days: list[datetime], temperatures: list[float]) -> None:
        """Draw a plot of the weather data."""
        # Plot the data
        fig, ax = plt.subplots(figsize=(10, 10))
        ax.plot(days, temperatures, marker="o", linestyle="-", color="b")
        ax.set_title("Temperature Over Time")
        ax.set_xlabel("Date")
        ax.set_ylabel("Temperature (°C)")
        ax.grid(True)
        plt.show()
