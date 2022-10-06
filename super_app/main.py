from typing import Union

from fastapi import FastAPI, HTTPException, Path, Depends, Query, Request
from sqlmodel import Session

from loguru import logger

from super_app import crud, models
from super_app.database import engine


def create_db_and_tables():
    models.SQLModel.metadata.create_all(engine)


logger.remove()
logger.add("logs/logfile.log", format="{time:HH:mm:ss} | {level} | {message}", rotation="1 KB", retention=5)

app = FastAPI()


# Dependency
def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    logger.info(f"REQUEST: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"RESPONSE CODE: {response.status_code}")
    return response


@app.get("/car/{car_id}", response_model=models.Car)
def read_item(car_id: Union[str, None] = Path(default=None, max_length=6, regex=r"^[А-я]{1}[0-9]{3}[А-я]{2}$",
                                              example="Г123Ло", description="Russian number with lower or upper case letters"), db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if db_car is None:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    return db_car


@app.post("/car", response_model=models.Car)
def create_item(car: models.Car, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id=car.car_id)
    if db_car:
        # update info
        return crud.replace_car(db=db, car=car)
    else:
        return crud.create_car(db=db, car=car)


@app.get("/car")
def read_item(page: int = Query(default=1, gt=0), per_page: int = Query(default=..., gt=0), db: Session = Depends(get_db)):
    return crud.get_all_cars(db=db, page=page, per_page=per_page)


@app.patch("/car", response_model=models.Car)
def update_item(car: models.UpdateCar, db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car.car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    else:
        return crud.update_car(db=db, car=car)


@app.delete("/car/{car_id}", response_model=models.Car)
def delete_item(car_id: Union[str, None] = Path(default=None, max_length=6,
                                                example="Г123Ло", description="Russian number with lower or upper case letters"), db: Session = Depends(get_db)):
    db_car = crud.get_car(db, car_id)
    if not db_car:
        raise HTTPException(status_code=404, detail="404 NOT FOUND")
    return crud.delete_car(db=db, car_id=car_id)
