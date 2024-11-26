from fastapi.testclient import TestClient
from backend.main import app
from backend.database import engine, metadata
import pytest

client = TestClient(app)


@pytest.fixture(scope="function", autouse=True)
def databaseSetup():
    metadata.drop_all(bind=engine)
    metadata.create_all(bind=engine)

    client.post(
        "/api/register",
        json={
            "email": "user@example.com",
            "password": "securePassword",
            "username": "user123",
        },
    )

def testLoginGetUser():
    login_response = client.post(
        "/api/login",
        json={"email": "user@example.com", "password": "securePassword"}
    )
    assert login_response.status_code == 200
    assert "accessToken" in login_response.json()
    token = login_response.json()["accessToken"]

    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("api/users/me", headers=headers)
    assert response.status_code == 200
    assert response.json() == {
        "email": "user@example.com",
        "username": "user123",
    }


def testCurrentUserNotFound():
    headers = {"Authorization": f"Bearer wrong-token"}
    response = client.get("api/users/me", headers=headers)
    print(response.json())
    assert response.status_code == 401
    assert response.json() == {"detail": "Cannot authorize user."}