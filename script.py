import asyncio
import pandas as pd
from pprint import pprint
import time
from aiohttp import ClientSession
import json
from sqlalchemy.orm import sessionmaker
from models import Weather, engine
from datetime import datetime



def convert_wind_direction(deg):
    # This function convers the degree of wind direction to a string
    # It uses assumption that the degree ranges from 0 to 360
    if deg>337.5: return 'N'
    if deg>292.5: return 'NW'
    if deg>247.5: return 'W'
    if deg>202.5: return 'SW'
    if deg>157.5: return 'S'
    if deg>122.5: return 'SE'
    if deg>67.5: return 'E'
    if deg>22.5: return 'NE'
    return 'N'


# initiate a databese interaction session 
Sessiondb = sessionmaker(bind=engine)
sessiondb = Sessiondb()

async def get_weather():
    # This function fetches data from open-meteo.com and returns it as a python dictionary
    async with ClientSession() as sessionhttp:
        url = f'https://api.open-meteo.com/v1/forecast'
        params = {
            "latitude": 55.70593, "longitude": 37.37000, # Skoltech
            # "latitude": 50.06248, "longitude": 14.41990, # Prague
            "current": ["temperature_2m",
                    "surface_pressure",
                    "wind_speed_10m",
                    "wind_direction_10m",
                    "precipitation",
                    ]
        }
        async with sessionhttp.get(url=url, params=params) as response:
            weather_json = await response.json()
                        
            # This converts a string provided by 'time' field to a datetime format
            weather_json['current']['time'] = datetime.strptime(weather_json['current']['time'], '%Y-%m-%dT%H:%M')
            
            # The following converts the angle of the winf direction to a string like 'NW', 'SE', etc
            dir = weather_json['current']['wind_direction_10m']
            weather_json['current']['wind_direction'] = convert_wind_direction(dir)
            
            print('Weather data fetched ', weather_json['current']['time'])
            
    return weather_json
        
async def write_db():
        # This function collects 100 samples of weather data and stores them to sqlite database. 
        # Since the data on the server renews only every 15 minutes, we should call the sample collection not often than once in 15 minutes
        for i in range(100):
            # But we are not going to wait, so I set the interval to 2 seconds
            await asyncio.sleep(2)
            weather_json = await get_weather()
        
            # pprint(weather_json["current"])
            weather = Weather(**weather_json["current"])
            sessiondb.add(weather)
            sessiondb.commit()
        

def export_db():
    # This function grabs the data from database and uses pandas library for exporting it to Excell fomat 
    
    #~ a lambda function for converting the db row to dictionary
    dbrow_to_dict  = lambda r: {c.name: getattr(r, c.name) for c in r.__table__.columns}
    excel_file_name = "weather.xlsx"
    
    user_input = input("\npress 'y' if you want to export the collected data to Excell\n")
    print("Export data to " + excel_file_name)
    if user_input=='y':
        weather_data_array = sessiondb.query(Weather).all()
        weather_df = pd.DataFrame()
        for row in weather_data_array:
            row_as_dict = dbrow_to_dict(row)
            # pprint(row_as_dict)
            weather_df = weather_df.append(row_as_dict, ignore_index = True)
        # pprint(weather_df)
        weather_df.to_excel(excel_file_name, index=False)

        
    
async def main():

    # run the prompt to export database on the background. 
    # As soon as you press 'y' the execution is over.
    _= asyncio.create_task(write_db())
    # create a coroutine for the blocking export_db function call
    coroutine = asyncio.to_thread(export_db)
    # execute the call in a new thread and await the result
    await coroutine
    

print(time.strftime('%X'))

asyncio.run(main())

print(time.strftime('%X'))