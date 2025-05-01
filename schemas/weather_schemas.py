from typing import Dict, Set, Any, List

from pydantic import BaseModel, ConfigDict

from schemas.setting_schemas import (
    CurrentSettings,
    DailySettings,
    HourlySettings,
)


class Location(BaseModel):
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


class Conditions(BaseModel):
    text: str
    icon: str


class WeatherBase(BaseModel):
    last_updated: str
    condition: Conditions
    humidity: int
    cloud: int
    wind_dir: str


class WeatherInfoBritish(BaseModel):
    temp_f: float
    wind_mph: float
    pressure_in: float
    precip_in: float
    feelslike_f: float
    windchill_f: float
    vis_miles: float
    gust_mph: float


class WeatherInfoMetric(BaseModel):
    temp_c: float
    wind_kph: float
    pressure_mb: int
    precip_mm: float
    feelslike_c: float
    windchill_c: float
    vis_km: float
    gust_kph: float


class CurrentWeatherBritish(WeatherBase, WeatherInfoBritish):
    model_config = ConfigDict()


class CurrentWeatherMetric(WeatherBase, WeatherInfoMetric):
    model_config = ConfigDict()


class CurrentWeatherPublic(BaseModel):
    model_config = ConfigDict()
    last_updated: str
    condition: Conditions
    humidity: int | None = None
    cloud: int | None = None
    wind_dir: str | None = None
    temp_f: float | None = None
    temp_c: float | None = None
    wind_mph: float | None = None
    wind_kph: float | None = None
    pressure_in: float | None = None
    pressure_mb: int | None = None
    precip_in: float | None = None
    precip_mm: float | None = None
    feelslike_f: float | None = None
    feelslike_c: float | None = None
    windchill_f: float | None = None
    windchill_c: float | None = None
    vis_miles: float | None = None
    vis_km: float | None = None
    gust_mph: float | None = None
    gust_kph: float | None = None


class DailyBase(BaseModel):
    avghumidity: int
    daily_will_it_rain: int
    daily_chance_of_rain: int
    daily_will_it_snow: int
    daily_chance_of_snow: int
    condition: Conditions


class DailyWeatherBritish(DailyBase):
    model_config = ConfigDict()
    maxtemp_f: float
    mintemp_f: float
    avgtemp_f: float
    maxwind_mph: float
    totalprecip_in: float
    avgvis_miles: float


class DailyWeatherMetric(DailyBase):
    model_config = ConfigDict()
    maxtemp_c: float
    mintemp_c: float
    avgtemp_c: float
    maxwind_kph: float
    totalprecip_mm: float
    avgvis_km: float


class Astro(BaseModel):
    model_config = ConfigDict()
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str


class DailyWeatherPublic(BaseModel):
    model_config = ConfigDict()
    maxtemp_c: float | None = None
    maxtemp_f: float | None = None
    mintemp_c: float | None = None
    mintemp_f: float | None = None
    avgtemp_c: float | None = None
    avgtemp_f: float | None = None
    maxwind_mph: float | None = None
    maxwind_kph: float | None = None
    totalprecip_mm: float | None = None
    totalprecip_in: float | None = None
    avgvis_km: float | None = None
    avgvis_miles: float | None = None
    avghumidity: int | None = None
    daily_will_it_rain: int | None = None
    daily_chance_of_rain: int | None = None
    daily_will_it_snow: int | None = None
    daily_chance_of_snow: int | None = None
    condition: Conditions | None = None


class DailyForecastPublic(BaseModel):
    model_config = ConfigDict()
    date: str
    day: DailyWeatherPublic
    astro: Astro | None = None


class DailyWeather(BaseModel):
    model_config = ConfigDict()
    date: str
    day: DailyWeatherPublic
    astro: Astro


class HourlyBase(BaseModel):
    time: str
    condition: Conditions
    wind_dir: str
    humidity: int
    cloud: int
    will_it_rain: int
    chance_of_rain: int
    will_it_snow: int
    chance_of_snow: int


class HourlyWeatherMetric(HourlyBase, WeatherInfoMetric):
    model_config = ConfigDict()


class HourlyWeatherBritish(HourlyBase, WeatherInfoBritish):
    model_config = ConfigDict()


class HourlyForecastPublic(BaseModel):
    model_config = ConfigDict()
    time: str
    condition: Conditions
    wind_dir: str | None = None
    humidity: int | None = None
    cloud: int | None = None
    will_it_rain: int | None = None
    chance_of_rain: int | None = None
    will_it_snow: int | None = None
    chance_of_snow: int | None = None
    temp_c: float | None = None
    temp_f: float | None = None
    wind_kph: float | None = None
    wind_mph: float | None = None
    pressure_mb: int | None = None
    pressure_in: float | None = None
    precip_mm: float | None = None
    precip_in: float | None = None
    feelslike_c: float | None = None
    feelslike_f: float | None = None
    windchill_c: float | None = None
    windchill_f: float | None = None
    vis_km: float | None = None
    vis_miles: float | None = None
    gust_kph: float | None = None
    gust_mph: float | None = None


class Forecast(BaseModel):
    model_config = ConfigDict()
    forecastday: List[DailyForecastPublic]
    forecasthour: List[HourlyForecastPublic]


class Alerts(BaseModel):
    model_config = ConfigDict(extra="allow")


class ForecastPublic(BaseModel):
    model_config = ConfigDict()
    location: Location
    current: CurrentWeatherPublic
    forecast: Forecast
    alerts: Alerts


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
