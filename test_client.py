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
            _LOGGER.info("\n" +
                "AIR DENSITY: " + str(row.air_density) + "\n" +
                "TEMPERATURE: " + str(row.air_temperature) + "\n" +
                "BRIGHTNESS: " + str(row.brightness) + "\n" +
                "DEW POINT: " + str(row.dew_point) + "\n" +
                "FEELS LIKE: " + str(row.feels_like) + "\n" +
                "FREEZING: " + str(row.freezing) + "\n" +
                "HEAT INDEX: " + str(row.heat_index) + "\n" +
                "LIGHTNING: " + str(row.lightning) + "\n" +
                "LIGHTNING TIME: " + row.lightning_strike_last_time + "\n" +
                "LIGHTNING DISTANCE: " + str(row.lightning_strike_last_distance) + "\n" +
                "LIGHTNING COUNT: " + str(row.lightning_strike_count) + "\n" +
                "LIGHTNING COUNT 3 HOURS: " + str(row.lightning_strike_count_last_3hr) + "\n" +
                "RAIN LAST HOUR: " + str(row.precip_accum_last_1hr) + "\n" +
                "RAIN TODAY: " + str(row.precip_accum_local_day) + "\n" +
                "RAIN YESTERDAY: " + str(row.precip_accum_local_yesterday) + "\n" +
                "RAIN RATE: " + str(row.precip_rate) + "\n" +
                "RAIN MINUTES TODAY: " + str(row.precip_minutes_local_day) + "\n" +
                "RAIN MINUTES YESTERDAY: " + str(row.precip_minutes_local_yesterday) + "\n" +
                "HUMIDITY: " + str(row.relative_humidity) + "\n" +
                "RAINING: " + str(row.raining) + "\n" +
                "SOLAR RADIATION: " + str(row.solar_radiation) + "\n" +
                "STATION PRESSURE: " + str(row.station_pressure) + "\n" +
                "TIMESTAMP: " + row.timestamp + "\n" +
                "UV: " + str(row.uv) + "\n" +
                "WIND AVG: " + str(row.wind_avg) + "\n" +
                "WIND BEARING: " + str(row.wind_bearing) + "\n" +
                "WIND CHILL: " + str(row.wind_chill) + "\n" +
                "WIND GUST: " + str(row.wind_gust) + "\n" +
                "WIND DIRECTION: " + str(row.wind_direction)
            )

    except SmartWeatherError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.run(main())