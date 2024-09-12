from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base


db_url = "sqlite:///weatherdb.sqlite"
engine = create_engine(db_url)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    
Base.metadata.create_all(engine)
