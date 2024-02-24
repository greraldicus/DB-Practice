from .database import engine, SessionLocal, Base
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, ForeignKey


class People(Base):
    __tablename__ = 'peoples'
    id = Column(Integer, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    sex = Column(String)
    region_id = Column(Integer, ForeignKey('regions.id'), nullable=True)

class Regions(Base):
    __tablename__ = 'regions'
    id = Column(Integer, primary_key=True, index=True)
    region_name = Column(String)

session = SessionLocal()



