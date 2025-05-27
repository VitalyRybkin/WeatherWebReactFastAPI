"""
Module. Settings pydantic models.
"""

from typing import Annotated, Dict

from annotated_types import MaxLen
from pydantic import BaseModel, ConfigDict


class Settings(BaseModel):
    """
    Class. Base user settings pydantic model.
    Attributes
    acc_id: int
        user account id
    """

    acc_id: int


class WeatherSettings(BaseModel):
    """
    Class. Base weather settings pydantic model.
    Attributes
    ---------
    visibility: bool
        visibility flag
    humidity: bool
        humidity flag
    """

    visibility: bool
    humidity: bool


class FavoriteLocation(BaseModel):
    """
    Class. Pydentic model for user location information.
    Attributes
    ---------
    loc_id: int
        location id
    loc_name: Annotated[str, MaxLen(100)]
        location name
    loc_region: Annotated[str, MaxLen(100)]
        location region
    loc_country: Annotated[str, MaxLen(100)]
        location country
    """

    model_config = ConfigDict()
    loc_id: int
    loc_name: Annotated[str, MaxLen(100)]
    loc_region: Annotated[str, MaxLen(100)]
    loc_country: Annotated[str, MaxLen(100)]


class HourlySettings(WeatherSettings):
    """
    Class. Hourly weather settings pydantic model.
    Attributes
    ---------
    wind_extended: bool
        wind extended flag
    pressure: bool
        pressure flag
    """

    model_config = ConfigDict()
    wind_extended: bool
    pressure: bool


class CurrentSettings(WeatherSettings):
    """
    Class. Current weather settings pydantic model.
    Attributes
    ---------
    wind_extended: bool
        wind extended flag
    pressure: bool
        pressure flag
    """

    model_config = ConfigDict()

    wind_extended: bool
    pressure: bool


class DailySettings(WeatherSettings):
    """
    Class. Daily weather settings pydantic model.
    Attributes
    ---------
    astro: bool
        astro flag
    """

    model_config = ConfigDict()

    astro: bool


class UserSettings(BaseModel):
    """
    Class. User settings pydantic model.
    Attributes
    ---------
    current: bool = True
        current weather display flag
    daily: int = 3
        daily weather display flag
    hourly: int = 8
        hourly weather display flag
    units: str = "F"
        units setting value
    dark_theme: bool = False
        dark_theme setting flag
    alerts: bool = False
        alerts setting flag
    notifications: Dict[int, str] = {}
        notifications schedule
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    current: bool = True
    daily: int = 3
    hourly: int = 8
    units: str = "F"
    dark_theme: bool = False
    alerts: bool = False
    notifications: Dict[int, str] = {}


class LocationPublic(BaseModel):
    """
    Pydentic model for user location public information.
    Attributes
    ---------
    id: int
        location id
    name: Annotated[str, MaxLen(100)]
        location name
    region: Annotated[str, MaxLen(100)]
        location region
    country: Annotated[str, MaxLen(100)]
        location country
    """

    model_config = ConfigDict()
    id: int
    name: Annotated[str, MaxLen(100)]
    region: Annotated[str, MaxLen(100)]
    country: Annotated[str, MaxLen(100)]


class SettingsPublic(BaseModel):
    """
    Class. Pydantic model for public user settings.
    Attributes
    ---------
    settings: UserSettings
        user settings pydantic model
    current: CurrentSettings
        current weather settings pydentic model
    daily: DailySettings
        daily weather settings pydantic model
    hourly: HourlySettings
        hourly weather settings pydantic model
    """

    settings: UserSettings
    current: CurrentSettings
    daily: DailySettings
    hourly: HourlySettings
