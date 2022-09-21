from typing import Union
from pydantic import BaseModel, Field


class Car(BaseModel):
    car_id: Union[str, None] = Field(description="Russian car number", max_length=6, example="К897ЩА",
                                     regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$")
    model: Union[str, None] = Field(default=None, description="Model of car", example="BMW X999")
    # Номер паспорта через -
    owner: Union[str, None, int] = Field(default=None, description="Passport number", min_length=10, max_length=11,
                                         example="1234-123456", regex=r"^[0-9]{4}.[0-9]{6}$")
    mileage: float = Field(default=0.0, description="mileage of the car in kilometers")

    class Config:
        orm_mode = True


class UpdateCar(BaseModel):
    car_id: Union[str, None] = Field(description="Russian car number", max_length=6, example="К897ЩА",
                                     regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$")
    model: Union[str, None] = Field(default=None, description="Model of car", example="BMW X999")
    # Номер паспорта через -
    owner: Union[str, None, int] = Field(default=None, description="Passport number", min_length=10, max_length=11,
                                         example="1234-123456", regex=r"^[0-9]{4}.[0-9]{6}$")
    mileage: Union[float, None] = Field(default=None, description="mileage of the car in kilometers")

    class Config:
        orm_mode = True
