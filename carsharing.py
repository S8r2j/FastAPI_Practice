from fastapi import FastAPI, HTTPException, Depends
from datetime import datetime

from schemas import CarInput, CarOutput, TripOutput, TripInput, Car, Trip
from sqlmodel import create_engine, SQLModel, Session, select

app = FastAPI(title="Car Sharing")


engine = create_engine(
    "sqlite:///carsharing.db",
    connect_args={"check_same_thread": False},
    echo=True
)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)



def get_session():
    with Session(engine) as session:
        yield session
# Adding an operation called get_cars()
# That is served at /api/cars
# And that returns all car data

# @app.get("/api/cars")
# def get_cars():
#     return db
@app.get("/api/cars")
def get_cars(size: str | None = None, doors: int | None = None, session: Session= Depends(get_session)) -> list:
        query=select(Car)
        if size:
            query=query.where(Car.size==size)
        if doors:
            query=query.where(Car.doors>=doors)
        return session.exec(query).all()


@app.get("/api/cars/{id}", response_model=CarOutput)
def car_by_id(id: int = None,session: Session= Depends(get_session)) -> dict:
    car=session.get(Car,id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.get("/")
def welcome(name):
    """Returns the friendly welcome message"""
    return {'message': f"Welcome, {name}, to the Car sharing service!"}


@app.get("/date")
def date():
    """Returns the friendly welcome message"""
    return {'message': datetime.now()}


@app.post("/api/cars/", response_model=Car)
def add_car(car_input: CarInput,session: Session= Depends(get_session)) -> Car:
        new_car = Car.from_orm(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car)
        return new_car


@app.delete("/api/cars", status_code=204)
def delete_car(id: int, session: Session=Depends(get_session)) -> None:
    car=session.get(Car,id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found.")


@app.put("/api/cars", response_model=CarOutput)
def change_car(id: int, new_data: CarInput, session: Session= Depends(get_session)):
    car=session.get(Car,id)
    if car:
        car.size = new_data.size
        car.fuel = new_data.fuel
        car.doors = new_data.doors
        car.transmission = new_data.transmission
        session.add(car)
        session.commit()
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars/{id}/trips", response_model=Trip)
def add_trip(car_id: int, trip_input: TripInput, session: Session=Depends(get_session)) -> Trip:
    car=session.get(Car,car_id)
    if car:
        new_trip = Trip.from_orm(trip_input, update={'car_id':car_id})
        car.trips.append((new_trip))
        session.commit()
        session.refresh(new_trip)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found.")
