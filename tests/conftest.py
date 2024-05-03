from cgi import test
import json
from fastapi.testclient import TestClient
import pytest
from app.main import app
from db import database
from model import models
from io import BytesIO


# Tests for endpoints in user_router.py
@pytest.fixture()
def client():
    with TestClient(app) as test_client:
        yield test_client


# Drop and clear each table after test
@pytest.fixture(autouse=True)
def drop_all_tables():
    engine = database.engine
    yield
    models.Base.metadata.drop_all(engine)
    models.Base.metadata.create_all(engine)


# Create a user for every test
@pytest.fixture()
def create_user(client):
    try:
        user_data = {
            "username": "testuser",
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
            "email": "testuser@example.com",
        }
        image_file = BytesIO(b"fake image data")
        files = {
            "request": (None, json.dumps(user_data), "application/json"),
            "image": ("test_image.jpg", image_file, "image/jpeg"),
            "coverPhoto": ("test_cover.jpg", image_file, "image/jpeg"),
        }

        response = client.post("/user/create", files=files)
        assert response.status_code == 201
        created_user = response.json()
        created_user["password"] = user_data["password"]
        return created_user
    except Exception as e:
        print(e)
