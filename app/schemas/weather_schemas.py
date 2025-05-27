"""
Module. Weather pydantic models.
"""

from typing import Set, List

from pydantic import BaseModel, ConfigDict

from app.schemas.setting_schemas import (
    CurrentSettings,
    DailySettings,
    HourlySettings,
)


class Location(BaseModel):
    """
    Class. Location basic info pydantic model.
    Attributes
    ----------
    name: str
        location name
    region: str
        location region
    country: str
        location country
    lat: float
        location latitude
    lon: float
        location longitude
    tz_id: str
        location timezone
    localtime_epoch: int
        location timezone
    localtime: str
        location local time
    """

    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str


class Conditions(BaseModel):
    """
    Class. Weather conditions pydantic model.
    Attributes
    --------
    text: str
        weather condition text info
    icon: str
        weather condition icon url
    """

    text: str
    icon: str


class WeatherBase(BaseModel):
    """
    Class. Weather base pydantic model.
    Attributes
    --------
    last_updated: str
        last updated time
    condition: Conditions
        condition pydantic model
    humidity: int
        humidity value
    cloud: int
        cloud coverage value
    wind_dir: str
        wind direction
    """

    last_updated: str
    condition: Conditions
    humidity: int
    cloud: int
    wind_dir: str


class WeatherInfoBritish(BaseModel):
    """
    Class. Weather info british (Fahrenheit) units pydantic model.
    Attributes
    ----------
    temp_f: float | None = None
        location temperature value
    wind_mph: float | None = None
        location wind speed
    pressure_in: float | None = None
        location pressure
    precip_in: float | None = None
        location precipitation
    feelslike_f: float | None = None
        location feelslike temperature
    windchill_f: float | None = None
        location windchill temperature
    vis_miles: float | None = None
        location visibility miles
    gust_mph: float | None = None
        location wind gust
    """

    temp_f: float | None = None
    wind_mph: float | None = None
    pressure_in: float | None = None
    precip_in: float | None = None
    feelslike_f: float | None = None
    windchill_f: float | None = None
    vis_miles: float | None = None
    gust_mph: float | None = None


class WeatherInfoMetric(BaseModel):
    """
    Class. Weather info metric (Celsius) units pydantic model.
    Attributes
    ----------
    temp_c: float | None = None
        location temperature value
    wind_kph: float | None = None
        location wind speed
    pressure_mb: float | None = None
        location pressure
    precip_mm: float | None = None
        location precipitation
    feelslike_c: float | None = None
        location feelslike temperature
    windchill_c: float | None = None
        location windchill temperature
    vis_km: float | None = None
        location visibility miles
    gust_kph: float | None = None
        location wind gust
    """

    temp_c: float | None = None
    wind_kph: float | None = None
    pressure_mb: int | None = None
    precip_mm: float | None = None
    feelslike_c: float | None = None
    windchill_c: float | None = None
    vis_km: float | None = None
    gust_kph: float | None = None


class CurrentWeatherBritish(WeatherBase, WeatherInfoBritish):
    """
    Class. Current weather british pydantic model.
    """

    model_config = ConfigDict()


class CurrentWeatherMetric(WeatherBase, WeatherInfoMetric):
    """
    Class. Current weather metric pydantic model.
    """

    model_config = ConfigDict()


class CurrentWeatherPublic(CurrentWeatherMetric, WeatherInfoBritish):
    """
    Class. Current weather public pydantic model.
    """

    model_config = ConfigDict()


class DailyBase(BaseModel):
    """
    Class. Daily weather base pydantic model.
    Attributes
    --------
    avghumidity: int | None = None
        location average humidity value
    daily_will_it_rain: int
        daily chance of rain
    daily_chance_of_rain: int
        daily chance of rain
    daily_will_it_snow: int
        daily chance of snow
    daily_chance_of_snow: int
        daily chance of snow
    condition: Conditions
        condition pydantic model
    """

    avghumidity: int | None = None
    daily_will_it_rain: int
    daily_chance_of_rain: int
    daily_will_it_snow: int
    daily_chance_of_snow: int
    condition: Conditions


class DailyWeatherBritish(DailyBase):
    """
    Class. Daily weather pydantic british model.
    Attributes
    ---------
    maxtemp_f: float | None = None
        location max temperature value
    mintemp_f: float | None = None
        location min temperature value
    avgtemp_f: float | None = None
        location average temperature value
    maxwind_mph: float | None = None
        location max wind speed
    totalprecip_in: float | None = None
        location total precipitation
    avgvis_miles: float | None = None
        location average visibility
    """

    model_config = ConfigDict()
    maxtemp_f: float | None = None
    mintemp_f: float | None = None
    avgtemp_f: float | None = None
    maxwind_mph: float | None = None
    totalprecip_in: float | None = None
    avgvis_miles: float | None = None


