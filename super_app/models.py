from sqlalchemy import Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlmodel import SQLModel, Field
from typing import Union

# Base = declarative_base()


# class Car(Base):
#     __tablename__ = "Cars_data"
#
#     car_id = Column(String(6), primary_key=True)
#     model = Column(String)
#     owner = Column(String(11))
#     mileage = Column(Float)


class Car(SQLModel, table=True):
    """
    Car model for database and validation requests

    car_id - Russian car number (example = "К897ЩА")
    model - Model of car (string)
    owner - Owner's passport number (example = "1234-123456")
    mileage - Mileage of a car (float)
    """
    __tablename__ = "Cars_data"

    car_id: Union[None, str] = Field(default=..., description="Russian car number", max_length=6,
                                     regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$", primary_key=True)
    model: Union[None, str] = Field(default=None, description="Model of car")
    # Номер паспорта через -
    owner: Union[None, str] = Field(default=None, description="Passport number", min_length=10, max_length=11,
                                    regex=r"^[0-9]{4}.[0-9]{6}$")
    mileage: Union[None, float] = Field(default=0.0, description="mileage of the car in kilometers")

    class Config:
        schema_extra = {
            "example": {
                "car_id": "К897ЩА",
                "model": "ZAZ",
                "owner": "1234-123456",
                "mileage": 3.2,
            }
        }


class UpdateCar(SQLModel):
    """
    Car model for PATCH request

    car_id - Russian car number (example = "К897ЩА")
    model - Model of car (string)
    owner - Owner's passport number (example = "1234-123456")
    mileage - Mileage of a car (float)
    """
    car_id: Union[None, str] = Field(default=..., description="Russian car number", max_length=6,
                                     regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$")
    model: Union[None, str] = Field(default=None, description="Model of car")
    # Номер паспорта через -
    owner: Union[None, str, int] = Field(default=None, description="Passport number", min_length=10, max_length=11,
                                         regex=r"^[0-9]{4}.[0-9]{6}$")
    mileage: Union[None, float] = Field(default=None, description="mileage of the car in kilometers")

    class Config:
        schema_extra = {
            "example": {
                "car_id": "К897ЩА",
                "model": "ZAZ-2",

            }
        }
