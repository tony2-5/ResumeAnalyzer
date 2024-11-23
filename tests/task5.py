from fastapi.testclient import TestClient
from backend.main import app 
from backend.database import engine, metadata
from backend.auth import SECRET_KEY, ALGORITHM
import jwt
import pytest

client = TestClient(app)

@pytest.fixture(scope="function", autouse=True)
def databaseSetup():
    # Clear the database before each test
    metadata.drop_all(bind=engine) 
    metadata.create_all(bind=engine) 
    # create user for login tests
    client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )


def testSuccessfulLogin():
    response = client.post(
        "/api/login",
        json={"email": "user@example.com", "password": "securePassword"}
    )
    
    assert response.status_code == 200
    assert "accessToken" in response.json()
    token = response.json()["accessToken"]
    
    # decode the token to ensure it's valid
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert payload["sub"] == "user@example.com" 

def testInvalidPassword():
    response = client.post(
        "/api/login",
        json={"email": "user@example.com", "password": "wrongPassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email or password."}

def testUserNotFound():
    response = client.post(
        "/api/login",
        json={"email": "nonexistentuser@example.com", "password": "securePassword"}
    )
    
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid email or password."}