from hmac import new
import json
from security.hash import Hash


# Test for retriving a user
def test_get_user(client, create_user):
    # Test retrieving a user
    response = client.get(f"/user/{create_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == create_user["email"]
    assert data["firstName"] == create_user["firstName"]
    assert data["lastName"] == create_user["lastName"]
    assert "password" not in data


# Test for creating a user
def test_create_user(client):
    with open("files/image/helo.jpg", "rb") as image_file, open(
        "files/coverphoto/spike.jpg", "rb"
    ) as cover_file:
        payload = {
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

        new_user = client.post(
            "/user/create",
            data={"request": json.dumps(payload)},
            files={"image": image_file, "coverPhoto": cover_file},
        )
    assert new_user.status_code == 201
    assert new_user.json()["email"] == payload["email"]
    assert new_user.json()["firstName"] == payload["firstName"]
    assert new_user.json()["lastName"] == payload["lastName"]


# Test for partially updating a user using PATCH
def test_patch_user(client, create_user):
    payload = {"fullName": "Updated Patch User"}

    files = {
        "request": (None, json.dumps(payload), "application/json"),
    }
    response = client.patch(f"user/{create_user['id']}/update", files=files)
    assert response.status_code == 200
    assert response.json()["fullName"] == payload["fullName"]


# Test for updating all fields of a user using PUT
def test_put_user(client, create_user):

    payload = {
        "username": "updateduser",
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
        "email": "updateduser@example.com",
    }
    files = {"request": (None, json.dumps(payload), "application/json")}

    response = client.put(f"/user/{create_user['id']}/updateall", files=files)
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]
    assert response.json()["firstName"] == payload["firstName"]
    assert response.json()["lastName"] == payload["lastName"]
    assert response.json()["fullName"] == payload["fullName"]


# Test for deleting a user
def test_delete_user(client, create_user):

    response = client.delete(f"/user/{create_user['id']}")
    assert response.status_code == 200
    assert response.json() == {
        "message": f"User with id: {create_user['id']} is deleted."
    }

    fetch_deleted_user = client.get(f"user/{create_user['id']}")
    assert fetch_deleted_user.status_code == 404
    assert fetch_deleted_user.json() == {
        "detail": f"User with {create_user['id']} not found."
    }


# Test for invalid user request since some important fields are missing on creation
def test_input_validation(client, create_user):
    payload = {
        "address": "",
        "bio": "",
        "changeProfile": "false",
        "city": "",
        "country": "",
        "dob": "2024-01-01",
        "emailConfirmed": "false",
        "firstLogin": "true",
        "firstName": "",
        "fullName": "",
        "lastName": "",
        "password": "test123",
    }

    files = {"request": (None, json.dumps(payload), "application/json")}

    response = client.post("/user/create", files=files)
    assert response.status_code == 400


# Test for validation of user request whenever it is being updated, since some important fields are missing
def test_validation_patch(client, create_user):

    payload = {
        "address": "",
        "bio": "",
        "changeProfile": "false",
        "city": "",
        "country": "",
        "dob": "2024-01-01",
        "emailConfirmed": "false",
        "firstLogin": "true",
        "firstName": "",
        "fullName": "",
        "lastName": "",
        "password": "test123",
    }

    files = {"request": (None, json.dumps(payload), "application/json")}

    response = client.patch(f"/user/{create_user['id']}/update", files=files)
    assert response.status_code == 400


# Same test as PATCH validation but for PUT
def test_validation_put(client, create_user):

    payload = {
        "address": "Updated village",
        "bio": "Updated bio",
        "changeProfile": "false",
        "city": "Updated City",
        "country": "test country",
        "dob": "2024-01-23",
        "emailConfirmed": "true",
        "firstLogin": "false",
        "firstName": "",
        "fullName": "",
        "gender": "other",
        "isActive": "true",
        "lastName": "User",
        "phoneNumber": "123456789",
        "state": "Davao del Norte",
        "street": "Updated street",
        "userType": "Admin",
        "zipCode": "7895",
        "password": "updatedtest123",
        "email": "updateduser@example.com",
    }

    files = {"request": (None, json.dumps(payload), "application/json")}

    response = client.put(f"/user/{create_user['id']}/updateall", files=files)
    assert response.status_code == 400
