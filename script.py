import openmeteo_requests
import asyncio

import requests_cache
import pandas as pd
from retry_requests import retry


async def getWeatherData():
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        # "latitude": 55.70593, "longitude": 37.37000, # Skoltech
        "latitude": 50.06248, "longitude": 14.41990, # Prague
        "current": ["temperature_2m",
                "surface_pressure",
                "wind_speed_10m",
                "wind_direction_10m",
                "precipitation",
                "weather_code"]
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation {response.Elevation()} m asl")
    print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

    # Process hourly data. The order of variables needs to be the same as requested.
    current = response.Current()
    temperature_2m = current.Variables(0).Value()
    surface_pressure =  current.Variables(1).Value()
    wind_speed_10m =  current.Variables(2).Value()
    wind_direction_10m =  current.Variables(3).Value()
    precipitation =  current.Variables(4).Value()
    weather_code =  current.Variables(5).Value()

    current_data = {"date": pd.date_range(
        start = pd.to_datetime(current.Time(), unit = "s", utc = True),
        end = pd.to_datetime(current.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = current.Interval()),
        # inclusive = "left"
    )}
    current_data["temperature_2m"] = temperature_2m
    current_data["surface_pressure"] = surface_pressure
    current_data["wind_speed_10m"] = wind_speed_10m
    current_data["wind_direction_10m"] = wind_direction_10m
    current_data["precipitation"] = precipitation
    current_data["weather_code"] = weather_code
    print (current_data)
    return current_data





async def main():
    task1 = asyncio.create_task(getWeatherData())
    # task2 = asyncio.create_task(fun2(4))


asyncio.run(main())

    
# current_dataframe = pd.DataFrame(data = current_data)
# print(current_data)
