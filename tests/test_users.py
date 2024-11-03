from app.main import app
from fastapi.testclient import TestClient
from app.schemas import *
from .testingdb import client, db
from app.jwt_handler import settings as set
from jose import jwt
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
    ## decode token received to check if its valid
    res_body = Token(**res.json())
    payload = jwt.decode(res_body.access_token, set.secret_key, algorithms=[set.algorithm])

    id = payload.get('user_id')
    assert test_user['id'] == id
    assert res.status_code == 200
