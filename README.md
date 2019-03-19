# pySmartWeatherIO
Wrapper for the WeatherFlow Smart Weather REST API. Designed to work with Home Assistant.

This module communicates with a Smart Home Weather station from the company [WeatherFlow](http://weatherflow.com/smart-home-weather-stations/) using their REST API. It retrieves current weather data from the attached units. Currently they have two types of Units:
* **AIR** - This unit measures Temperature, Humidity, Pressure and Lightning Strikes
* **SKY** - This unit measures Precipitation, Wind, Illuminance and UV
They are both attached to a central hub, that broadcasts the data via UDP and sends the data to a cloud database managed by WeatherFlow. This module retrieves the data back from the cloud database.

## Functions
The module exposes the following functions:
***load_stationdata(stationid, apikey, units)*** - this will return a Data Class with all the data collected from a specific Station.<br>
**stationid**<br>
(string)(required) If you have your own Smart Weather Station, then you know your Station ID. If you don't have one, there are a lot of public stations available, and you can find one near you on [this link](https://smartweather.weatherflow.com/map). If you click on one of the stations on the map, you will see that the URL changes, locate the number right after */map/* - this is the Station ID<br>

**api_key**<br>
(string)(Required) The WeatherFlow REST API requires a API Key, but for personal use, you can use a development key, which you can [find here](https://weatherflow.github.io/SmartWeather/api/#getting-started). Please note the restrictions applied.

**units**<br>
(string)(optional) The unit system to use. Metric or Imperial<br>
Default value: Metric
