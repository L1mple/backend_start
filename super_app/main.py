from typing import Union

from fastapi import FastAPI, HTTPException, Path, Depends, Query, Request
from sqlalchemy.orm import Session

from loguru import logger
from super_app import schemas, crud, models
from super_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)


logger.remove()
logger.add("logs/logfile.log", format="{time:HH:mm:ss} | {level} | {message}", rotation="1 KB", retention=5)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Число машин на одной странице(для запроса с учетом пагинации)
number_of_cars_in_page = 3


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info(f"REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"RESPONSE CODE: {response.status_code}")
    return response


@app.get("/car/{car_id}", response_model=schemas.Car)
def read_item(car_id: Union[str, None] = Path(default=None, max_length=6, regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$",
                                              example="Г123Ло", description="Russian number with lower or upper case letters"), db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    return db_car


@app.post("/car", response_model=schemas.Car)
def create_item(car: schemas.Car, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car.car_id)
    if db_car:
        # update info
        return crud.replace_car(db=db, car=car)
    else:
        return crud.create_car(db=db, car=car)


@app.get("/car")
def read_item(page: int = Query(default=1, gt=0), per_page: int = Query(default=..., gt=0), db: Session = Depends(get_db)):
    if per_page < page:
        raise HTTPException(status_code=400, detail="per_page parameter must be greater than page parameter")
    else:
        return crud.get_all_cars(db=db, page=page, per_page=per_page, number_of_cars_in_page=number_of_cars_in_page)


@app.patch("/car", response_model=schemas.Car)
def update_item(car: schemas.UpdateCar, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car.car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    else:
        return crud.update_car(db=db, car=car)


@app.delete("/car/{car_id}", response_model=schemas.Car)
def delete_item(car_id: Union[str, None] = Path(default=None, max_length=6,
                                                example="Г123Ло", description="Russian number with lower or upper case letters"), db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    return crud.delete_car(db=db, car_id=car_id)
