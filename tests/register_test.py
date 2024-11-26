from fastapi.testclient import TestClient
from backend.main import app 
from backend.database import engine, metadata
import pytest

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def clearDatabase():
    # Clear the database before each test
    metadata.drop_all(bind=engine) 
    metadata.create_all(bind=engine) 

def testRegisterValid():
    response = client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )
    assert response.status_code == 201
    assert response.json() == {"message": "User registered."}

def testRegisterDuplicateEmail():
    client.post(
        "/api/register",
        json={
            "email": "duplicate@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )

    response = client.post(
        "/api/register",
        json={
            "email": "duplicate@example.com",
            "password": "anotherPassword",
            "username": "user456",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered."}

def testRegisterInvalidEmail():
    response = client.post(
        "/api/register",
        json={
            "email": "not-an-email",
            "password": "securePassword",
            "username": "user123",
        },
    )
    assert response.status_code == 400
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]

def testRegisterMissingEmail():
    response = client.post(
        "/api/register",
        json={
            "password": "securePassword",
            "username": "user123",
        },
    )
    assert response.status_code == 400
    assert "Field required" in response.json()["detail"][0]["msg"]

def testRegisterMissingPassword():
    response = client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "username": "user123",
        },
    )
    assert response.status_code == 400
    assert "Field required" in response.json()["detail"][0]["msg"]

def testRegisterMissingUsername():
    response = client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "securePassword",
        },
    )
    print(response.json())
    assert response.status_code == 400
    assert "Field required" in response.json()["detail"][0]["msg"]
