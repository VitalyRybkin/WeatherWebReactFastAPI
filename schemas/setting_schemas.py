from typing import Annotated, List

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    acc_id: int


class WeatherSettings(BaseModel):
    visibility: bool
    humidity: bool


class FavoriteLocation(BaseModel):
    """
    Pydentic model for user location information
    """

    model_config = ConfigDict()
    loc_id: int
    loc_name: Annotated[str, MaxLen(100)]
    loc_region: Annotated[str, MaxLen(100)]
    loc_country: Annotated[str, MaxLen(100)]


class HourlySettings(WeatherSettings):
    model_config = ConfigDict()
    wind_extended: bool
    pressure: bool


class CurrentSettings(WeatherSettings):
    model_config = ConfigDict()

    wind_extended: bool
    pressure: bool


class DailySettings(WeatherSettings):
    model_config = ConfigDict()

    astro: bool


class UserSettings(BaseModel):
    model_config = ConfigDict()

    current: bool = True
    daily: int = 3
    hourly: int = 8
    units: str = "F"


class LocationPublic(BaseModel):
    """
    Pydentic model for user location information
    """

    model_config = ConfigDict()
    id: int
    name: Annotated[str, MaxLen(100)]
    region: Annotated[str, MaxLen(100)]
    country: Annotated[str, MaxLen(100)]


class SettingsPublic(BaseModel):
    settings: UserSettings
    current: CurrentSettings
    daily: DailySettings
    hourly: HourlySettings
