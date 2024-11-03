from app.schemas import *
from app.jwt_handler import settings as set
from jose import jwt
import pytest


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

@pytest.mark.parametrize("username, password, status_code", [
    ('wrongname', 'password123', 403),
    ('wrongemail@gmail.com', 'password123', 403),
    ('newuser', 'wrongpassword', 403),
])
def test_login_failure(client, test_user, username, password, status_code):
    res = client.post("/login", data={
        "username": username,
        "password": password
    })
    assert res.status_code == status_code


def test_get_user(client, test_user):
    res = client.get(f"/users/{test_user['id']}")
    assert res.status_code == 200
    user = UserWithPosts(**res.json())
    assert user.User.email == test_user['email']
