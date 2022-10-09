from sqlmodel import Session
from super_app import models


def validate_car_owner(car_owner: str):
    """
    Get string number and transform it to (1234-123456)
    For example: (1234123456 -> 1234-123456)
    :param car_owner: Owner's passport number (example = "1234-123456")
    :return:
    """
    if car_owner:
        if len(car_owner) == 11 and car_owner[4] != "-":
            car_owner = car_owner[:4] + "-" + car_owner[5:]
        elif len(car_owner) == 10:
            car_owner = car_owner[:4] + "-" + car_owner[4:]
    return car_owner


def get_car(db: Session, car_id: str):
    """
    Queries the database and return Car model with (car_id=car_id)
    :param db: Session to database
    :param car_id: Russian car number (example = "К897ЩА")
    :return:
    """
    return db.query(models.Car).filter(models.Car.car_id == car_id.upper()).first()


def get_all_cars(db: Session, page: int, per_page: int):
    """
    Queries the database and return massive of Car models
    :param db: Session to database
    :param page: Number of page
    :param per_page: Number of cars on each page
    :return:
    """
    return db.query(models.Car).order_by(models.Car.car_id).offset((page - 1) * per_page).limit(per_page).all()


def create_car(db: Session, car: models.Car):
    """
    Queries the database to create a record about the car and returns the created model
    :param db: Session to database
    :param car: Car model in json format
    :return:
    """
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


def update_car(db: Session, car: models.UpdateCar):
    """
    Queries the database to update information in record about the car and returns updated model
    :param db: Session to database
    :param car: UpdateCar model in json format
    :return:
    """
    car_data = car.dict(exclude_unset=True)
    car.owner = validate_car_owner(str(car.owner))
    db_car = get_car(db, car.car_id)
    for key, value in car_data.items():
        setattr(db_car, key, value)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


def delete_car(db: Session, car_id: str):
    """
    Queries the database to delete record about the car and returns deleted model
    :param db: Session to database
    :param car_id: Russian car number (example = "К897ЩА")
    :return:
    """
    db_car = db.query(models.Car).filter(models.Car.car_id == car_id.upper()).first()
    db.delete(db_car)
    db.commit()
    return db_car


def replace_car(db: Session, car: models.Car):
    """
    Queries the database to update information in record about the car and returns updated model
    :param db: Session to database
    :param car: Car model in json format
    :return:
    """
    car.owner = validate_car_owner(str(car.owner))
    db_car = get_car(db, car.car_id)
    car_data = car.dict(exclude_unset=False)
    for key, value in car_data.items():
        setattr(db_car, key, value)
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car
