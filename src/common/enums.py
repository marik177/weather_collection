from enum import Enum


class WindDirection(str, Enum):
    NORTH = "С"
    NORTH_EAST = "СВ"
    EAST = "В"
    SOUTH_EAST = "ЮВ"
    SOUTH = "Ю"
    SOUTH_WEST = "ЮВ"
    WEST = "З"
    NORTH_WEST = "СЗ"
