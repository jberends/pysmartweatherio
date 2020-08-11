"""Define a client to interact with Weatherflow SmartWeather."""
import asyncio
import logging
from typing import Optional
from datetime import datetime

from aiohttp import ClientSession, ClientTimeout
from aiohttp.client_exceptions import ClientError

from pysmartweatherio.errors import InvalidApiKey, RequestError, ResultError
from pysmartweatherio.helper_functions import ConversionFunctions
from pysmartweatherio.dataclasses import StationData, ForecastData
from pysmartweatherio.const import (
    BASE_URL,
    DEFAULT_TIMEOUT,
    UNIT_SYSTEM_METRIC,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_TEMP_CELCIUS,
    UNIT_TEMP_FAHRENHEIT,
    UNIT_PRESSURE_HPA,
    UNIT_PRESSURE_INHG,
    UNIT_PRECIP_IN,
    UNIT_PRECIP_MM,
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
    UNIT_DISTANCE_KM,
    UNIT_DISTANCE_MI,
    UNIT_TYPE_TEMP,
    UNIT_TYPE_WIND,
    UNIT_TYPE_RAIN,
    UNIT_TYPE_PRESSURE,
    UNIT_TYPE_DISTANCE,
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
)

_LOGGER = logging.getLogger(__name__)


class SmartWeather:
    """SmartWeather Communication Client."""

    def __init__(
        self,
        api_key: str,
        station_id: int,
        to_units: str = UNIT_SYSTEM_METRIC,
        to_wind_unit: str = UNIT_WIND_MS,
        session: Optional[ClientSession] = None,
        ):
        self._api_key = api_key
        self._station_id = station_id
        self._to_units = to_units
        self._to_wind_unit = to_wind_unit
        self._session: ClientSession = session
        self.req = session
        self._latitude = None
        self._longitude = None

        if self._to_units == UNIT_SYSTEM_METRIC:
            self._to_units_temp = UNIT_TEMP_CELCIUS
            self._to_units_pressure = UNIT_PRESSURE_HPA
            self._to_units_wind = UNIT_WIND_MS
            if self._to_wind_unit == UNIT_WIND_KMH:
                self._to_units_wind = UNIT_WIND_KMH
            self._to_units_precip = UNIT_PRECIP_MM
            self._to_units_distance = UNIT_DISTANCE_KM
        else:
            self._to_units_temp = UNIT_TEMP_FAHRENHEIT
            self._to_units_pressure = UNIT_PRESSURE_INHG
            self._to_units_wind = UNIT_WIND_MPH
            self._to_units_precip = UNIT_PRECIP_IN
            self._to_units_distance = UNIT_DISTANCE_MI

    async def get_station_name(self) -> None:
        """Returns the Station Name."""
        return await self._station_name_by_station_id()

    async def get_station_data(self) -> None:
        """Returns current sensor data."""
        return await self._current_station_data()

    async def get_station_hardware(self) -> None:
        """Returns station hardware data."""
        return await self._station_information()

    async def get_forecast(self, forecast_type=FORECAST_TYPE_DAILY) -> None:
        """Returns station Weather Forecast."""
        return await self._forecast_data(forecast_type)

    async def get_units(self) -> None:
        """Returns the units used for Values."""
        if self._to_units == UNIT_SYSTEM_METRIC:
            unit_temp = "°C"
            unit_wind = "m/s"
            if self._to_units_wind == UNIT_WIND_KMH:
                unit_wind = "km/h"
            unit_rain = "mm"
            unit_pressure = "hPa"
            unit_distance = "km"
        else:
            unit_temp = "°F"
            unit_wind = "mi/h"
            unit_rain = "in"
            unit_pressure = "inHg"
            unit_distance = "mi"

        units = {
            UNIT_TYPE_TEMP: unit_temp,
            UNIT_TYPE_WIND: unit_wind,
            UNIT_TYPE_RAIN: unit_rain,
            UNIT_TYPE_PRESSURE: unit_pressure,
            UNIT_TYPE_DISTANCE: unit_distance,
        }
        return units

    async def _station_information(self) -> None:
        """Return Information about the station HW."""
        endpoint = f"stations/{self._station_id}?api_key={self._api_key}"
        json_data = await self.async_request("get", endpoint)
        
        for row in json_data["stations"]:
            items = {}
            name = row["name"]
            self._latitude = row["latitude"]
            self._longitude = row["longitude"]
            for item in row["devices"]:
                if "device_type" in item:
                    if item["device_type"] == "HB":
                        items = {
                            "station_name": name,
                            "latitude": self._latitude,
                            "longitude": self._longitude,
                            "station_type": "AIR & SKY",
                            "serial_number": item["serial_number"],
                            "device_id": item["device_id"],
                            "firmware_revision": item["firmware_revision"],
                            "hardware_revision": item["hardware_revision"],
                        }
                    if item["device_type"] == "ST":
                        items = {
                            "station_name": name,
                            "latitude": self._latitude,
                            "longitude": self._longitude,
                            "station_type": "Tempest",
                            "serial_number": item["serial_number"],
                            "device_id": item["device_id"],
                            "firmware_revision": item["firmware_revision"],
                            "hardware_revision": item["hardware_revision"],
                        }
                        break

            if items:
                return items


    async def _station_name_by_station_id(self) -> None:
        """Return Station name from the Station ID."""
        endpoint = f"observations/station/{self._station_id}?api_key={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        return self._station_id if json_data.get("station_name") is None else json_data.get("station_name")

    async def _current_station_data(self) -> None:
        """Return current observation data for the Station."""
        endpoint = f"observations/station/{self._station_id}?api_key={self._api_key}"
        json_data = await self.async_request("get", endpoint)

        row = json_data.get("station_units")
        if row is not None:
            from_units_temp = row["units_temp"]
            from_units_wind = row["units_wind"]
            from_units_precip = row["units_precip"]
            from_units_pressure = row["units_pressure"]
            from_units_distance = row["units_distance"]
            from_units_direction = row["units_direction"]
            from_units_other = row["units_other"]

        station_name = json_data.get("station_name")

        cnv = ConversionFunctions()
        items = []
        observations = json_data.get("obs")
        if observations is None:
            observations = {"nodata": "NoData"}
        
        for row in observations:
            item = {
                "air_density": 0 if "air_density" not in row else row["air_density"],
                "air_temperature": 0 if "air_temperature" not in row else
                await cnv.temperature(row["air_temperature"], from_units_temp, self._to_units_temp),
                "brightness": 0 if "brightness" not in row else row["brightness"],
                "dew_point": 0 if "dew_point" not in row else
                await cnv.temperature(row["dew_point"], from_units_temp, self._to_units_temp),
                "feels_like": 0 if "feels_like" not in row else
                await cnv.temperature(row["feels_like"], from_units_temp, self._to_units_temp),
                "heat_index": 0 if "heat_index" not in row else
                await cnv.temperature(row["heat_index"], from_units_temp, self._to_units_temp),
                "lightning_strike_last_time": None if "lightning_strike_last_epoch" not in row else
                await cnv.epoch_to_datetime(row["lightning_strike_last_epoch"]),
                "lightning_strike_last_distance": 0 if "lightning_strike_last_distance" not in row else
                await cnv.distance(row["lightning_strike_last_distance"], from_units_distance, self._to_units_distance),
                "lightning_strike_count": 0 if "lightning_strike_count" not in row else row["lightning_strike_count"],
                "lightning_strike_count_last_3hr": 0 if "lightning_strike_count_last_3hr" not in row else row["lightning_strike_count_last_3hr"],
                "precip_accum_last_1hr": 0 if "precip_accum_last_1hr" not in row else
                await cnv.precip(row["precip_accum_last_1hr"], from_units_precip, self._to_units_precip),
                "precip_accum_local_day": 0 if "precip_accum_local_day" not in row else
                await cnv.precip(row["precip_accum_local_day"], from_units_precip, self._to_units_precip),
                "precip_accum_local_yesterday": 0 if "precip_accum_local_yesterday" not in row else
                await cnv.precip(row["precip_accum_local_yesterday"], from_units_precip, self._to_units_precip),
                "precip_rate": 0 if "precip" not in row else
                await cnv.precip(row["precip"], from_units_precip, self._to_units_precip) * 60,
                "precip_minutes_local_day": 0 if "precip_minutes_local_day" not in row else row["precip_minutes_local_day"],
                "precip_minutes_local_yesterday": 0 if "precip_minutes_local_yesterday" not in row else row["precip_minutes_local_yesterday"],
                "relative_humidity": 0 if "relative_humidity" not in row else row["relative_humidity"],
                "station_pressure": 0 if "station_pressure" not in row else
                await cnv.pressure(row["station_pressure"], from_units_pressure, self._to_units_pressure),
                "station_name": station_name,
                "solar_radiation": 0 if "solar_radiation" not in row else row["solar_radiation"],
                "timestamp": None if "timestamp" not in row else
                await cnv.epoch_to_datetime(row["timestamp"]),
                "uv": 0 if "uv" not in row else row["uv"],
                "wind_avg": 0 if "wind_avg" not in row else
                await cnv.wind(row["wind_avg"], from_units_wind, self._to_units_wind),
                "wind_bearing": 0 if "wind_direction" not in row else row["wind_direction"],
                "wind_chill": 0 if "wind_chill" not in row else
                await cnv.temperature(row["wind_chill"], from_units_temp, self._to_units_temp),
                "wind_gust": 0 if "wind_gust" not in row else
                await cnv.wind(row["wind_gust"], from_units_wind, self._to_units_wind),
            }
            items.append(StationData(item))

        return items

    async def _forecast_data(self, forecast_type) -> None:
        """Return Forecast data for the Station."""
        if self._latitude is None:
            # _LOGGER.debug(f"LAT: {self._latitude}")
            await self._station_information()

        cnv = ConversionFunctions()
        endpoint = f"better_forecast?station_id={self._station_id}&api_key={self._api_key}&lat={self._latitude}&lon={self._longitude}"
        json_data = await self.async_request("get", endpoint)
        items = []

        forecast = json_data.get("forecast")
        for row in forecast[forecast_type]:
            dt_object = datetime.fromtimestamp(row["day_start_local"])
            item = {
                "timestamp": dt_object,
                "conditions": row["conditions"],
                "icon": row["icon"],
                "sunrise": datetime.fromtimestamp(row["sunrise"]),
                "sunset": datetime.fromtimestamp(row["sunset"]),
                "air_temp_high": await cnv.temperature(row["air_temp_high"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "air_temp_low": await cnv.temperature(row["air_temp_low"], UNIT_TEMP_CELCIUS, self._to_units_temp),
                "air_temp_high_color": row["air_temp_high_color"],
                "air_temp_low_color": row["air_temp_low_color"],
                "precip_probability": row["precip_probability"],
                "precip_icon": row["precip_icon"],
                "precip_type": row["precip_type"],
            }
            items.append(ForecastData(item))

        return items
        
    async def async_request(self, method: str, endpoint: str) -> dict:
        """Make a request against the SmartWeather API."""

        use_running_session = self._session and not self._session.closed

        if use_running_session:
            session = self._session
        else:
            session = ClientSession(timeout=ClientTimeout(total=DEFAULT_TIMEOUT))

        try:
            async with session.request(
                method, f"{BASE_URL}/{endpoint}"
            ) as resp:
                resp.raise_for_status()
                data = await resp.json()
                return data
        except asyncio.TimeoutError:
            raise RequestError("Request to endpoint timed out: {endpoint}")
        except ClientError as err:
            if err.message == "Unauthorized":
                raise InvalidApiKey("Your API Key is invalid or does not support this operation")
            elif err.message == "Not Found":
                raise ResultError("The Station ID does not exist")
            else:
                raise RequestError(
                    f"Error requesting data from {endpoint}: {err}"
                ) from None
        finally:
            if not use_running_session:
                await session.close()
