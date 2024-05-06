from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, func

from src.common.enums import WindDirection
from src.database.models import Base
from src.database.models.base.mixins import ModelWithIDMixin


class Weather(ModelWithIDMixin, Base):
    measurement_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    temperature: Mapped[float]
    wind_speed: Mapped[float]
    wind_direction: Mapped[WindDirection]
    pressure: Mapped[float]
    rain: Mapped[float]
    showers: Mapped[float]
    snowfall: Mapped[float]
    address: Mapped[str]
