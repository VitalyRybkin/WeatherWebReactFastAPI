from typing import Dict, Set, Any

from pydantic import BaseModel, ConfigDict

from utils.setting_schemas import CurrentSettings, DailySettings, HourlySettings


class CurrentInfo(BaseModel):
    last_updated: str
    condition: Dict[str, str]
    humidity: int
    cloud: int
    wind_dir: str


class CurrentWeatherBritish(CurrentInfo):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    temp_f: float
    wind_mph: float
    pressure_in: float
    precip_in: float
    feelslike_f: float
    windchill_f: float
    vis_miles: float
    gust_mph: float


class CurrentWeatherMetric(CurrentInfo):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    temp_c: float
    wind_kph: float
    pressure_mb: int
    precip_mm: float
    feelslike_c: float
    windchill_c: float
    vis_km: float
    gust_kph: float


class DailyBase(BaseModel):
    avghumidity: int
    daily_will_it_rain: int
    daily_chance_of_rain: int
    daily_will_it_snow: int
    daily_chance_of_snow: int
    condition: Dict[str, str]


class DailyWeatherBritish(DailyBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    maxtemp_f: float
    mintemp_f: float
    avgtemp_f: float
    maxwind_mph: float
    totalprecip_in: float
    avgvis_miles: float


class DailyWeatherMetric(DailyBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    maxtemp_c: float
    mintemp_c: float
    avgtemp_c: float
    maxwind_kph: float
    totalprecip_mm: float
    avgvis_km: float


class Astro(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str


class DailyWeather(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    date: str
    day: Dict[str, Any]
    astro: Astro


class HourlyBase(BaseModel):
    time: str
    condition: Dict[str, str]
    wind_dir: str
    humidity: int
    cloud: int
    will_it_rain: int
    chance_of_rain: int
    will_it_snow: int
    chance_of_snow: int


class HourlyWeatherMetric(HourlyBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    temp_c: float
    wind_kph: float
    pressure_mb: int
    precip_mm: int
    feelslike_c: float
    windchill_c: float
    vis_km: int
    gust_kph: float


class HourlyWeatherBritish(HourlyBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    temp_f: float
    wind_mph: float
    pressure_in: float
    precip_in: int
    feelslike_f: float
    windchill_f: float
    vis_miles: int
    gust_mph: float


def exclude_fields(
    current: CurrentSettings = None,
    daily: DailySettings = None,
    hourly: HourlySettings = None,
) -> Set[str]:
    """
    Function: Set of excluded fields from validation using user settings
    :param current: current user settings
    :param daily: daily user settings
    :param hourly: hourly user settings
    :return: Set of excluded fields
    """
    excluded_fields: Set[str] = set()

    if current:
        if not current.pressure:
            excluded_fields.update({"pressure_mb", "pressure_in"})
        if not current.wind_extended:
            excluded_fields.update(
                {"gust_mph", "gust_kph", "windchill_c", "windchill_f"}
            )
        if not current.humidity:
            excluded_fields.update({"humidity"})
        if not current.visibility:
            excluded_fields.update({"vis_km", "vis_miles"})

    if daily:
        if not daily.visibility:
            excluded_fields.update({"avgvis_miles", "avgvis_km"})
        if not daily.humidity:
            excluded_fields.update({"avghumidity"})
        if not daily.wind_extended:
            excluded_fields.update({"maxwind_mph", "maxwind_kph"})
        if not daily.astro:
            excluded_fields.update({"astro"})

    if hourly:
        if not hourly.visibility:
            excluded_fields.update({"vis_km", "vis_miles"})
        if not hourly.humidity:
            excluded_fields.update({"humidity"})
        if not hourly.wind_extended:
            excluded_fields.update(
                {"windchill_c", "windchill_f", "gust_mph", "gust_kph"}
            )
        if not hourly.pressure:
            excluded_fields.update({"pressure_mb", "pressure_in"})

    return excluded_fields
