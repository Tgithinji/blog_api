from app.main import app
from fastapi.testclient import TestClient
from app.schemas import *
from .testingdb import client, db
import pytest


# fixture to create new user to make login independent
@pytest.fixture
def test_user(client):
    data = {
        "username": "newuser",
        "email": "newuser@gmail.com",
        "password": "password123"
        }
    res = client.post("/users", json=data)
    new_user = res.json()
    new_user['password'] = data['password']
    return new_user



def test_create_user(client):
    res = client.post("/users", json={
        "username": "newuser",
        "email": "newuser@gmail.com",
        "password": "password123"
    })
    new_user = UserResponse(**res.json())
    assert res.status_code == 201
    assert new_user.email == 'newuser@gmail.com'


def test_login(client, test_user):
    res = client.post("/login", data={
        "username": test_user['username'],
        "password": test_user['password']
    })
    assert res.status_code == 200
