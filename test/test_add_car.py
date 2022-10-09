from unittest.mock import Mock
from fastapi.testclient import TestClient

from carsharing import app
from routers.cars import add_car
from schemas import CarInput, User, Car

client=TestClient(app)


def test_add_car():
    response= client.post("/api/cars/",json={
        "doors": 5,
        "size": "xxl"
    }, headers={'Authorization': 'Bearer reindirect'})
    assert response.status_code==200
    car=response.json()
    assert car['doors']==5
    assert car['size']=='xxl'