# pySmartWeatherIO
Wrapper for the WeatherFlow Smart Weather REST API. Designed to work with Home Assistant.

This module communicates with a Smart Home Weather station from the company [WeatherFlow](http://weatherflow.com/smart-home-weather-stations/) using their REST API. It retrieves current weather data from the attached units. Currently they have two types of Units:
* **AIR** - This unit measures Temperature, Humidity, Pressure and Lightning Strikes
* **SKY** - This unit measures Precipitation, Wind, Illuminance and UV
They are both attached to a central hub, that broadcasts the data via UDP and sends the data to a cloud database managed by WeatherFlow. This module retrieves the data back from the cloud database.

## Functions
The module exposes the following functions:<br>
### SmartWeather(api_key, station_id, to_units, to_wind_units)
this will return a handle to the SmartWeather class and open the connection.<br>

**api_key**<br>
(string)(Required) The WeatherFlow REST API requires a API Key, but for personal use, you can use a development key, which you can [find here](https://weatherflow.github.io/SmartWeather/api/#getting-started). Please note the restrictions applied.

**station_id**<br>
(string)(required) If you have your own Smart Weather Station, then you know your Station ID. If you don't have one, there are a lot of public stations available, and you can find one near you on [this link](https://smartweather.weatherflow.com/map). If you click on one of the stations on the map, you will see that the URL changes, locate the number right after */map/* - this is the Station ID<br>

**to_units**<br>
(string)(optional) The unit system to use. metric or imperial<br>
Default value: metric<br>

**to_wind_units**<br>
(string)(optional) The wind unit system to use. mps (Meter pr second) or kmh (kilometer pr hour). Will be ignored if *to_units* is imperial<br> 
Default value: mps<br>

### get_station_hardware()
Returns a JSON array with information about the Station Hardware.<br>

* **station_name** The name of the Station as set by the User
* **serial_number** The serial number of the HUB Device
* **device_id** A unique device ID of the HUB Device
* **firmware_revision** The current firmware revision of the HUB Device

### get_station_data()
Returns a JSON array with current sensor values of the associated AIR and SKY or TEMPEST modules.<br>

* **air_temperature** - Current temperature
* **dew_point** - Dewpoint. The atmospheric temperature (varying according to pressure and humidity) below which water 
* **feels_like** - How the temperature Feels Like. A combination of Heat Index and Wind Chill
* **heat_index** - A temperature measurement combining Humidity and temperature. How hot does it feel. Only used when temperature is above 26.67°C (80°F)
* **wind_avg** - Current Average Wind Speed
* **wind_bearing** - Wind bearing in degrees (Example: 287°)
* **wind_chill** - How cold does it feel. Only used if temperature is below 10°C (50°F)
droplets begin to condense and dew can form
* **wind_direction** - Wind bearing as directional text (Example: NNW)
* **wind_gust** - Highest Wind Speed in the last minute
* **wind_lull** - Lowest Wind Speed in the last minute
* **precip_accum_local_day** - Precipitation since midnight
* **precip_rate** - The current precipitation rate - 0 if it is not raining
* **precip_accum_last_1hr** - Precipitation in the last hour
* **precip_accum_local_yesterday** - Precipitation yesterday
* **precip_minutes_local_day** - Number of minutes it has been raining for the current day
* **precip_minutes_local_yesterday** - Number of minutes it has been raining yesterday
* **station_pressure** - Current barometric pressure, taking in to account the position of the station
* **relative_humidity** - Current humidity in %
* **uv** - The UV index
* **solar_radiation** - The current Solar Radiation measured in W/m2
* **brightness** - Shows the brightness in Lux
* **lightning_strike_count** - Shows the numbers of lightning strikes for last minute. 

