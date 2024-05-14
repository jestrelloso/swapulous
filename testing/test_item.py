from pydoc import plain
import pytest
from fastapi.testclient import TestClient
from app.main import app
from db import database
from model import models


# Tests for endpoints in user_router.py
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def drop_all_tables():
    engine = database.engine
    yield
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)


def create_user(client):
    payload = {
        "address": "Spring village",
        "bio": "This is a test bio! Hi there!",
        "changeProfile": "false",
        "city": "Davao City",
        "country": "Philippines",
        "dob": "2024-01-01",
        "emailConfirmed": "false",
        "firstLogin": "true",
        "firstName": "Test",
        "fullName": "Test user",
        "gender": "male",
        "isActive": "true",
        "lastName": "User",
        "phoneNumber": "123456",
        "state": "Davao del Sur",
        "street": "Green street",
        "userType": "User",
        "zipCode": "8000",
        "password": "test123",
    }

    new_user = client.post("/user/create", json=payload)
    return new_user


def test_create_user(client):
    response = create_user(client)

    assert response.status_code == 201
    assert response.json()["fullName"] == "Test user"
    assert response.json()["firstName"] == "Test"
    assert response.json()["lastName"] == "User"


def test_patch_user(client):
    new_user = create_user(client)
    payload = {"fullName": "Updated Patch User", "password": "updatedtest123"}

    response = client.patch(f"/user/{new_user.json()['id']}/update", json=payload)
    assert response.status_code == 200
    assert response.json()["fullName"] == payload["fullName"]

    # plain_txt_pwd = payload["password"]
    # hashed_pwd = response.json()["password"]
    # assert Hash.verify(hashed_pwd, plain_txt_pwd) == True


def test_put_user(client):
    new_user = create_user(client)
    payload = {
        "address": "Updated village",
        "bio": "Updated bio",
        "changeProfile": "false",
        "city": "Updated City",
        "country": "Uruguay",
        "dob": "2024-01-23",
        "emailConfirmed": "true",
        "firstLogin": "false",
        "firstName": "Updated",
        "fullName": "Updated user",
        "gender": "other",
        "isActive": "true",
        "lastName": "User",
        "phoneNumber": "123456789",
        "state": "Davao del Norte",
        "street": "Updated street",
        "userType": "Admin",
        "zipCode": "7895",
        "password": "updatedtest123",
    }

    response = client.put(f"/user/{new_user.json()['id']}/updateall", json=payload)
    assert response.status_code == 200
    assert response.json()["fullName"] == payload["fullName"]
    assert response.json()["firstName"] == payload["firstName"]
    assert response.json()["lastName"] == payload["lastName"]

    # plain_txt_pwd = payload["password"]
    # hashed_pwd = response.json()["password"]

    # assert Hash.verify(hashed_pwd, plain_txt_pwd) == True


def test_get_user(client):
    new_user = create_user(client)

    response = client.get(f"/user/{new_user.json()['id']}")
    assert response.status_code == 200
    assert response.json()["fullName"] == new_user.json()["fullName"]
    assert response.json()["firstName"] == new_user.json()["firstName"]
    assert response.json()["lastName"] == new_user.json()["lastName"]


def test_delete_user(client):
    new_user = create_user(client)

    response = client.delete(f"/user/{new_user.json()['id']}")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"User with id: {new_user.json()['id']} is deleted."
    }

    fetch_deleted_user = client.get(f"user/{new_user.json()['id']}")
    assert fetch_deleted_user.status_code == 404
    assert fetch_deleted_user.json() == {
        "detail": f"User with {new_user.json()['id']} not found."
    }
