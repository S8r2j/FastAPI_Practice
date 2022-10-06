from fastapi import FastAPI, HTTPException
from datetime import datetime

app = FastAPI()

db=[
    {"id": 1, "size": "s", "fuel": "gasoline", "doors": 3, "transmission":"auto"},
    {"id": 2, "size": "s", "fuel": "gasoline", "doors": 3, "transmission":"auto"},
    {"id": 3, "size": "s", "fuel": "electric", "doors": 5, "transmission":"manual"},
    {"id": 4, "size": "m", "fuel": "electric", "doors": 3, "transmission":"auto"},
    {"id": 5, "size": "m", "fuel": "hybrid", "doors": 5, "transmission":"auto"},
    {"id": 6, "size": "m", "fuel": "gasoline", "doors": 5, "transmission":"manual"},
    {"id": 7, "size": "l", "fuel": "diesel", "doors": 5, "transmission":"manual"},
    {"id": 8, "size": "l", "fuel": "electric", "doors": 5, "transmission":"auto"},
    {"id": 9, "size": "l", "fuel": "hybrid", "doors": 5, "transmission":"auto"}
]
# Adding an operation called get_cars()
# That is served at /api/cars
# And that returns all car data

# @app.get("/api/cars")
# def get_cars():
#     return db
@app.get("/api/cars")
def get_cars(size:str|None=None, doors:int|None=None)->list:
    result=db
    if size:
        result= [car for car in result if car['size']==size]
    if doors:
        result= [motor for motor in result if motor['doors']>=doors]
    return result

@app.get("/api/cars/{id}")
def car_by_id(id:int=None)->dict:
    result=db
    if id:
        result = [motors for motors in db if motors['id']==id]
    if result:
        return result
    else:
        raise HTTPException(status_code=404, detail=f"No car with id={id}.")

@app.get("/")
def welcome(name):
    """Returns the friendly welcome message"""
    return{'message': f"Welcome, {name}, to the Car sharing service!"}

@app.get("/date")
def date():
    """Returns the friendly welcome message"""
    return{'message':datetime.now()}