import os
from sqlalchemy import Column, Integer, Float, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# This code creates an sqlite database and prepare the columns
db_url = "sqlite:///weatherdb.sqlite"
engine = create_engine(db_url)
Base = declarative_base()

class Weather(Base):
    __tablename__ = "weather"
    id = Column(Integer, primary_key=True)
    temperature_2m = Column(Float)
    surface_pressure = Column(Float)
    wind_speed_10m = Column(Float) 
    wind_direction_10m = Column(Float)
    precipitation = Column(Float)

if os.path.   
Base.metadata.create_all(engine)