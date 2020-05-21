""" The test for the API """
"""Run an example script to quickly test."""
import asyncio
import logging
import time
import json

from pysmartweatherio import (
    SmartWeather,
    SmartWeatherError,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_WIND_MS,
    UNIT_WIND_KMH,
    UNIT_WIND_MPH,
)

_LOGGER = logging.getLogger(__name__)


API_KEY = "20c70eae-e62f-4d3b-b3a4-8586e90f3ac8"
STATION_ID = 2777
TO_UNITS = UNIT_SYSTEM_METRIC
TO_WIND_UNIT = UNIT_WIND_MS # Will be ignored if UNITS = Imperial

async def main() -> None:
    """Create the aiohttp session and run the example."""
    logging.basicConfig(level=logging.DEBUG)

    smartweather = SmartWeather(API_KEY,STATION_ID, TO_UNITS, TO_WIND_UNIT)

    start = time.time()

    try:
        # _LOGGER.info("GETTING STATION NAME:")
        # station_name = await smartweather.get_station_name()
        # _LOGGER.info(f"STATION: {station_name}")

        _LOGGER.info("GETTING STATION DATA:")
        data = await smartweather.get_station_data()
        for row in data:
            _LOGGER.info(f"{row.timestamp} - {row.air_temperature} - {row.station_pressure} - {row.wind_avg} - {row.precip_rate} - {row.relative_humidity}% - {row.wind_direction} - {row.lightning_strike_last_time}")

        # _LOGGER.info("GETTING CURRENT DATA:")
        # data = await wbit.async_get_current_data()
        # for row in data:
        #     _LOGGER.info(f"{row.datetime} - {row.sunrise} - {row.sunset} - {row.is_night}")

        # _LOGGER.info("GETTING DAILY FORECAST DATA:")
        # data = await wbit.async_get_forecast_daily()
        # for row in data:
        #     _LOGGER.info(f"{row.city_name} - {row.valid_date} - {row.weather_text} - {row.max_temp}")

        # NOTE: Unmark if you have a paid API Key
        # _LOGGER.info("GETTING HOURLY FORECAST DATA:")
        # data = await wbit.async_get_forecast_hourly()
        # for row in data:
        #     _LOGGER.info(f"{row.city_name} - {row.timestamp} - {row.weather_text} - {row.temp}")

        # _LOGGER.info("GETTING WEATHER ALERTS:")
        # data = await wbit.async_get_weather_alerts()
        # for row in data:
        #     _LOGGER.info(f"{row.city_name} - {row.title}")

    except SmartWeatherError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.run(main())