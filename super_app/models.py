from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Car(Base):
    __tablename__ = "Cars_data"

    car_id = Column(String(6), primary_key=True)
    model = Column(String)
    owner = Column(String(11))
    mileage = Column(Float)