from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Players(Base):

    __tablename__ = "Player_Details"
    
    id = Column(Integer , primary_key=True, index=True)
    Player_Name = Column(String)
    Age = Column(Integer)
    Gender = Column(String)
    Sport = Column(String)