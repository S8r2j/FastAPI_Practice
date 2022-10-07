from fastapi import FastAPI, HTTPException
from datetime import datetime

from schemas import load_db, save_db, CarInput, CarOutput, TripOutput, TripInput

app = FastAPI(title="Car Sharing")

db = load_db()


# Adding an operation called get_cars()
# That is served at /api/cars
# And that returns all car data

# @app.get("/api/cars")
# def get_cars():
#     return db
@app.get("/api/cars")
def get_cars(size: str | None = None, doors: int | None = None) -> list:
    result = db
    if size:
        result = [car for car in result if car.size == size]
    if doors:
        result = [motor for motor in result if motor.doors >= doors]
    return result


@app.get("/api/cars/{id}")
def car_by_id(id: int = None) -> dict:
    result = db
    if id:
        result = [motors for motors in db if motors.id == id]
    if result:
        return result
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


@app.post("/api/cars", response_model=CarOutput)
def add_car(car: CarInput) -> CarOutput:
    new_car = CarOutput(size=car.size, doors=car.doors, fuel=car.fuel, transmission=car.transmission, id=len(db) + 1)
    db.append(new_car)
    save_db(db)
    return new_car


@app.delete("/api/cars", status_code=204)
def delete_car(id: int) -> None:
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        db.remove(car)
        save_db(db)
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found.")


@app.put("/api/cars", response_model=CarOutput)
def change_car(id: int, new_data: CarInput):
    matches = [car for car in db if car.id == id]
    if matches:
        car = matches[0]
        car.size = new_data.size
        car.fuel = new_data.fuel
        car.doors = new_data.doors
        car.transmission = new_data.transmission
        save_db(db)
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")


@app.post("/api/cars/{id}/trips", response_model=TripOutput)
def add_trip(car_id: int, trip: TripInput) -> TripOutput:
    matches = [car for car in db if car.id == car_id]
    if matches:
        car = matches[0]
        new_trip = TripOutput(id=len(car.trips) + 1, start=trip.start, end=trip.end, description=trip.description)
        car.trips.append(new_trip)
        save_db(db)
        return new_trip
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found.")
