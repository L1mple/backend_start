from sqlalchemy.orm import Session
from  sqlalchemy import func, select

from super_app import schemas, models


def validate_car_owner(car_owner: str):
    if car_owner:
        if len(car_owner) == 11 and car_owner[4] != "-":
            car_owner = car_owner[:4] + "-" + car_owner[5:]
        elif len(car_owner) == 10:
            car_owner = car_owner[:4] + "-" + car_owner[4:]
    return car_owner


def get_car(db: Session, car_id: str):
    return db.query(models.Car).filter(models.Car.car_id == car_id.upper()).first()


def get_all_cars(db: Session, page: int, per_page: int, number_of_cars_in_page: int):
    return db.query(models.Car).order_by(models.Car.car_id).all()[(page-1)*number_of_cars_in_page:per_page*number_of_cars_in_page]


def create_car(db: Session, car: schemas.Car):
    car.owner = validate_car_owner(str(car.owner))
    db_car = models.Car(
        car_id=car.car_id.upper(),
        model=car.model,
        owner=car.owner,
        mileage=car.mileage

    )
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def update_car(db: Session, car: schemas.UpdateCar):
    car.owner = validate_car_owner(str(car.owner))
    db_car = get_car(db, car.car_id)
    car_data = car.dict(exclude_unset=True)
    for key, value in car_data.items():
        setattr(db_car, key, value)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: str):
    db_car = db.query(models.Car).filter(models.Car.car_id == car_id.upper()).first()
    db.delete(db_car)
    db.commit()
    return db_car


def replace_car(db: Session, car: schemas.Car):
    car.owner = validate_car_owner(str(car.owner))
    db_car = get_car(db, car.car_id)
    car_data = car.dict(exclude_unset=False)
    for key, value in car_data.items():
        setattr(db_car, key, value)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