class DailyWeatherMetric(DailyBase):
    """
    Class. Daily weather pydantic metric model.
    Attributes
    ---------
    maxtemp_c: float | None = None
        location max temperature value
    mintemp_c: float | None = None
        location min temperature value
    avgtemp_c: float | None = None
        location average temperature value
    maxwind_kph: float | None = None
        location max wind speed
    totalprecip_mm: float | None = None
        location total precipitation
    avgvis_km: float | None = None
        location average visibility
    """

    model_config = ConfigDict()
    maxtemp_c: float | None = None
    mintemp_c: float | None = None
    avgtemp_c: float | None = None
    maxwind_kph: float | None = None
    totalprecip_mm: float | None = None
    avgvis_km: float | None = None


class Astro(BaseModel):
    """
    Class. Astro weather pydantic model.
    Attributes
    ---------
    sunrise: str
        location sunrise time
    sunset: str
        location sunset time
    moonrise: str
        location moon rise time
    moonset: str
        location moon set time
    moon_phase: str
        location moon phase
    """

    model_config = ConfigDict()
    sunrise: str
    sunset: str
    moonrise: str
    moonset: str
    moon_phase: str


class DailyWeatherPublic(DailyWeatherBritish, DailyWeatherMetric):
    """
    Class. Daily weather pydantic public model.
    """

    model_config = ConfigDict()


class DailyForecastPublic(BaseModel):
    """
    Class. Daily forecast public model.
    Attributes
    ---------
    date: str
        date of forecast
    day: DailyWeatherPublic
        daily forecast pydentic model
    astro: Astro | None = None
        astro pydentic model
    """

    model_config = ConfigDict()
    date: str
    day: DailyWeatherPublic
    astro: Astro | None = None


class DailyWeather(BaseModel):
    """
    Class. Daily weather pydantic model.
    Attributes
    ---------
    date: str
        date of forecast
    day: DailyWeatherPublic
        daily forecast pydentic model
    astro: Astro | None = None
        astro pydentic model
    """

    model_config = ConfigDict()
    date: str
    day: DailyWeatherPublic
    astro: Astro


class HourlyBase(BaseModel):
    """
    Class. Hourly weather base pydantic model.
    Attributes
    ---------
    time: str
        time of forecast
    condition: Conditions
        condition pydantic model
    wind_dir: str
        location wind direction
    humidity: int | None = None
        location humidity
    cloud: int
        location cloud coverage
    will_it_rain: int
        daily chance of rain
    chance_of_rain: int
        daily chance of rain
    will_it_snow: int
        daily chance of snow
    chance_of_snow: int
        condition: Conditions

    """

    time: str
    condition: Conditions
    wind_dir: str
    humidity: int | None = None
    cloud: int
    will_it_rain: int
    chance_of_rain: int
    will_it_snow: int
    chance_of_snow: int


class HourlyWeatherMetric(HourlyBase, WeatherInfoMetric):
    """
    Class. Hourly weather metric pydantic model.
    """

    model_config = ConfigDict()


class HourlyWeatherBritish(HourlyBase, WeatherInfoBritish):
    """
    Class. Hourly weather metric pydantic model.
    """

    model_config = ConfigDict()


class HourlyForecastPublic(HourlyBase, WeatherInfoMetric, WeatherInfoBritish):
    """
    Class. Hourly forecast public pydantic model.
    """

    model_config = ConfigDict()


class Forecast(BaseModel):
    """
    Class. Forecast pydantic model.
    Attributes
    ---------
    forecastday: List[DailyForecastPublic]
        list of daily forecast pydentic model
    forecasthour: List[HourlyForecastPublic]
        list of hourly forecast pydentic model
    """

    model_config = ConfigDict()
    forecastday: List[DailyForecastPublic]
    forecasthour: List[HourlyForecastPublic]


class Alerts(BaseModel):
    """
    Class. Alerts pydantic model.
    """

    model_config = ConfigDict(extra="allow")


class ForecastPublic(BaseModel):
    """
    Class. Public forecast pydantic model.
    Attributes
    ---------
    location: Location
        location info pydantic model
    current: CurrentWeatherPublic
        current weather info pydentic model
    forecast: Forecast
        forecast pydentic model
    alerts: Alerts
        alert pydentic model
    """

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
