import os
import pathlib
from functools import lru_cache


class BaseConfig:
    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent

    DATABASE_URL: str = os.environ.get(
        "DATABASE_URL", f"sqlite+aiosqlite:///{BASE_DIR}/db.sqlite3"
    )


class DevelopmentConfig(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    pass


class TestingConfig(BaseConfig):
    pass


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig,
    }
    config_name = os.environ.get("WEATHER_PROJECT_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


# Number of requests per hour
REQUESTS_PER_HOUR = 20

# Open-Meteo API
OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={latitude}"
    "&longitude={longitude}&current=temperature_2m,"
    "precipitation,rain,showers,snowfall,surface_pressure,wind_speed_10m,"
    "wind_direction_10m&wind_speed_unit=ms"
)


settings = get_settings()
