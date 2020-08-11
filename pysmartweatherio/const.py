"""Constant Definitions for SmartWeather."""

BASE_URL = "https://swd.weatherflow.com/swd/rest"

DEFAULT_TIMEOUT = 10

UNIT_TYPE_TEMP = "temperature"
UNIT_TYPE_WIND = "wind"
UNIT_TYPE_RAIN = "rain"
UNIT_TYPE_PRESSURE = "pressure"
UNIT_TYPE_DISTANCE = "distance"

UNIT_SYSTEM_METRIC = "metric"
UNIT_SYSTEM_IMPERIAL = "imperial"
UNIT_TEMP_CELCIUS = "c"
UNIT_TEMP_FAHRENHEIT = "f"
UNIT_PRESSURE_HPA = "hpa"
UNIT_PRESSURE_MB = "mb"
UNIT_PRESSURE_INHG = "inhg"
UNIT_PRECIP_MM = "mm"
UNIT_PRECIP_IN = "in" 
UNIT_WIND_MS = "mps"
UNIT_WIND_KMH = "kmh"
UNIT_WIND_MPH = "mph"
UNIT_DISTANCE_KM = "km"
UNIT_DISTANCE_MI = "mi"

FORECAST_TYPE_DAILY = "daily"
FORECAST_TYPE_HOURLY = "hourly"

FORECAST_TYPES = [
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
]
