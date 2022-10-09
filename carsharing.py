from fastapi import FastAPI, Request
from routers import cars, web

from db import engine
from sqlmodel import SQLModel

app = FastAPI(title="Car Sharing")
app.include_router(cars.router)
app.include_router(web.router)


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.middleware("http")
async def add_cars_cookie(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="cars_cookie", value="you_visited_this_app")
    return response

