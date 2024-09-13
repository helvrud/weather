import os
from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This code creates an sqlite database and prepare the columns
db_url = "sqlite:///weatherdb.sqlite"
engine = create_engine(db_url)
Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    time = Column(DateTime)
    temperature_2m = Column(Float)
    surface_pressure = Column(Float)
    wind_speed_10m = Column(Float) 
    wind_direction_10m = Column(Float)
    wind_direction = Column(String)
    precipitation = Column(Float)
    interval = Column(Integer) 
    

if not os.path.exists("weatherdb.sqlite"):
    Base.metadata.create_all(engine)
    
    
    
    