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
    FORECAST_TYPE_DAILY,
    FORECAST_TYPE_HOURLY,
)

_LOGGER = logging.getLogger(__name__)


API_KEY = "20c70eae-e62f-4d3b-b3a4-8586e90f3ac8"
STATION_ID = 22980 #6544
TO_UNITS = UNIT_SYSTEM_IMPERIAL
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

        # _LOGGER.info("GETTING STATION HARDWARE:")
        # data = await smartweather.get_station_hardware()
        # print(data)

        # _LOGGER.info("GETTING STATION DATA:")
        # data = await smartweather.get_station_data()
        # for row in data:
        #     _LOGGER.info("\n" +
        #         "AIR DENSITY: " + str(row.air_density) + "\n" +
        #         "TEMPERATURE: " + str(row.air_temperature) + "\n" +
        #         "BRIGHTNESS: " + str(row.brightness) + "\n" +
        #         "DEW POINT: " + str(row.dew_point) + "\n" +
        #         "FEELS LIKE: " + str(row.feels_like) + "\n" +
        #         "FREEZING: " + str(row.freezing) + "\n" +
        #         "HEAT INDEX: " + str(row.heat_index) + "\n" +
        #         "LIGHTNING: " + str(row.lightning) + "\n" +
        #         "LIGHTNING TIME: " + str(row.lightning_strike_last_time) + "\n" +
        #         "LIGHTNING DISTANCE: " + str(row.lightning_strike_last_distance) + "\n" +
        #         "LIGHTNING COUNT: " + str(row.lightning_strike_count) + "\n" +
        #         "LIGHTNING COUNT 3 HOURS: " + str(row.lightning_strike_count_last_3hr) + "\n" +
        #         "RAIN LAST HOUR: " + str(row.precip_accum_last_1hr) + "\n" +
        #         "RAIN TODAY: " + str(row.precip_accum_local_day) + "\n" +
        #         "RAIN YESTERDAY: " + str(row.precip_accum_local_yesterday) + "\n" +
        #         "RAIN RATE: " + str(row.precip_rate) + "\n" +
        #         "RAIN MINUTES TODAY: " + str(row.precip_minutes_local_day) + "\n" +
        #         "RAIN MINUTES YESTERDAY: " + str(row.precip_minutes_local_yesterday) + "\n" +
        #         "HUMIDITY: " + str(row.relative_humidity) + "\n" +
        #         "RAINING: " + str(row.raining) + "\n" +
        #         "SOLAR RADIATION: " + str(row.solar_radiation) + "\n" +
        #         "STATION PRESSURE: " + str(row.station_pressure) + "\n" +
        #         "STATION NAME: " + str(row.station_name) + "\n" +
        #         "TIMESTAMP: " + str(row.timestamp) + "\n" +
        #         "UV: " + str(row.uv) + "\n" +
        #         "WIND AVG: " + str(row.wind_avg) + "\n" +
        #         "WIND BEARING: " + str(row.wind_bearing) + "\n" +
        #         "WIND CHILL: " + str(row.wind_chill) + "\n" +
        #         "WIND GUST: " + str(row.wind_gust) + "\n" +
        #         "WIND DIRECTION: " + str(row.wind_direction)
        #     )

        _LOGGER.info("GETTING DAILY FORECAST DATA:")
        data = await smartweather.get_forecast()
        for row in data:
            _LOGGER.info("\n" +
                "TIME: " + str(row.timestamp) + "\n" +
                "CONDITIONS: " + str(row.conditions) + "\n" +
                "ICON: " + str(row.icon) + "\n" +
                "SUNRISE: " + str(row.sunrise) + "\n" +
                "SUNSET " + str(row.sunset) + "\n" +
                "TEMP HIGH: " + str(row.temp_high) + "\n" +
                "TEMP LOW: " + str(row.temp_low) + "\n" +
                "TEMP HIGH COLOR: " + str(row.temp_high_color) + "\n" +
                "TEMP LOW COLOR: " + str(row.temp_low_color) + "\n" +
                "PRECIP: " + str(row.precip) + "\n" +
                "PRECIP PROBABILITY: " + str(row.precip_probability) + "\n" +
                "PRECIP ICON: " + str(row.precip_icon) + "\n" +
                "PRECIP TYPE: " + str(row.precip_type) + "\n" +
                "WIND AVG: " + str(row.wind_avg) + "\n" +
                "WIND BEARING: " + str(row.wind_bearing) + "\n" +
                "CUR CONDITION: " + str(row.current_condition) + "\n" +
                "CUR ICON: " + str(row.current_icon) + "\n"
                "TODAY HIGH: " + str(row.temp_high_today) + "\n"
                "TODAY LOW: " + str(row.temp_low_today) + "\n"
            )


        # _LOGGER.info("GETTING HOURLY FORECAST DATA:")
        # data = await smartweather.get_forecast(FORECAST_TYPE_HOURLY, 48)
        # for row in data:
        #     _LOGGER.info("\n" +
        #         "TIME: " + str(row.timestamp) + "\n" +
        #         "CONDITIONS: " + str(row.conditions) + "\n" +
        #         "ICON: " + str(row.icon) + "\n" +
        #         "TEMP: " + str(row.temperature) + "\n" +
        #         "PRESSURE: " + str(row.pressure) + "\n" +
        #         "HUMIDITY " + str(row.humidity) + "\n" +
        #         "PRECIP: " + str(row.precip) + "\n" +
        #         "PRECIP PROBABILITY: " + str(row.precip_probability) + "\n" +
        #         "PRECIP ICON: " + str(row.precip_icon) + "\n" +
        #         "PRECIP TYPE: " + str(row.precip_type) + "\n" +
        #         "WIND AVG: " + str(row.wind_avg) + "\n" +
        #         "WIND GUST: " + str(row.wind_gust) + "\n" +
        #         "WIND BEARING: " + str(row.wind_bearing) + "\n" +
        #         "WIND DIRECTION: " + str(row.wind_direction) + "\n" +
        #         "UV: " + str(row.uv) + "\n" +
        #         "CUR ICON: " + str(row.current_icon) + "\n" +
        #         "FEELS LIKE: " + str(row.feels_like) + "\n"
        #     )

        # _LOGGER.info("GETTING DAILY RAW FORECAST DATA:")
        # data = await smartweather.get_daily_forecast_raw()
        # _LOGGER.info(json.dumps(data, indent=1))

    except SmartWeatherError as err:
        _LOGGER.info(err)

    end = time.time()

    _LOGGER.info("Execution time: %s seconds", end - start)


asyncio.run(main())