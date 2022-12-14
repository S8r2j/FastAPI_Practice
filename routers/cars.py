
from fastapi import Depends, HTTPException, APIRouter
from sqlmodel import Session, select

from db import get_session
from routers.auth import get_current_user
from schemas import Car, CarOutput, CarInput, Trip, TripInput, User


router= APIRouter(prefix="/api/cars")


@router.get("/")
def get_cars(size: str | None = None, doors: int | None = None, session: Session= Depends(get_session)) -> list:
        query=select(Car)
        if size:
            query=query.where(Car.size==size)
        if doors:
            query=query.where(Car.doors>=doors)
        return session.exec(query).all()


@router.get("/{id}", response_model=CarOutput)
def car_by_id(id: int = None, session: Session= Depends(get_session)) -> dict:
    car=session.get(Car,id)
    if car:
        return car
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")




@router.post("/", response_model=Car)
def add_car(car_input: CarInput, session: Session= Depends(get_session),user: User=Depends(get_current_user)) -> Car:
        new_car = Car.from_orm(car_input)
        session.add(new_car)
        session.commit()
        session.refresh(new_car)
        return new_car


@router.delete("/", status_code=204)
def delete_car(id: int, session: Session=Depends(get_session)) -> None:
    car=session.get(Car,id)
    if car:
        session.delete(car)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id} found.")


@router.put("/", response_model=CarOutput)
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


@router.post("/{id}/trips", response_model=Trip)
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
